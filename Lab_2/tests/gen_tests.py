import random as r

PLAYER_NO = 0
AI_NO = 1


def gen_test_case() -> list[list[int]]:
    case = [[2 for _ in range(7)] for _ in range(6)]
    min_index = [0 for _ in range(7)]
    move_count = r.randint(0, 19)

    for _ in range(move_count):
        column = r.randint(0, 6)
        while min_index[column] == 6:
            column = r.randint(0, 6)
        case[5 - min_index[column]][column] = PLAYER_NO
        min_index[column] += 1

        column = r.randint(0, 6)
        while min_index[column] == 6:
            column = r.randint(0, 6)
        if min_index[column] != 0:
            case[5 - min_index[column]][column] = AI_NO
            min_index[column] += 1

    return case


def gen_test_cases(count: int) -> list[list[list[int]]]:
    cases = []
    for _ in range(count):
        cases.append(gen_test_case())
    return cases


def write_tests(tests: list[list[list[int]]]):
    with open("tests/test_cases.txt", "w") as file:
        file.write(str(tests))


def read_tests() -> list[list[list[int]]]:
    with open("tests/test_cases.txt", "r") as file:
        string = file.read()
    return eval(string)


def get_col_index(board: list[list[int]]):
    col_index = [0 for _ in range(len(board[0]))]
    for col in range(len(board[0])):
        row = 0
        while row < len(board) and board[row][col] == 2:
            row += 1
        col_index[col] = 6 - row

    return col_index


def main():
    test_cases = gen_test_cases(10000)
    write_tests(test_cases)


if __name__ == "__main__":
    main()
