# ● Design a program that determines the award a person competing in a
# triathlon will receive.
# ● Your program should read in the times (in minutes) for all three events of a
# triathlon, namely swimming, cycling, and running, and then calculate and
# display the total time taken to complete the triathlon.

swim_time = int(input("How many minutes did the swim take the triathlete in minutes?\n"))
cycle_time = int(input("How many minutes did the cycle take the triathlete in minutes?\n"))
run_time = int(input("How many minutes did the run take the triathlete in minutes?\n"))

total_time = swim_time + cycle_time + run_time
print(f"Triathlon total time taken: {total_time} minutes.")

# ● The award a participant receives is based on the total time taken to
# complete the triathlon. The qualifying time for awards is 100 minutes.
# Display the award that the participant will receive based on the following
# criteria:

# Qualifying Criteria ~ Time Range ~ Award
# Within the qualifying time. ~ 0 - 100 minutes ~ Provincial Colours
# Within 5 minutes of the qualifying time. ~ 101 - 105 minutes ~ Provincial Half Colours
# Within 10 minutes of the qualifying time. ~ 106 - 110 minutes ~ Provincial Scroll
# More than 10 minutes off from the qualifying time. ~ 111+ minutes ~ No award

if total_time > 110:
    print("More than 10 mins off qualifying time of 100mins. No award.")
elif total_time > 105:
    print("Within 10 mins above qualifying time of 100mins. Provincial Scroll awarded.")
elif total_time > 100:
    print("Within 5 min above qualifying time of 100mins. Provincial Half Colours awarded.")
elif total_time >= 0:
    print("Within the qualifying time of 100mins or less. Provincial Colours awarded.")
else:
    print("Time taken must be more than 0 mins. Input times again.")

