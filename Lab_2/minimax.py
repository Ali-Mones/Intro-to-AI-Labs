import math
from typing import overload
from tree_drawer import TreeDrawer

HUMAN = 0
AI = 1
EMPTY = 2
HEIGHT, WIDTH = 6, 7
m: dict[str, float] = {}
hoz_hue = [1, 2, 3, 4, 3, 2, 1]
ver_hue = [1, 2, 3, 3, 2, 1]
diag_hue = [
    [0, 0, 0, 1, 1, 1, 1],
    [0, 0, 1, 2, 2, 2, 1],
    [0, 1, 2, 3, 3, 2, 1],
    [1, 2, 3, 3, 2, 1, 0],
    [1, 2, 2, 2, 1, 0, 0],
    [1, 1, 1, 1, 0, 0, 0],
]


def detect_winner(board):
    for c in range(WIDTH - 3):
        for r in range(HEIGHT):
            if (
                board[r][c] != EMPTY
                and board[r][c] == board[r][c + 1]
                and board[r][c] == board[r][c + 2]
                and board[r][c] == board[r][c + 3]
            ):
                return board[r][c]

    for c in range(WIDTH):
        for r in range(HEIGHT - 3):
            if (
                board[r][c] != EMPTY
                and board[r][c] == board[r + 1][c]
                and board[r][c] == board[r + 2][c]
                and board[r][c] == board[r + 3][c]
            ):
                return board[r][c]

    for c in range(WIDTH - 3):
        for r in range(HEIGHT - 3):
            if (
                board[r][c] != EMPTY
                and board[r][c] == board[r + 1][c + 1]
                and board[r][c] == board[r + 2][c + 2]
                and board[r][c] == board[r + 3][c + 3]
            ):
                return board[r][c]

    # Check negatively sloped diaganols
    for c in range(WIDTH - 3):
        for r in range(3, HEIGHT):
            if (
                board[r][c] != EMPTY
                and board[r][c] == board[r - 1][c + 1]
                and board[r][c] == board[r - 2][c + 2]
                and board[r][c] == board[r - 3][c + 3]
            ):
                return board[r][c]
    return EMPTY


def evaluate_group(group):
    ai_cnt = 0
    human_cnt = 0
    empty_cnt = 0
    for g in group:
        if g == AI:
            ai_cnt += 1
        elif g == HUMAN:
            human_cnt += 1
        else:
            empty_cnt += 1
    if ai_cnt > 0 and human_cnt > 0:
        # no one can win
        return 0
    if ai_cnt > 0:
        if ai_cnt == 1:
            return 1
        if ai_cnt == 2:
            return 4
        if ai_cnt == 3:
            return 10
        if ai_cnt == 4:
            return 80
    if human_cnt == 1:
        return -1
    if human_cnt == 2:
        return -4
    if human_cnt == 3:
        return -10
    if human_cnt == 4:
        return -80
    return 0


def hueristic(board):
    score = 0
    # horizontal
    for c in range(WIDTH - 3):
        for r in range(HEIGHT):
            group = [board[r][c], board[r][c + 1], board[r][c + 2], board[r][c + 3]]
            score += evaluate_group(group)

    for c in range(WIDTH):
        for r in range(HEIGHT - 3):
            group = [board[r][c], board[r + 1][c], board[r + 2][c], board[r + 3][c]]
            score += evaluate_group(group)

    for c in range(WIDTH - 3):
        for r in range(HEIGHT - 3):
            group = [
                board[r][c],
                board[r + 1][c + 1],
                board[r + 2][c + 2],
                board[r + 3][c + 3],
            ]
            score += evaluate_group(group)

    # Check negatively sloped diaganols
    for c in range(WIDTH - 3):
        for r in range(3, HEIGHT):
            group = [
                board[r][c],
                board[r - 1][c + 1],
                board[r - 2][c + 2],
                board[r - 3][c + 3],
            ]
            score += evaluate_group(group)
    return score


def parr(board):
    for row in board:
        print(row)


def get_copy(board):
    c: list[list[int]] = []
    for row in range(HEIGHT):
        c.append([])
        for element in range(WIDTH):
            c[row].append(board[row][element])
    return c


def minimax(
    board: list[list[int]],
    depth,
    maximizing: bool,
    colomn_ind: list[int],
    tree: list[float | None],
):
    state = "2" * 7 * 6
    m.clear()
    state = list(state)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            state[i * WIDTH + j] = chr(board[i][j] + ord("0"))
    print(state)
    return minimax2(board, depth, maximizing, colomn_ind, state, tree, 0)


def minimax_alphabeta(
    board: list[list[int]],
    depth,
    maximizing: bool,
    colomn_ind: list[int],
    tree: list[float | None],
):
    state = "2" * 7 * 6
    m.clear()
    state = list(state)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            state[i * WIDTH + j] = chr(board[i][j] + ord("0"))
    print(state)
    return minimax_alphabeta_impl(
        board, depth, maximizing, colomn_ind, state, -math.inf, math.inf, tree, 0
    )


