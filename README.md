# Beware-of-the-police-
Positioning the police on a city to monitor scooters !


So imagine a city where we are promoting scooters to reduce some traffic ! Not a bad idea, right. But more scooters on roads of that like Los Angeles, more is the safety concern.

There is a need to place some police team on roads at certain places so that they could monitor the scooter traffic. Wow, cool! So that's the whole idea here.

Let us assume we know the coordinates of the city and suppose there are some scooters which we know would be at some positions during the day. Our goal is to place the police optimally such that we gain more acivity points.

So what are activity points ? Assume if a scooter and police are at same coordinate, then we gain an activity point.

Just maximize the score is the target !

We can have constraints here. There is no point in placing officers next to each other. So lets put some n-queen problem rules here ;)
1.Officers cannot be in same square, same row, same column, or along the same diagonal.
2.Officers cannot move

Input: The file input.txt in the current directory of your program will be formatted as
follows:
First line: strictly positive 32-bit integer n, the width and height of the n x n city area, n <= 15.
Second line: strictly positive 32-bit integer p, the number of police officers
Third line: strictly positive 32-bit integer s, the number of scooters
Next s*12 lines: the list of scooter x,y coordinates over time, separated with the End-of-line
character LF. With s scooters and 12 timesteps in a day, this results in 12 coordinates per
scooter.

Output:
Max activity points: strictly positive 32-bit integer m  


There are two approaches in the code, one goes with A* search using heuristics and other using Simulated Annealing!
