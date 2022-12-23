#!/usr/bin/env python

example_board = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#."""

example_moves = "10R5L5R10L4R5L5"


def parse_moves(moves_str):
    digits = ""
    for char in moves_str:
        if char.isdigit():
            digits += char
        else:
            if digits:
                yield int(digits)
                digits = ""
            yield char
    if digits:
        yield int(digits)


def parse_board(board_str):
    board = {}
    for j, row in enumerate(board_str.split("\n")):
        for i, val in enumerate(row):
            if val != " ":
                board[(i, j)] = val
    return board


directions = {
    (1, 0): ">",
    (0, 1): "v",
    (-1, 0): "<",
    (0, -1): "^",
}


def row(board, j):
    row = [(x, y) for (x, y) in board if y == j]
    row.sort(key=lambda b: b[0])
    return row


def column(board, i):
    column = [(x, y) for (x, y) in board if x == i]
    column.sort(key=lambda b: b[1])
    return column


def print_board(board):
    xs = {x for (x, y) in board}
    ys = {y for (x, y) in board}

    for y in range(min(ys), max(ys) + 1):
        print("".join(board.get((x, y), " ") for x in range(min(xs), max(xs) + 1)))


def wrap_flat(board, position, next_position, direction):
    if next_position not in board:
        # wrap around
        if direction == (1, 0):
            next_position = row(board, position[1])[0]
        elif direction == (0, 1):
            next_position = column(board, position[0])[0]
        elif direction == (-1, 0):
            next_position = row(board, position[1])[-1]
        elif direction == (0, -1):
            next_position = column(board, position[0])[-1]

    return next_position




def plot_path(board, moves, wrap_function):
    position = row(board, 0)[0]
    direction = (1, 0)

    for move in moves:
        if move == "R":
            direction = (-direction[1], direction[0])
        elif move == "L":
            direction = (direction[1], -direction[0])
        else:
            for _ in range(move):
                next_position = (position[0] + direction[0], position[1] + direction[1])

                if next_position not in board:
                    next_position = wrap_function(board, position, next_position, direction)

                if board[next_position] == "#":
                    # hit wall
                    break
                else:
                    board[position] = directions[direction]
                    position = next_position

    return position, direction


"""
R (1,0)    rotate_right: (-y, x)
D (0,1)    rorate_left: (y, -x)
L (-1,0)
U (0,-1)
"""


def main():
    board_str, moves_str = read_input()

    # board_str = example_board
    # moves_str = example_moves

    moves = list(parse_moves(moves_str))
    board = parse_board(board_str)

    (x, y), direction = plot_path(board, moves, wrap_flat)
    score = 1000 * (y + 1) + 4 * (x + 1) + list(directions).index(direction)
    print(x, y, direction)
    print(score)

    # print_board(board)


def read_input() -> list[str]:
    with open("day22.txt") as f:
        return f.read().rstrip().split("\n\n")


if __name__ == "__main__":
    main()
