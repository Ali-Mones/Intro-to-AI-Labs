import unittest
import random
import ai_algorithms as ai
import time
import threading


class DataTestCase(unittest.TestCase):
    def setUp(self):
        with open("Lab_1/8 Game/solvable.txt") as file:
            file_str = file.read()
            self.init_states = file_str.split("\n")
            print(f"read {len(self.init_states)} lines")

    def get_path_length(self, parent: dict[str, str]):
        state = "_12345678"
        size = 0
        while parent[state] != state:
            state = parent[state]
            size += 1

        return size

    def algorithm_wrapper(self, init_state, fun, result_list):
        t = time.thread_time_ns()
        result = fun(init_state)
        t = time.thread_time_ns() - t
        result_list.append(result)
        result_list.append(t / 1e6)

    def test_data(self):
        total_times = [0, 0, 0, 0]
        total_path_lengths = [0, 0, 0, 0]
        total_nodes_expanded = [0, 0, 0, 0]
        total_depths = [0, 0, 0, 0]
        total_times = [0, 0, 0, 0]

        iterations = 1000

        for i in range(iterations):
            print(f"iteration {i}")
            state = self.init_states[i]
            dfs = []
            bfs = []
            euclidean = []
            manhattan = []

            dfs_thread = threading.Thread(
                target=self.algorithm_wrapper, args=[state, ai.DFS, dfs]
            )
            bfs_thread = threading.Thread(
                target=self.algorithm_wrapper, args=[state, ai.BFS, bfs]
            )
            euclidean_thread = threading.Thread(
                target=self.algorithm_wrapper,
                args=[state, ai.AStarEuclidean, euclidean],
            )
            manhattan_thread = threading.Thread(
                target=self.algorithm_wrapper,
                args=[state, ai.AStarManhattan, manhattan],
            )

            dfs_thread.start()
            bfs_thread.start()
            euclidean_thread.start()
            manhattan_thread.start()

            dfs_thread.join()
            bfs_thread.join()
            euclidean_thread.join()
            manhattan_thread.join()

            total_times[0] += dfs[1]
            total_times[1] += bfs[1]
            total_times[2] += euclidean[1]
            total_times[3] += manhattan[1]

            total_path_lengths[0] += self.get_path_length(dfs[0][1])
            total_path_lengths[1] += self.get_path_length(bfs[0][1])
            total_path_lengths[2] += self.get_path_length(euclidean[0][1])
            total_path_lengths[3] += self.get_path_length(manhattan[0][1])

            total_depths[0] += dfs[0][3]
            total_depths[1] += bfs[0][3]
            total_depths[2] += euclidean[0][3]
            total_depths[3] += manhattan[0][3]

            total_nodes_expanded[0] += dfs[0][4]
            total_nodes_expanded[1] += bfs[0][4]
            total_nodes_expanded[2] += euclidean[0][4]
            total_nodes_expanded[3] += manhattan[0][4]

        print("time: ")
        for time in total_times:
            print("    " + str(time / iterations))
        print("----------------")

        print("path_lengths: ")
        for path_length in total_path_lengths:
            print("    " + str(path_length / iterations))
        print("----------------")

        print("depths: ")
        for depth in total_depths:
            print("    " + str(depth / iterations))
        print("----------------")

        print("nodes_expanded: ")
        for nodes_expanded in total_nodes_expanded:
            print("    " + str(nodes_expanded / iterations))
        print("----------------")


def get_state(states_lock, init_states):
    charset = "_12345678"

    for _ in range(10):
        state = ""
        while len(state) != 9:
            c = random.choice(charset)
            if c not in state:
                state += c
        if ai.BFS(state)[0] == False:
            states_lock.acquire()
            if state not in init_states:
                init_states.append(state)
            states_lock.release()


def get_states():
    init_states: list[str] = []

    with open("Lab_1/8 Game/unsolvable.txt", "r") as file:
        state = file.read()
        read_states = state.split("\n")
        print(f"read {len(read_states)} lines")

    init_states = read_states

    states_lock = threading.Lock()
    threads = [
        threading.Thread(target=get_state, args=[states_lock, init_states])
        for _ in range(4)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    with open("Lab_1/8 Game/unsolvable.txt", "w") as file:
        print(f"writing {len(init_states)} lines")
        for state in init_states:
            file.write(state)
            file.write("\n")


if __name__ == "__main__":
    unittest.main()
    # get_states()
