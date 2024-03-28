# Imports for Natural Language Processing (NLP), dataset manipulation, and PDF generation/opening
import spacy  # NLP
import pandas as pd  # Dataset manipulation
from spacytextblob.spacytextblob import SpacyTextBlob  # Sentiment analysis
from reportlab.lib.styles import getSampleStyleSheet  # PDF design and generation
from reportlab.lib import colors
from reportlab.graphics.charts.piecharts import Pie
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Image
from reportlab.graphics.shapes import Drawing
from datetime import datetime  # Get current date/time for PDF name
import webbrowser  # Opens PDF in user's default PDF application
from multiprocessing import Pool, cpu_count  # Parallel processing


# Preprocess text data by stripping and removing stop words from the reviews column in a batch, parallel processing pipeline. Use spaCy is_stop to exclude stop words
def preprocess_texts(texts: list[str], nlp: spacy.language.Language) -> list[str]:
    """
    Processes already lowercased texts to remove stop words, remove punctuation, and strip unneeded whitespace characters. The function utilises spaCy's .pipe() for efficient parallelised batch processing. Compared to applying a function to each member of the column individually, this approach significantly enhances performance when preprocessing a large number of texts by leveraging the pipeline's ability to process texts as a stream, and batch up reviews to be worked on in chunks. All available CPU cores will be utilised in order to reduce processing time.

    Text should be already lowercased, e.g. using pandas: texts = df["reviews.text"].str.lower(), before passing as the first parameter to this function.

    Parameters:
        - texts (list[str]): A list of lowercase raw texts from product reviews to be processed. Each element in the list is a string representing a single review's text.
        - nlp (spacy.language.Language | spacy.language.PipeCallable): Instance of nlp text-processing pipeline from loading selected spaCy language model elsewhere in the script. Utilising the .pipe method from this instance allows for efficient batch processing of text data. The spacy.language.PipeCallable type, returned when calling spacy.load(<model_name>).add_pipe(<pipe_component_name>) on the nlp instance, is technically valid for use here, although explicit type hinting for PipeCallable is omitted to avoid linting issues and maintain clarity in documentation.

    Returns:
        - list[str]: A list of processed texts. Each element in the returned list corresponds to the cleaned and processed text of each review in the input list. The processing includes removing stop words, converting text to lowercase, removing punctuation, and stripping leading and trailing whitespace from each token.

    Example usage:
        >>> nlp = spacy.load("en_core_web_sm")
        >>> texts = ["this is the first review in lowercase.", "here's another review!"]
        >>> processed_texts = preprocess_texts(texts, nlp)
        >>> print(processed_texts)
        ['first review', 'another review']
    """
    processed_texts = []

    # The only component of spaCy required is the tokeniser, allowing to check a token for being a stop word, so enable only that component and disable the rest. nlp will be restored to full functionality at the end of the with block.
    with nlp.select_pipes(enable="tokenizer"):

        # Process texts as a stream using nlp.pipe, which is more efficient for batch processing, along with using n_process parameter to parallelise the processing across all the CPU cores available
        # Batch size chosen is reasonable for shorter texts like product reviews

        for doc in nlp.pipe(texts, batch_size=400, n_process=-1):

            # Filter out stop words, lowercase the tokens, remove punctuation, and strip whitespace
            tokens = [
                token.text.strip()
                for token in doc
                if (not token.is_stop and not token.is_punct)
            ]

            # Join the meaningful (i.e., non-stop and non-punctuation) words in the sentence back with single spaces between words
            processed_text = " ".join(tokens)

            # Append to the output list, which will be used to form a cleaned text column of the reviews
            processed_texts.append(processed_text)

    return processed_texts


