from gen_tests import read_tests, get_col_index
import sys
sys.path.append("./")
from minimax import *
import time


def time_nodes_test(tests: list[list[list[int]]], count: int, depth: int, with_no_pruning: bool) -> tuple[float, float, float, float]:
    t_total = 0
    t_ab_total = 0
    nodes_total = 0
    nodes_ab_total = 0
    for i in range(count):
        board = tests[i]
        col_index = get_col_index(board)

        if with_no_pruning:
            t = time.time_ns()
            _, _, nodes = minimax(board, depth, True, col_index)
            t = time.time_ns() - t
            t_total += t
            nodes_total += nodes

        t = time.time_ns()
        _, _, nodes = minimax_alphabeta(board, depth, True, col_index)
        t = time.time_ns() - t
        t_ab_total += t
        nodes_ab_total += nodes

    return (t_total / count / 1e6, t_ab_total / count / 1e6, nodes_total / count, nodes_ab_total / count)


def time_nodes_diff_depths_test(tests: list[list[list[int]]], count: int, min_depth: int, max_depth: int, with_no_pruning: bool) -> dict[int, tuple[float, float, float, float]]:
    times: dict[int, tuple[float, float, float, float]] = {}

    for i in range(min_depth, max_depth + 1):
        times[i] = time_nodes_test(tests, count, i, with_no_pruning)
        with open("tests/data2.txt", "a") as file:
            file.write(str(times))

    return times

def main():
    tests = read_tests()
    count = 30
    min_depth = 12
    max_depth = 12
    with_no_pruning = False
    print(time_nodes_diff_depths_test(tests, count, min_depth, max_depth, with_no_pruning))


if __name__ == "__main__":
    main()