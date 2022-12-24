#!/usr/bin/env python
from collections import defaultdict

example_lines = """\
.....
..##.
..#..
.....
..##.
.....""".split(
    "\n"
)

example_lines = """\
..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............""".split(
    "\n"
)


def parse_grid(lines):
    grid = set()
    for j, row in enumerate(lines):
        for i, val in enumerate(row):
            if val == "#":
                grid.add((i, j))
    return grid


def count_empty_tiles(grid):
    xs = {x for (x, y) in grid}
    ys = {y for (x, y) in grid}

    area = (max(xs) + 1 - min(xs)) * (max(ys) + 1 - min(ys))
    return area - len(grid)


def print_grid(grid):
    xs = {x for (x, y) in grid}
    ys = {y for (x, y) in grid}

    for y in range(min(ys), max(ys) + 1):
        print(
            "".join("#" if (x, y) in grid else "." for x in range(min(xs), max(xs) + 1))
        )
    print()


def propose_north(grid, x, y):
    if not {(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)} & grid:
        return (x, y - 1)


def propose_south(grid, x, y):
    if not {(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)} & grid:
        return (x, y + 1)


def propose_west(grid, x, y):
    if not {(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)} & grid:
        return (x - 1, y)


def propose_east(grid, x, y):
    if not {(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)} & grid:
        return (x + 1, y)


def do_turn(grid, turn_number):
    proposed_moves = defaultdict(list)

    functions = [propose_north, propose_south, propose_west, propose_east]
    functions = functions[turn_number % 4 :] + functions[: turn_number % 4]

    for (x, y) in grid:
        neighbours = {
            (x + 1, y),
            (x + 1, y + 1),
            (x, y + 1),
            (x - 1, y + 1),
            (x - 1, y),
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
        }
        if not neighbours & grid:
            continue

        for function in functions:
            if proposed := function(grid, x, y):
                proposed_moves[proposed].append((x, y))
                break

    num_changes = 0
    for k, values in proposed_moves.items():
        if len(values) == 1:
            grid.remove(values[0])
            grid.add(k)
            num_changes += 1

    return num_changes


def main():
    lines = read_input()

    grid = parse_grid(lines)

    for x in range(10):
        num_changes = do_turn(grid, x)

    part_1 = count_empty_tiles(grid)
    print(f"{part_1=}")

    while True:
        x += 1
        num_changes = do_turn(grid, x)
        if num_changes == 0:
            break
    part_2 = x + 1

    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day23.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