# Function for batch processing sentiment analysis using spacytextblob pipe methods
def get_sentiments(texts: list[str]) -> list[str]:
    """
    Processes texts to determine sentiments, utilising the spacytextblob extension for sentiment analysis with spaCy's nlp.pipe for efficient batch processing. Parallelisation is achieved through spawning new running instances of a worker function, and using imports from multiprocessing: Pool and cpu_count(). The results list from each worker function instance are flattened into a single output list of sentiment labels, which can be added to the original dataframe inplace.

    With the spacytextblob component engaged, the pipeline cannot be serialised, so new instances of the spacytextblob pipeline will be created once per spawn of the worker function, since spaCy's inbuilt parallelisation methods cannot work in this situation.

    Parameters:
        - texts (list[str]): A list of preprocessed, lowercased texts from product reviews to be analysed for sentiment. Each element in the list is a string representing the cleaned and preprocessed text of a single review.

    Returns:
        - list[str]: A list of sentiment labels. Each element in the returned list corresponds to the sentiment analysis result of each review in the input list, categorised as "Positive", "Negative", or "Neutral".

    Example usage:
        >>> texts = ["i love this product", "this was a terrible purchase"]
        >>> sentiments = get_sentiments(texts)
        >>> print(sentiments)
        ['Positive', 'Negative']
    """

    # Determine CPU count
    n_cores = cpu_count()

    # Split texts list into a list of approximately equal-sized chunks, based on the number of cores
    chunk_size = len(texts) // n_cores + 1
    text_chunks = [texts[i : i + chunk_size] for i in range(0, len(texts), chunk_size)]

    # Create a Pool of processes, as many as there are CPU cores, to parallelise processing, before the stage of batching
    with Pool(n_cores) as pool:

        # Worker processes of chunk_sentiment_worker are mapped to each chunk of the column, and will batch process reviews inside each chunk
        result_chunks = pool.map(chunk_sentiment_worker, text_chunks)

    # Flattening the list of lists (chunks) into a single list of sentiment results, of the same length as the texts list parameter which was originally passed in
    # Use list comprehension with nested for loops to iterate through each chunk of sentiments, and append them all to the same flat, non-nested list
    results = [sentiment for chunk in result_chunks for sentiment in chunk]

    return results


# Worker function which spawns NLP instances from spaCy each time it is called, reducing run time of processing
def chunk_sentiment_worker(texts_chunk: list[str]) -> list[str]:
    """
    Worker function, to be spawned when parallel processing for sentiment analysis at reduced time of execution. Given a chunk of a larger list of strings, this function will use spacytextblob-generated sentiment attributes to convert polarity score (in the range -1 to 1) to a human-understandable descriptive text label string. Batch processing pipeline methods of spaCy are utilised.

    Important: This function will create a new spaCy NLP instance with the required spacytextblob component, each time it is called. This is important to allow parallel processing through reducing competition for access to the NLP instance between parallel threads. This approach favours speed of processing over memory-saving tactics, and will use the CPU maximally to minimise the time taken to analyse sentiments.

    Parameters:
        - texts_chunk (list[str]): A list of lowercase raw texts from product reviews to be processed. Each element in the list is a string representing a single review's text.

    Returns:
        - list[str]: Sentiment labels of "Positive", "Negative", or "Neutral", in a list of strings.

    NOTE: This function is not meant to be run directly by the user, but rather as a subprocess of the get_sentiments() function.
    Example usage:
        >>> texts = ["i love this product", "this was a terrible purchase"]
        >>> sentiments = chunk_sentiment_worker(texts)
        >>> print(sentiments)
        ['Positive', 'Negative']
    """
    # Initialise output list
    sentiments = []

    # Instantiate spaCy nlp with spacytextblob pipe enabled
    # Load en_core_web_sm spaCy model to enable natural language processing, classification and sentiment analysis of the product reviews
    worker_nlp = spacy.load("en_core_web_sm")
    # Add TextBlob component to the pipeline
    worker_nlp.add_pipe("spacytextblob")

    # Disable components of the nlp pipe callable which aren't directly related to spacytextblob, to save processing time. nlp will be restored to full functionality at the end of the with block.
    with worker_nlp.select_pipes(enable=["spacytextblob"]):
        # Batch size of 50 is reasonable in the context of product review texts
        for doc in worker_nlp.pipe(texts_chunk, batch_size=50):
            # The polarity score from TextBlob is accessed through spaCy's token extension (._.blob.polarity.sentiment)
            pol = doc._.blob.sentiment.polarity
            # Polarity is a float between -1 and 1. Positive polarity is close to 1, negative to -1, and neutral is at 0: here being close to 0 is used as a proxy for being mostly neutral
            sentiment = (
                "Positive" if pol > 0.1 else "Negative" if pol < -0.1 else "Neutral"
            )
            # Add the sentiment label to the output list
            sentiments.append(sentiment)

    return sentiments


