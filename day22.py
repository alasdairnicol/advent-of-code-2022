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

    return next_position, direction


def wrap_cube(board, position, next_position, direction):
    """
    Hardcode wrapping for my specific cube:

    .BA
    .C.
    ED.
    F..
    """
    xs = {x for (x, y) in board}
    width = max(xs) - min(xs) + 1
    face_length = (width) // 3

    if direction == (1, 0):
        if 0 <= next_position[1] < face_length:
            # Face A -> DE reversed
            next_direction = (-1, 0)
            x = 2 * face_length - 1
            y = 3 * face_length - 1 - (next_position[1] % face_length)
            next_position = (x, y)
        elif face_length <= next_position[1] < 2 * face_length:
            # Face C -> AS
            next_direction = (0, -1)
            x = 2 * face_length + (next_position[1] % face_length)
            y = face_length - 1
            next_position = (x, y)
        elif 2 * face_length <= next_position[1] < 3 * face_length:
            # Face D -> AE reversed
            next_direction = (-1, 0)
            x = 3 * face_length - 1
            y = face_length - 1 - (next_position[1] % face_length)
            next_position = (x, y)
        elif 3 * face_length <= next_position[1] < 4 * face_length:
            # Face F -> DS
            next_direction = (0, -1)
            x = face_length + (next_position[1] % face_length)
            y = 3 * face_length - 1
            next_position = (x, y)
    elif direction == (0, 1):
        if 0 <= next_position[0] < face_length:
            # Face F -> AN
            next_direction = (0, 1)
            x = 2 * face_length + next_position[0]
            y = 0
            next_position = (x, y)
        elif face_length <= next_position[0] < 2 * face_length:
            # Face D -> FE
            next_direction = (-1, 0)
            x = face_length - 1
            y = 3 * face_length + (next_position[0] % face_length)
            next_position = (x, y)
        elif 2 * face_length <= next_position[0] < 3 * face_length:
            # Face A -> CE
            next_direction = (-1, 0)
            x = 2 * face_length - 1
            y = face_length + (next_position[0] % face_length)
            next_position = (x, y)
    elif direction == (-1, 0):
        if 0 <= next_position[1] < face_length:
            # Face B -> EW reversed
            next_direction = (1, 0)
            x = 0
            y = 3 * face_length - 1 - next_position[1]
            next_position = (x, y)
        elif face_length <= next_position[1] < 2 * face_length:
            # Face C -> EN
            next_direction = (0, 1)
            x = next_position[1] % face_length
            y = 2 * face_length
            next_position = (x, y)
        elif 2 * face_length <= next_position[1] < 3 * face_length:
            # Face E -> BW reversed
            next_direction = (1, 0)
            x = face_length
            y = face_length - 1 - (next_position[1] % face_length)
            next_position = (x, y)
        elif 3 * face_length <= next_position[1] < 4 * face_length:
            # Face F -> BN
            next_direction = (0, 1)
            x = face_length + (next_position[1] % face_length)
            y = 0
            next_position = (x, y)
    if direction == (0, -1):
        if 0 <= next_position[0] < face_length:
            # Face E -> CW
            next_direction = (1, 0)
            x = face_length
            y = face_length + next_position[0]
            next_position = (x, y)
        elif face_length <= next_position[0] < 2 * face_length:
            # Face B -> FW
            next_direction = (1, 0)
            x = 0
            y = 3 * face_length + (next_position[0] % face_length)
            next_position = (x, y)
        elif 2 * face_length <= next_position[0] < 3 * face_length:
            # Face A -> FS
            next_direction = (0, -1)
            x = next_position[0] % face_length
            y = 4 * face_length - 1
            next_position = (x, y)

    return next_position, next_direction


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
                next_direction = direction

                if next_position not in board:
                    next_position, next_direction = wrap_function(
                        board, position, next_position, direction
                    )

                if board[next_position] == "#":
                    # hit wall
                    break
                else:
                    board[position] = directions[direction]
                    position = next_position
                    direction = next_direction

    return position, direction


"""
R (1,0)    rotate_right: (-y, x)
D (0,1)    rorate_left: (y, -x)
L (-1,0)
U (0,-1)
"""


def score(x, y, direction):
    return 1000 * (y + 1) + 4 * (x + 1) + list(directions).index(direction)


def main():
    board_str, moves_str = read_input()

    moves = list(parse_moves(moves_str))
    board = parse_board(board_str)

    (x, y), direction = plot_path(board.copy(), moves, wrap_flat)
    part_1 = score(x, y, direction)
    print(f"{part_1=}")

    (x, y), direction = plot_path(board.copy(), moves, wrap_cube)
    part_2 = score(x, y, direction)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day22.txt") as f:
        return f.read().rstrip().split("\n\n")


if __name__ == "__main__":
    main()
