from copy import deepcopy
import numpy as np
import time, math
import random as rand
import decimal

class CityState:

    def __init__(self, city, positions, police):
        self.city = city
        self.positions = positions
        self.police = police
        self.points = self.calculate_score()
        self.conflicts = self.calculate_cost()

    # Method to calculate the heuristic of current state
    def calculate_cost(self):

        conflicts = 0

        for i in range(n):
            for j in range(i + 1, n):
                if self.positions[i] != -1 and self.positions[j] != -1:
                    # Horizontal axis
                    if self.positions[i] == self.positions[j]:
                        conflicts = conflicts + 1
                    # Diagonal Axis Positive
                    if abs(self.positions[i] - self.positions[j]) == abs(i - j):
                        conflicts = conflicts + 1

        return conflicts


    def calculate_score(self):
        score = 0

        for i in range(0, len(self.positions)):
            if self.positions[i] != -1:
                score += self.city[self.positions[i]][i]


        return score


def read_input():

    with open('input1.txt', 'r') as input_file:
        n = int(input_file.readline())
        police = int(input_file.readline())
        scooters = int(input_file.readline())
        city = [[0 for x in range(n)] for y in range(n)]
        for line in input_file:
            location = line.strip().split(',')
            city[int(location[1])][int(location[0])] += 1

    return n, police, scooters, city


def write_output(max_score):
    with open('output.txt', 'w') as output_file:
        output_file.write(max_score)


def find_solution(state):

    print(state.conflicts)

    max_score = 0
    T = 4800
    alpha = 0.9
    # Continue to search until a goal node is reached
    for i in range(0, 170000):
        T = T * alpha

        next_state = get_random_state(state.city, state.police)
        dw = next_state.conflicts - state.conflicts
        exp = decimal.Decimal(decimal.Decimal(math.e) ** (decimal.Decimal(-dw) * decimal.Decimal(T)))

        if dw > 0 or rand.uniform(0, 1) < exp:
            state = next_state


        print(state.points)
        if state.conflicts == 0:
            if state.points > max_score:
                max_score = state.points
            state = get_random_state(state.city, state.police)



    return str(max_score)


def randomNeighbour(state):
    col_list = []

    n = len(state.positions)

    i = rand.randint(0, n-1)
    while True:
        if state.positions[i] != -1:
            break
        else:
            i = rand.randint(0, n-1)

    col_list.append(i)

    for j in range(0, n):
        if state.positions[j] == -1:
            col_list.append(j)

    final_col = col_list[rand.randint(0, len(col_list)-1)]
    final_row = rand.randint(0, len(state.positions)-1)
    state.positions[final_col] = final_row
    if final_col != i:
        state.positions[i] = -1

    new_state = CityState(state.city, state.positions, state.police)

    return new_state


def get_random_state(city, police):
    positions = [-1 for x in range(n)]
    for i in range(0, police):
        positions[i] = rand.randint(0, n - 1)
    return CityState(city, positions, police)

if __name__ == '__main__':
    start = time.time()
    n, police, scooters, city = read_input()
    #print(city)
    #n = 15
    #police = 15
    #city = [[16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16], [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16], [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16], [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16], [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16], [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16], [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16], [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16], [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16], [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16], [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16], [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16], [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16], [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16], [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]]

    current_state = get_random_state(city, police)
    max_score = find_solution(current_state)
    end = time.time()
    print("Time is - {}".format(end-start))
    write_output(max_score)
