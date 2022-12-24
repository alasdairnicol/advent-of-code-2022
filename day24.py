#!/usr/bin/env python
from collections import defaultdict

example_lines = """\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#""".split(
    "\n"
)


def parse_grid(lines):
    grid = defaultdict(list)
    for j, row in enumerate(lines):
        for i, val in enumerate(row):
            if val != ".":
                grid[(i, j)].append(val)
    return grid


def get_val(grid, x, y):
    val = grid.get((x, y), ["."])
    return str(len(val)) if len(val) > 1 else val[0]


def print_grid(grid):
    xs = {x for (x, y) in grid}
    ys = {y for (x, y) in grid}

    for y in range(min(ys), max(ys) + 1):
        print("".join(get_val(grid, x, y) for x in range(min(xs), max(xs) + 1)))
    print()


def next_grid(grid, width, height):
    # FIXME wrap wrap wrap!
    new = defaultdict(list)
    for (x, y), values in grid.items():
        for value in values:
            if value == "#":
                new[(x, y)].append(value)
            elif value == "^":
                new_y = y - 1 if y > 1 else height - 1
                new[(x, new_y)].append(value)
            elif value == ">":
                new_x = x + 1 if x < width - 1 else 1
                new[(new_x, y)].append(value)
            elif value == "v":
                new_y = y + 1 if y < height - 1 else 1
                new[(x, new_y)].append(value)
            elif value == "<":
                new_x = x - 1 if x > 1 else width - 1
                new[(new_x, y)].append(value)
            else:
                raise ValueError(f"Unknown value {value}")
    return new


def main():
    lines = read_input()
    lines = example_lines
    grid = parse_grid(lines)
    minute = 0
    print(f"Minute {minute}")
    print_grid(grid)

    xs = {x for (x, y) in grid}
    ys = {y for (x, y) in grid}
    start_column = set(grid.get((1, y), ["."])[0] for y in range(min(ys), max(ys) + 1))
    end_column = set(
        grid.get((max(xs) - 1, y), ["."])[0] for y in range(min(ys), max(ys) + 1)
    )
    width = max(xs)
    height = max(ys)
    assert {"^", "v"} & (start_column | end_column) == set()

    for minute in range(1, 19):
        grid = next_grid(grid, width, height)
        print(f"Minute {minute}")
        print_grid(grid)
    # Check there are not blizzards moving up/down in the start/end columns
    # This means we don't have to worry about blizzards hitting the start/end
    # points

    # part_1 = count_empty_tiles(grid)
    # print(f"{part_1=}")


def read_input() -> list[str]:
    with open("day24.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