# Using spaCy doc.similarity() method to return a score
def get_similarity(
    review1: str,
    review2: str,
    nlp: spacy.language.Language,
) -> float:
    """Calculates the similarity between two product reviews.

    Parameters:
        - review1 (str): The cleaned text of the first review.
        - review2 (str): The cleaned text of the second review.
        - nlp (spacy.language.Language): Instance of nlp text-processing pipeline from loading selected spaCy language model elsewhere in the script. spacy.language.PipeCallable is also a valid type to pass (calling spacy.load(<model_name>).add_pipe(<pipe_component_name>) on the nlp instance technically returns PipeCallable), although type hinting for this in a docstring creates linting issues and is therefore omitted.

    Returns:
        - float: Similarity score in the range 0 to 1.
    """
    doc1 = nlp(review1)
    doc2 = nlp(review2)
    return doc1.similarity(doc2)


# Using reportlab library to generate a PDF
def generate_report(
    df: pd.DataFrame,
    positive_count: int,
    negative_count: int,
    neutral_count: int,
    similarity_score: float,
    review1: str,
    review2: str,
) -> None:
    """
    Generates a PDF report summarising the sentiment analysis and similarity of product reviews, using reportlab library. Includes a pie chart and sections with text. It is passed the results of the functions and formats the result to a new PDF file in the current directory, labelling the PDF filename with the current date and time.

    Parameters:
        - df (pandas.DataFrame): The DataFrame containing product reviews and sentiment labels.
        - positive_count (int): The number of positive reviews.
        - negative_count (int): The number of negative reviews.
        - neutral_count (int): The number of neutral reviews.
        - similarity_score (float): The similarity score returned for the pair of reviews analysed by get_similarity().
        - review1 (str): First review which was passed to get_similarity().
        - review2 (str): Second review which was passed to get_similarity().

    Returns:
        - None. This functions writes to a PDF in the current directory.
    """
    # Concatenate the current date and time with the title and add the correct PDF file extension
    pdf_path = (
        f"sentiment_analysis_report-{datetime.now().strftime('%d-%m-%Y_%H-%M')}.pdf"
    )

    # Create doc template tied to the given pdf path filename
    pdf_doc = SimpleDocTemplate(pdf_path)

    # Get the default style sheet
    styles = getSampleStyleSheet()

    # Override and modify the "Normal" style directly to better space out paragraphs throughout PDF
    styles["Normal"].spaceAfter = 12

    # Initialise document story
    story = []

    # Title
    story.append(
        Paragraph(
            "Amazon Product Review Sentiment Analysis Report: PDF composed in Python with reportlab library",
            styles["Heading1"],
        )
    )
    story.append(Spacer(1, 12))

    # Dataset Description
    story.append(Paragraph("Dataset Description", styles["Heading2"]))
    story.append(
        Paragraph(
            "This report analyses the sentiment of customer reviews for Amazon products dated between 2010 and 2018, sourced from bestbuy.com and amazon.com. The dataset is retrieved from the file named <link href='https://www.kaggle.com/datasets/datafiniti/consumer-reviews-of-amazon-products' underline=True color=blue>1429_1.csv (48.99MB) from this page on Kaggle.com</link> and contains 34,660 reviews.",
            styles["Normal"],
        )
    )
    story.append(
        Paragraph(
            "All columns except reviews.text were dropped, since they will not be used for the current scope of sentiment distribution analysis. In future work, other columns would be required in order to draw correlations and predictive analytics between aspects of the dataset which may be interrelated.",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 12))

    # Preprocessing Steps
    story.append(Paragraph("Preprocessing Steps", styles["Heading2"]))
    story.append(
        Paragraph(
            "Leveraging spaCy, pandas, and inbuilt Python string manipulation functions, the following preprocessing steps were applied to the review text column:",
            styles["Normal"],
        )
    )
    story.append(
        Paragraph(
            "- Text cleaning: Removed stop words, punctuation, and converted to lowercase.",
            styles["Normal"],
        )
    )

    # Performance Considerations
    story.append(Paragraph("Performance Considerations", styles["Heading2"]))
    story.append(
        Paragraph(
            "- In order to reduce duration of preprocessing, the preprocessing function was refactored from an approach of using a lambda function to apply to every review one by one, to a pipeline/text stream-based function using spaCy's pipe functionality. Batch processing occurs, as well as parallelisation, thanks to spaCy's parameters inside the nlp.pipe(texts, batch_size, n_processes) function. Thereby, reviews are bunched together to be processed in batches, and the pipe will create as many functions as it can - limited by the number of CPU cores.",
            styles["Normal"],
        )
    )
    story.append(
        Paragraph(
            "- The bottleneck in preprocessing comes from the fact that there is a single nlp instance which must share its logical resources despite the parallelisation, and it is likely that creating worker functions with individual nlp instances would reduce runtime greatly. This latter approach is applied to sentiment analysis further down.",
            styles["Normal"],
        )
    )
    story.append(PageBreak())

    # Sentiment Analysis Results
    story.append(Paragraph("Sentiment Analysis Results", styles["Heading2"]))
    story.append(
        Paragraph(
            f"The sentiment analysis identified {positive_count} positive reviews, {negative_count} negative reviews, and {neutral_count} neutral reviews.",
            styles["Normal"],
        )
    )
    story.append(
        Paragraph(
            f"- spaCy is used in pipeline with a spacytextblob component engaged, and it is via TextBlob attributes that the sentiment and polarity of the reviews is judged. These counts are highly likely to change if the model could see the entire sentence in every case, e.g. without preprocessing, which could impact the meaning of the sentences in the reviews. It is also likely that a beefier language model would disagree with the small English spaCy language model used here, which lacks proper vectors between representations of word meanings for reasons of capacity limitation.",
            styles["Normal"],
        )
    )
    story.append(
        Paragraph(
            f"- There is an artistic licence in counting neutral reviews, since polarity is a continuous scalar floating point value in the range -1 to 1, meaning you are unlikely to find reviews which have a score of a perfect 0. Widening or narrowing the bounds for what is considered basically neutral will naturally alter the counts of the sentiment labels of the reviews dataset.",
            styles["Normal"],
        )
    )

    # Pie chart (sentiment distribution)
    # Prepare chart data
    data = [positive_count, negative_count, neutral_count]
    labels = ["Positive", "Negative", "Neutral"]
    colours = [colors.green, colors.red, colors.blue]  # positive, negative, neutral
    drawing = Drawing(400, 200)
    pie = Pie()
    pie.data = data
    pie.labels = labels
    pie.x = 150  # Set chart position
    pie.y = 50
    pie.simpleLabels = 0
    pie.sideLabels = 1

    for i, colour in enumerate(colours):
        pie.slices[i].popout = i * 4 + 2  # Spread pie segments apart
        pie.slices[i].fillColor = colour  # Colour each slice

    drawing.add(pie)

    # Add chart as an image to the report
    story.append(Image(drawing, width=400, height=200, hAlign="CENTER"))

    # Sample Reviews
    story.append(Paragraph("Sample Reviews", styles["Heading2"]))

    # Positive Sample
    positive_review_sample = df[df["sentiment"] == "Positive"]["reviews.text"].iloc[0]
    story.append(
        Paragraph(
            f"Positive review sample: <i>{positive_review_sample}</i>",
            styles["Normal"],
        )
    )

    # Negative Sample
    negative_review_sample = df[df["sentiment"] == "Negative"]["reviews.text"].iloc[0]
    story.append(
        Paragraph(
            f"Negative review sample: <i>{negative_review_sample}</i>",
            styles["Normal"],
        )
    )

    # Neutral Sample
    neutral_review_sample = df[df["sentiment"] == "Neutral"]["reviews.text"].iloc[0]
    story.append(
        Paragraph(
            f"Neutral review sample: <i>{neutral_review_sample}</i>",
            styles["Normal"],
        )
    )

    # Commentary on Accuracy
    story.append(Paragraph("Commentary on Accuracy", styles["Heading3"]))
    story.append(
        Paragraph(
            f"- The positive review seems an adequate categorisation. The negative review is not that negative, it is close to as positive as can be, save for one small detail. The neutral review sounds a lot more positive than neutral, perhaps the confounding word is 'disappointed', but the model should be able to see the whole context of the token and state that this is a positive review.",
            styles["Normal"],
        )
    )
    story.append(
        Paragraph(
            f"- It is debatable whether reviews are being accurately categorised to an adequate standard for executive decision making. There are plenty of nuances in speech, including sarcasm and humour, which it is hard for such a small language model to pick up on.",
            styles["Normal"],
        )
    )
    story.append(
        Paragraph(
            f"- Furthermore, there is additional useful data to be integrated to get the full picture: e.g., did the customer return the product? What was the title of the review? Does the user buy other products in the same category thereby making their opinion a more comparative one? There are ways that objectivity can also be analysed, using spacytextblob, and this could be incorporated for deeper value to be extracted from these reviews.",
            styles["Normal"],
        )
    )

    # Insights
    story.append(Paragraph("Insights", styles["Heading2"]))
    story.append(
        Paragraph(
            "Based on the sentiment distribution, the high percentage of positive reviews suggests customer satisfaction. On the other hand, one can qualitatively notice some reviews which are falsely categorised. Further analysis of positive/negative review content can reveal valuable perspectives into customer preferences and areas for improvement, only if the confidence in the sentiment analysis component is high. One should consider all columns that might be relevant to informing future stock/procurement/delivery service improvement decisions to be made.",
            styles["Normal"],
        )
    )
    story.append(PageBreak())

    # Review Similarity Example
    story.append(Paragraph("Review Similarity Example", styles["Heading2"]))
    story.append(
        Paragraph(f"Review 1: {review1}", styles["Normal"])
    )  # Display Review 1
    story.append(
        Paragraph(f"Review 2: {review2}", styles["Normal"])
    )  # Display Review 2
    story.append(
        Paragraph(
            f"The similarity score between the selected reviews is: {similarity_score:.2f}. The main purpose of this display is to show how spaCy has inbuilt methods that allow similarities between sentences to be estimated. There raises, however, a warning:",
            styles["Normal"],
        )
    )
    story.append(
        Paragraph(
            "<i>UserWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.</i>",
            styles["Normal"],
        )
    )
    story.append(
        Paragraph(
            f"...and this warning tells us we should be using a medium-sized or larger spaCy language model to accurately leverage insights from similar reviews (to extract key themes, understand commonalities between satisfied customers in order to maximise customer satisfaction in future, and more).",
            styles["Normal"],
        )
    )
    story.append(
        Paragraph(
            "- <b>Generally</b>: Reviews with high similarity scores likely discuss similar themes, while low scores suggest diverse or contrasting opinions. It is fruitful to point out that the similarity scores are judged from the raw reviews.text column in this instance, rather than the cleaned text column since this may have cleaned out the nuance in the review.",
            styles["Normal"],
        )
    )
    story.append(
        Paragraph(
            "- <b>Caution</b>: However, using user-entered text data is dangerous at the point of analysis. There may be typographical errors as seen in Review 1 above; there may be unfamiliar slang, abbreviations, or pop culture references. These all along with extra myriad factors that can confound a language model and cause its similarity score to stray from something a human would judge.",
            styles["Normal"],
        )
    )
    story.append(PageBreak())

    # Strengths
    story.append(Paragraph("Model Strengths", styles["Heading2"]))
    story.append(
        Paragraph(
            "Here are some strengths of the sentiment analysis model:", styles["Normal"]
        )
    )
    story.append(
        Paragraph(
            "- <b>Identifies overall sentiment quickly</b>: The model distinguishes between positive, negative, and neutral reviews, aiding in understanding overall customer sentiment. With my modifications to make the preprocessing and sentiment analysis run quicker, this approach represents a decent quick and dirty first-pass attempt at analytics of free text, which is often the hardest data to analyse in a dataset.",
            styles["Normal"],
        )
    )
    story.append(
        Paragraph(
            "- <b>Potential for customer insights</b>: Analysing the patterns or themes within positive and negative reviews can provide valuable insights into customer preferences and pain points. It would be wise to continue adding to the Natural Language Processing arsenal employed here, by extracting entities which are mentioned, perhaps taking a lemmatised approach, using a best-guess spelling corrector function, keeping polarity as a scalar rather than a categorical variable, and more.",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 6))

    # Limitations
    story.append(Paragraph("Model Limitations", styles["Heading2"]))
    story.append(
        Paragraph(
            "- <b>Difficulty in understanding nuance</b>: Sentiment analysis models may not always capture sarcasm or complex emotions. Additionally, the accuracy can be influenced by the dataset size and quality. It's recommended to manually review a sample of classified reviews to assess model performance, so a next step if trying to test this pipeline would be to compare human-labelled sentiments of reviews to what this model outputs for its best guess of sentiment.",
            styles["Normal"],
        )
    )
    story.append(
        Paragraph(
            "- <b>Tradeoffs and the scientific approach</b>: It would be fruitful to try with bigger models, always accounting for a balance of runtime, memory usage, CPU effort, and budget to provide for these resources. In all cases, logging and timing data should be collected to add a degree of impartiality to improving the analysis pipeline.",
            styles["Normal"],
        )
    )

    # Future Research Directions
    story.append(Paragraph("Future Research Directions", styles["Heading2"]))
    story.append(
        Paragraph(
            "- <b>Experiment with other spaCy Models</b>: Experiment with medium-sized spaCy models (e.g., en_core_web_md) to potentially improve the accuracy of sentiment analysis and similarity scores.",
            styles["Normal"],
        )
    )
    story.append(
        Paragraph(
            "- <b>Evaluation</b>: Include quantitative evaluation metrics (accuracy, precision, recall, F1-score) to compare the performance of the model before and after optimisations and with different spaCy models. Use a manually labelled dataset for this purpose.",
            styles["Normal"],
        )
    )

    # Build, save, and open the PDF in default PDF viewer
    pdf_doc.build(story)
    webbrowser.open(pdf_path)


