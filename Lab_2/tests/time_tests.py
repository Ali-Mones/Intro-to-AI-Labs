from gen_tests import read_tests, get_col_index
import sys
sys.path.append("./")
from minimax import *
import time


def time_nodes_test(tests: list[list[list[int]]], count: int, depth: int) -> tuple[float, float, float, float]:
    t_total = 0
    t_ab_total = 0
    nodes_total = 0
    nodes_ab_total = 0
    for i in range(count):
        board = tests[i]
        col_index = get_col_index(board)

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


def time_nodes_diff_depths_test(tests: list[list[list[int]]], count: int, max_depth: int) -> dict[int, tuple[float, float, float, float]]:
    times: dict[int, tuple[float, float, float, float]] = {}

    for i in range(1, max_depth + 1):
        times[i] = time_nodes_test(tests, count, i)

    return times

def main():
    tests = read_tests()
    count = 100
    max_depth = 8
    print(time_nodes_diff_depths_test(tests, count, max_depth))


if __name__ == "__main__":
    main()