def minimax2(
    board: list[list[int]],
    depth: int,
    maximizing: bool,
    colomn_ind: list[int],
    state: list[str],
    tree: list[float | None],
    tree_index: int,
) -> tuple[float, int, int]:
    columns = [int(i) for i in range(len(colomn_ind)) if colomn_ind[i] < HEIGHT]
    if not columns:
        print(colomn_ind)
        winner = detect_winner(board)
        if winner == AI:
            tree[tree_index] = math.inf
            return (math.inf, -1, 1)
        elif winner == HUMAN:
            tree[tree_index] = -math.inf
            return (-math.inf, -1, 1)
        else:
            tree[tree_index] = 0
            return (0, -1, 1)

    if depth == 0:
        score = hueristic(board)
        tree[tree_index] = score
        return (score, -1, 1)
    state_str = "".join(state)
    if m.get(state_str):
        return (m[state_str], -1, 1)

    nodes_expanded = 0
    if maximizing:
        value = -math.inf
        move = columns[0]
        for col in columns:
            board[HEIGHT - 1 - colomn_ind[col]][col] = AI
            state[(HEIGHT - 1 - colomn_ind[col]) * WIDTH + col] = chr(AI + ord("0"))
            colomn_ind[col] += 1
            new_value, new_move, nodes = minimax2(
                board,
                depth - 1,
                False,
                colomn_ind,
                state,
                tree,
                tree_index * 7 + 1 + col,
            )
            nodes_expanded += nodes
            colomn_ind[col] -= 1
            board[HEIGHT - 1 - colomn_ind[col]][col] = EMPTY
            state[(HEIGHT - 1 - colomn_ind[col]) * WIDTH + col] = chr(EMPTY + ord("0"))
            if new_value > value:
                value = new_value
                move = col
        m[state_str] = value
        tree[tree_index] = value
        return value, move, nodes_expanded
    else:
        # print(maximizing)
        value = math.inf
        move = columns[0]
        for col in columns:
            board[HEIGHT - 1 - colomn_ind[col]][col] = HUMAN
            state[(HEIGHT - 1 - colomn_ind[col]) * WIDTH + col] = chr(HUMAN + ord("0"))
            colomn_ind[col] += 1

            new_value, new_move, nodes = minimax2(
                board,
                depth - 1,
                True,
                colomn_ind,
                state,
                tree,
                tree_index * 7 + 1 + col,
            )
            nodes_expanded += nodes
            colomn_ind[col] -= 1
            board[HEIGHT - 1 - colomn_ind[col]][col] = EMPTY
            state[(HEIGHT - 1 - colomn_ind[col]) * WIDTH + col] = chr(EMPTY + ord("0"))
            if new_value < value:
                value = new_value
                move = col
        m[state_str] = value
        tree[tree_index] = value
        return value, move, nodes_expanded


def minimax_alphabeta_impl(
    board: list[list[int]],
    depth: int,
    maximizing: bool,
    colomn_ind: list[int],
    state: list[str],
    alpha: float,
    beta: float,
    tree: list[float | None],
    tree_index: int,
) -> tuple[float, int, int]:
    columns = [int(i) for i in range(len(colomn_ind)) if colomn_ind[i] < HEIGHT]
    if not columns:
        print(colomn_ind)
        winner = detect_winner(board)
        if winner == AI:
            tree[tree_index] = math.inf
            return (math.inf, -1, 1)
        elif winner == HUMAN:
            tree[tree_index] = -math.inf
            return (-math.inf, -1, 1)
        else:
            tree[tree_index] = 0
            return (0, -1, 1)

    if depth == 0:
        score = hueristic(board)
        tree[tree_index] = score
        return (score, -1, 1)
    state_str = "".join(state)

    if m.get(state_str):
        return (m[state_str], -1, 1)
    nodes_expanded = 0

    if maximizing:
        value = -math.inf
        move = columns[0]
        for col in columns:
            board[HEIGHT - 1 - colomn_ind[col]][col] = AI
            state[(HEIGHT - 1 - colomn_ind[col]) * WIDTH + col] = chr(AI + ord("0"))
            colomn_ind[col] += 1
            new_value, new_move, nodes = minimax_alphabeta_impl(
                board,
                depth - 1,
                False,
                colomn_ind,
                state,
                alpha,
                beta,
                tree,
                tree_index * 7 + 1 + col,
            )
            nodes_expanded += nodes
            colomn_ind[col] -= 1
            board[HEIGHT - 1 - colomn_ind[col]][col] = EMPTY
            state[(HEIGHT - 1 - colomn_ind[col]) * WIDTH + col] = chr(EMPTY + ord("0"))
            if new_value > value:
                value = new_value
                move = col
            alpha = max(alpha, new_value)
            if alpha >= beta:
                break
        m[state_str] = value
        tree[tree_index] = value
        return value, move, nodes_expanded
    else:
        value = math.inf
        move = columns[0]
        for col in columns:
            board[HEIGHT - 1 - colomn_ind[col]][col] = HUMAN
            state[(HEIGHT - 1 - colomn_ind[col]) * WIDTH + col] = chr(HUMAN + ord("0"))
            colomn_ind[col] += 1

            new_value, new_move, nodes = minimax_alphabeta_impl(
                board,
                depth - 1,
                True,
                colomn_ind,
                state,
                alpha,
                beta,
                tree,
                tree_index * 7 + 1 + col,
            )
            nodes_expanded += nodes
            colomn_ind[col] -= 1
            board[HEIGHT - 1 - colomn_ind[col]][col] = EMPTY
            state[(HEIGHT - 1 - colomn_ind[col]) * WIDTH + col] = chr(EMPTY + ord("0"))
            if new_value < value:
                value = new_value
                move = col
            beta = min(beta, new_value)
            if alpha >= beta:
                break
        m[state_str] = value
        tree[tree_index] = value
        return value, move, nodes_expanded
