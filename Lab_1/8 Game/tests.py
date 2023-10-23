import unittest
import random
import ai_algorithms as ai
import time

import unittest

class WidgetTestCase(unittest.TestCase):

    def setup(self):
        charset = '_12345678'
        self.init_state = ''
        while len(self.init_state) != 9:
            c = random.choice(charset)
            if c not in self.init_state:
                self.init_state += c

    def test_dfs(self):
        self.setup()
        t = time.time_ns()
        x = ai.BFS(self.init_state)
        t = time.time_ns() - t
        print(t / 1e9)

        if x == None:
            print('no answer')
            return

        if '_12345678' in x:
            print(len(x))
        else:
            print('couldnt reach answer')


if __name__ == '__main__':
    unittest.main()