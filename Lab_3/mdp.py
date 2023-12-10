class State:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value

    def __eq__(self, __value: object) -> bool:
        return self.row == __value.row and self.col == __value.col
    

class Action:
    def __init__(self, drow, dcol):
        self.drow = drow
        self.dcol = dcol

    
def bellman_equation(states: list[State], actions: list[Action], gamma: float, previous_values: list[float]):
    max_action_values = previous_values.copy()
    for i, state in enumerate(states):
        for action in actions:
            ans: int = 0
            for j, next_state in enumerate(states):
                ans += transition(state, action, next_state) * (reward(state, action, next_state) + gamma * previous_values[j])
            max_action_values[i] = ans if ans > max_action_values[i] else max_action_values[i]

    return max_action_values


def reward(state: State, action, next_state: State):
    return next_state.value


def transition(state: State, action: Action, next_state: State):
    #terminal state
    if state.row == 0 and state.col == 2 or state.row == 0 and state.col == 0:
        return 0

    if state.row + action.drow == next_state.row and state.col + action.dcol == next_state.col:
        return 0.8
    elif state.row - action.dcol == next_state.row and state.col - action.drow == next_state.col \
        or state.row + action.dcol == next_state.row and state.col + action.drow == next_state.col:
        return 0.1
    else:
        return 0


def main():
    r = 3
    actions: list[Action] = [Action(0, 1), Action(0, -1), Action(1, 0), Action(-1, 0)]
    board: list[list[int]] = [
        [r, -1, 10],
        [-1, -1, -1],
        [-1, -1, -1]
    ]

    states: list[State] = [
        State(0, 0, board[0][0]), State(0, 1, board[0][1]), State(0, 2, board[0][2]),
        State(1, 0, board[1][0]), State(1, 1, board[1][1]), State(1, 2, board[1][2]),
        State(2, 0, board[2][0]), State(2, 1, board[2][1]), State(2, 2, board[2][2])
    ]

    previous_values: list[float] = [0 for _ in range(len(states))]

    abs_error_limit = 0.00001
    abs_errors = [1 for _ in range(len(states))]
    while max(abs_errors) > abs_error_limit:
        new_values = bellman_equation(states, actions, 0.99, previous_values)

        for i in range(len(states)):
            abs_errors[i] = abs(new_values[i] - previous_values[i])

        previous_values = new_values
        print(previous_values)


if __name__ == "__main__":
    main()