# Entry point for the script, orchestrating the sentiment analysis process
def main():

    # Greet user and inform them to wait
    print(
        "The reviews data is being loaded, preprocessed, and analysed. A PDF will be generated and saved, wherein you can read the methods and insights of this data analysis. \n\nThis is likely to take a couple of minutes..."
    )

    # Load en_core_web_sm spaCy model to enable natural language processing, classification and sentiment analysis of the product reviews
    nlp = spacy.load("en_core_web_sm")
    # Add TextBlob component to the pipeline
    nlp.add_pipe("spacytextblob")

    print(
        "Loaded spaCy pipeline, using language model 'en_core_web_sm' with a TextBlob component..."
    )

    # Read CSV of Amazon product reviews, only need the review free text column
    df = pd.read_csv("amazon_product_reviews.csv", usecols=["reviews.text"])

    print("Loaded Product Reviews CSV...")

    # Drop missing values (pandas dropna) before preprocessing - this alters the original dataframe and drops rows with missing text reviews
    df = df.dropna()
    # Remove rows where "reviews.text" is an empty string
    df = df[df["reviews.text"].str.strip() != ""]
    # Reset index to account for dropped rows
    df = df.reset_index(drop=True)

    print("Dropped rows with empty reviews, and reset dataframe index...")

    # Convert the "reviews.text" column to a list to pass to preprocess_texts for batch preprocessing text manipulation involving nlp object methods and attributes
    # Pandas inbuilt string lowercasing function is useful to use before passing to the preprocessing function
    df["cleaned_text"] = preprocess_texts(df["reviews.text"].str.lower().tolist(), nlp)

    print(
        "Preprocessed the reviews data - stripped of punctuation and meaningless stop words, lowercased all words..."
    )

    # Apply sentiment analysis to the dataframe in a batch processing style, first converting to a list
    df["sentiment"] = get_sentiments(df["cleaned_text"].tolist())

    print("Sentiment of all reviews analysed...")

    # Sample 10 rows to show the preprocessing, sentiment analysis; qualitatively check for accuracy
    print(
        "Here is a sample review plus its preprocessed form and the calculated sentiment..."
    )
    print(df.sample(1)[["reviews.text", "cleaned_text", "sentiment"]])

    # Totalling each sentiment classification for later comparison
    print("Counting members of each sentiment category...")
    positive_count = sum(df["sentiment"] == "Positive")
    negative_count = sum(df["sentiment"] == "Negative")
    neutral_count = sum(df["sentiment"] == "Neutral")

    # Select two reviews for comparison - any row of the dataframe could have been picked
    review1 = df["reviews.text"][10]
    review2 = df["reviews.text"][20]

    # Calculate similarity between the two reviews
    similarity_score = get_similarity(review1, review2, nlp)
    print("Similarity between two sample reviews has been calculated...")

    # Create PDF with all the results and it will be written to the current directory
    generate_report(
        df,
        positive_count,
        negative_count,
        neutral_count,
        similarity_score,
        review1,
        review2,
    )

    print(
        "---\nReport has been generated and opened in your default PDF viewer. \nThank you for analysing your reviews.\n---"
    )


# This script is meant to be run directly, not imported. Guard case boilerplate:
if __name__ == "__main__":
    main()
