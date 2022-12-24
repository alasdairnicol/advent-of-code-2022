#!/usr/bin/env python
from collections import defaultdict
import itertools


def parse_grid(lines: list[str]) -> dict:
    grid = defaultdict(list)
    for j, row in enumerate(lines):
        for i, val in enumerate(row):
            if val != ".":
                grid[(i, j)].append(val)
    return grid


def get_val(grid: dict, x: int, y: int) -> str:
    val = grid.get((x, y), ["."])
    return str(len(val)) if len(val) > 1 else val[0]


def print_grid(grid: dict) -> None:
    xs = {x for (x, y) in grid}
    ys = {y for (x, y) in grid}
    print()
    for y in range(min(ys), max(ys) + 1):
        print("".join(get_val(grid, x, y) for x in range(min(xs), max(xs) + 1)))


def next_grid(grid: dict, width: int, height: int) -> dict:
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


def chart_path(grid: dict, width: int, height: int, path: list[tuple[int, int]]):
    time_taken = 0
    for start, destination in itertools.pairwise(path):
        reachable = {start}
        while destination not in reachable:
            grid = next_grid(grid, width, height)
            new_reachable = {start}
            for (x, y) in reachable:
                for (i, j) in [(0, 0), (0, -1), (1, 0), (0, 1), (-1, 0)]:
                    x_new, y_new = (x + i, y + j)
                    if (x_new, y_new) not in grid and (
                        (1 <= x_new < width and 1 <= y_new < height)
                        or (x_new, y_new) in {start, destination}
                    ):
                        new_reachable.add((x_new, y_new))

            reachable = new_reachable
            time_taken += 1

    return time_taken


def main():
    lines = read_input()
    grid = parse_grid(lines)

    # Calc dimensions of grid
    xs = {x for (x, y) in grid}
    ys = {y for (x, y) in grid}
    width = max(xs)
    height = max(ys)

    start = (1, 0)
    destination = (width - 1, height)

    part_1 = chart_path(grid, width, height, [start, destination])
    print(f"{part_1=}")

    part_2 = chart_path(grid, width, height, [start, destination, start, destination])
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day24.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
