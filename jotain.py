import time
import cProfile
from itertools import groupby

def getpoints(array):
    def check_adjacent(lst):
        lengths = []
        count = 1
        prev_element = lst[0]

        for current_element in lst[1:]:
            if current_element == prev_element:
                count += 1
            else:
                if count >= 3:
                    lengths.append(count)
                count = 1

            prev_element = current_element

        if count >= 3:
            lengths.append(count)

        return lengths

    def transpose(matrix):
        return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

    def calculatepoints(starlevel):
        '''
        Scoring is based on https://yppedia.puzzlepirates.com/Bilge_scoring
        Length 3 = 3 points
        Length 4 = 5 points
        Length 5 = 7 points
        NxN (double): 2 times
        NxNxN (bingo): 3 times
        Sea Donkey: At least 4 times, possibly 5 times.
        Vegas: At least 5 times, possibly 6 or 7 times.
        '''
        # TODO: scale points calculation based on star level
        # Lower star level means less points per combo

        lines = rows_lengths + columns_lengths
        basepoints = 0
        multiplier = len(lines)

        if multiplier == 4:
            multiplier = 4.5
            if 5 in lines:
                multiplier = 6

        for line in lines:
            if line == 3:
                basepoints += 3
            elif line == 4:
                basepoints += 5
            elif line == 5:
                basepoints += 7

        points = basepoints*multiplier
        return points

    rows_lengths = [length for row in array for length in check_adjacent(row)]
    columns_lengths = [length for column in transpose(array) for length in check_adjacent(column)]

    return calculatepoints(0)

def comparemoves(move1, move2):
    m1_score = move1[0]
    m2_score = move2[0]
    m1 = move1[0]/( len(move1) - 1 )
    m2 = move2[0]/( len(move2) - 1 )
    if m1_score == m2_score:
        return move1 if len(move1) < len(move2) else move2
    return move1 if m1_score > m2_score else move2

def checkpuffer(array):
    for y in range(12):
        for x in range(6):
            if array[y][x] == 69:
                return (x,y)
    return (-1,-1)

def getbestmove(array, iterations):
    # if a move set above this score is found, immediately stop calculating
    # treshold of 45 means AT LEAST 15 points per move
    treshold_score = 666

    def swap(listxy):
        x, y = listxy
        copy_of_array = [row[:] for row in array]
        copy_of_array[y][x], copy_of_array[y][x+1] = copy_of_array[y][x+1], copy_of_array[y][x]
        return copy_of_array


    moves: list[int|list[int]] = []

    crab_present = any(70 in row for row in array)

    for y in range(len(array)):
        for x in range(len(array[y]) - 1):
            if (not crab_present) or (array[y][x] != 70 and array[y][x+1] != 70):  # Check for Crab move only if Crab is on screen
                result_array = swap([x, y])
                points = getpoints(result_array)
                move = [points, [x, y]]
                moves.append(move)

    if iterations > 0:
        for i in range(len(moves)-1, 0, -1):
            if moves[i][0] == 0:
                array_new = swap(moves[i][1])
                best_new = getbestmove(array_new, iterations-1)
                moves[i][0] = best_new[0]
                for x in range(1,len(best_new)):
                    moves[i].append(best_new[x])
                if best_new[0] >= treshold_score:
                    return moves[i]

    best = [0,[0, 0]]
    for move in moves:
        best = comparemoves(best, move)

    return best


example_array = [
  [3, 4, 5, 2, 1, 3],
  [2, 1, 3, 5, 4, 1],
  [4, 3, 4, 3, 2, 4],
  [1, 5, 4, 2, 5, 2],
  [4, 4, 2, 4, 2, 2],
  [3, 5, 4, 1, 2, 3],
  [1, 4, 3, 2, 5, 2],
  [4, 5, 1, 1, 3, 5],
  [2, 3, 4, 5, 1, 3],
  [5, 1, 2, 3, 4, 1],
  [2, 3, 1, 5, 4, 3],
  [1, 5, 4, 3, 2, 1]
]




if __name__ == "__main__":
    cProfile.run('getbestmove(example_array, 2)')
    start_time = time.time()

    bestmove = getbestmove(example_array, 2)
    print("Best move gives score:",bestmove[0])
    print("Swaps to make:")
    for i in range(1,len(bestmove)):
        print(f"{bestmove[i]}")

    end_time = time.time()
    runtime = end_time-start_time
    print(f"Runtime is {runtime:.4f} seconds")
