from copy import deepcopy
import numpy as np
import time

class CityState:

    def __init__(self, city, positions, police, points, pos):
        self.city = city
        self.positions = positions
        self.police = police
        self.points = points
        self.n = len(city)
        self.pos = pos
        self.heuristic = self.calculate_heuristic()

    # Method to calculate the heuristic of current state
    def calculate_heuristic(self):

        max_list = []
        for i in range(0, self.n):
            col_max = -1

            for j in range(0, self.n):
                if self.positions[j][i] == 0 and self.city[j][i] > col_max:
                    col_max = self.city[j][i]

            if col_max != -1:
                max_list.append(col_max)

        max_list.sort(reverse=True)
        h = 0
        if len(max_list) < self.police:
            return -10000

        for i in range(0, self.police):
            h += max_list[i]
        return h


def read_input():

    with open('input.txt', 'r') as input_file:
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


def check_column_validity(state, col):

    for i in range(0, state.n):
        if state.positions[i][col] == 0:
            return True

    return False


def get_heuristic(state, row, col):
    new_police = state.police - 1
    new_positions = deepcopy(state.positions)
    new_positions = mark_invalid(new_positions, row, col)
    new_state = CityState(state.city, new_positions, new_police, state.points, "")
    return new_state.heuristic


def find_max_pos_col(state, col):
    x = -1
    column_max = -1
    for i in range(0, state.n):
        if state.positions[i][col] == 0:
            score = state.city[i][col] + get_heuristic(state, i, col)
            if score > column_max :
                column_max = score
                x = i

    return x


def mark_invalid(positions, row, col):
    for i in range(0, len(positions)):
        if positions[row][i] != 2:
            positions[row][i] = 1
        if positions[i][col] != 2:
            positions[i][col] = 1
    i = row + 1
    j = col + 1
    while (i < len(positions) and i >= 0) and (j < len(positions[0]) and j >= 0):
        if positions[i][j] != 2:
            positions[i][j] = 1
        i += 1
        j += 1

    i = row + 1
    j = col - 1
    while (i < len(positions) and i >= 0) and (j < len(positions[0]) and j >= 0):
        if positions[i][j] != 2:
            positions[i][j] = 1
        i += 1
        j -= 1

    i = row - 1
    j = col - 1
    while (i < len(positions) and i >= 0) and (j < len(positions[0]) and j >= 0):
        if positions[i][j] != 2:
            positions[i][j] = 1
        i -= 1
        j -= 1

    i = row - 1
    j = col + 1
    while (i < len(positions) and i >= 0) and (j < len(positions[0]) and j >= 0):
        if positions[i][j] != 2:
            positions[i][j] = 1
        i -= 1
        j += 1

    return positions


def compute_score(city, positions):
    score = 0
    for i in range(0, len(positions)):
        for j in range(0, len(positions)):
            if positions[i][j] == 2:
                score += city[i][j]


    return score


def get_all_configurations(state):
    new_matrix = deepcopy(state.positions)
    m = np.array(new_matrix)
    score = state.points
    #print(score)

    x = compute_score(state.city, np.flip(m, 0))
    #print(x)
    if x > score:
        score = x

    m = np.rot90(m)

    x = compute_score(state.city, m)
    #print(x)
    if x > score:
        score = x
    x = compute_score(state.city, np.flip(m, 0))
    #print(x)
    if x > score:
        score = x

    m = np.rot90(m)

    x = compute_score(state.city, m)
    #print(x)
    if x > score:
        score = x
    x = compute_score(state.city, np.flip(m, 0))
    #print(x)
    if x > score:
        score = x

    m = np.rot90(m)

    x = compute_score(state.city, m)
    #print(x)
    if x > score:
        score = x
    x = compute_score(state.city, np.flip(m, 0))
    #print(x)
    if x > score:
        score = x




    return score



def find_solution(state):

    open_set = []
    closed_set = set()
    open_set.append(state)
    start = time.time()

    max_score = 0

    while open_set:

        if time.time() - start > 175:
            return str(max_score)

        curr_state = open_set.pop(0)

        if curr_state.police == 0:
            #print("Hello\n")
            max_points = get_all_configurations(curr_state)

            if max_points > max_score:
                max_score = curr_state.points
            continue

        if curr_state.points + curr_state.heuristic <= max_score:
            continue

        flag = True
        s = 0

        for i in range(0, curr_state.n):
            if check_column_validity(curr_state, i):
                new_city = curr_state.city
                new_positions = deepcopy(curr_state.positions)
                new_police = curr_state.police - 1
                x = find_max_pos_col(curr_state, i)
                if x == -1:
                    continue
                new_points = curr_state.points + curr_state.city[x][i]
                new_positions = mark_invalid(new_positions, x, i)
                new_positions[x][i] = 2
                new_str = list(curr_state.pos)
                new_str[i] = ""+str(x)
                new_str = "".join(new_str)
                new_state = CityState(new_city, new_positions, new_police, new_points, new_str)
                if new_str in closed_set:
                    continue
                if flag:
                    s = new_state.points + new_state.heuristic
                    open_set.insert(0, new_state)
                else:
                    if new_state.points + new_state.heuristic > s:
                        s = new_state.points + new_state.heuristic
                        open_set.insert(0, new_state)
                    else:
                        open_set.append(new_state)
                closed_set.add(new_str)





    return str(max_score)


if __name__ == '__main__':
    #start = time.time()
    #n, police, scooters, city = read_input()
    #print(city)
    city = [[27, 29, 34, 22, 47, 1, 27, 6, 34, 2, 47, 24, 21, 20, 30], [31, 31, 24, 17, 39, 16, 41, 39, 46, 3, 9, 41, 3, 43, 49], [21, 35, 16, 14, 17, 35, 25, 2, 6, 45, 22, 2, 13, 27, 26], [48, 9, 14, 8, 42, 2, 11, 7, 28, 37, 39, 43, 23, 18, 6], [1, 14, 29, 14, 36, 8, 49, 44, 37, 9, 3, 0, 31, 41, 50], [42, 39, 28, 14, 37, 7, 26, 24, 38, 30, 38, 14, 25, 7, 31], [41, 36, 10, 8, 39, 37, 32, 13, 45, 46, 27, 11, 46, 15, 29], [44, 4, 17, 22, 49, 44, 35, 45, 35, 33, 0, 25, 13, 48, 29], [26, 46, 29, 9, 16, 2, 34, 10, 12, 43, 3, 15, 29, 7, 25], [41, 19, 38, 4, 10, 19, 15, 30, 3, 50, 44, 11, 26, 49, 0], [31, 21, 46, 17, 33, 4, 27, 31, 5, 40, 18, 6, 35, 50, 14], [4, 43, 44, 1, 48, 42, 7, 3, 10, 10, 37, 31, 26, 1, 48], [37, 24, 43, 15, 12, 28, 38, 20, 30, 12, 31, 22, 5, 8, 46], [7, 32, 49, 48, 37, 46, 35, 13, 18, 31, 4, 11, 44, 45, 3], [11, 49, 21, 12, 23, 13, 49, 14, 48, 32, 3, 40, 29, 43, 6]]
    n = 15
    police = 12

    positions = [[0 for x in range(n)] for y in range(n)]
    x_str = "x"*len(positions)
    current_state = CityState(city, positions, police, 0, x_str)
    max_score = find_solution(current_state)
    #end = time.time()
    #print("Time is - {}".format(end-start))
    write_output(max_score)
