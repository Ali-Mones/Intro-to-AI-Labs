import time

import sys
sys.path.insert(1, 'Lab_1/8 Game/')

import ai_algorithms as ai

def testcase(index, solvable):
    if solvable:
        filepath = "Lab_1/8 Game/solvable.txt"
    else:
        filepath = "Lab_1/8 Game/unsolvable.txt"

    with open(filepath) as file:
        file_str = file.read()
        available_states = file_str.split("\n")

        # get random test case
        init_state = available_states[index]

    print(init_state)
    print("")
    test_algorithm(init_state, solvable, ai.DFS)
    test_algorithm(init_state, solvable, ai.BFS)
    test_algorithm(init_state, solvable, ai.AStarEuclidean)
    test_algorithm(init_state, solvable, ai.AStarManhattan)

def test_algorithm(init_state, solvable, function):
    t = time.time_ns()
    solved, parent_map, explored, depth, nodes_expanded = function(init_state)
    t = time.time_ns() - t

    if solvable:
        path = ai.get_path(parent_map)
    print(f"------------------{str(function).split(' ')[1]}------------------")
    print(f"time = {t / 1e6} ms")
    # print(f"path = {path}")
    solvable and print(f"path = {path}")
    solvable and print(f"path length = {len(path)}")
    print(f"number of nodes expanded = {nodes_expanded}")
    print("---------------------------------------")
    print("")

# testcase(100, True)
# testcase(900, True)
testcase(100, False)
testcase(900, False)