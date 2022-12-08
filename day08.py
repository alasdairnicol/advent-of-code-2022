#!/usr/bin/env python


def make_grid(lines):
    grid = {}
    for j, line in enumerate(lines):
        for i, x in enumerate(line):
            grid[(i, j)] = int(x)
    return grid


def visible_trees_in_line(grid, points):
    tallest_seen = -1
    visible = set()
    for point in points:
        height = grid[point]
        if height > tallest_seen:
            visible.add(point)
            tallest_seen = height
    return visible


def main():
    lines = read_input()
    grid = make_grid(lines)
    width = max(i for (i, j) in grid) + 1
    length = max(j for (i, j) in grid) + 1

    visible_trees = set()

    for x in range(width):
        line = [(x, y) for y in range(length)]
        visible_trees |= visible_trees_in_line(grid, line)
        visible_trees |= visible_trees_in_line(grid, reversed(line))

    for y in range(length):
        line = [(x, y) for x in range(width)]
        visible_trees |= visible_trees_in_line(grid, line)
        visible_trees |= visible_trees_in_line(grid, reversed(line))

    part_1 = len(visible_trees)
    print(f"{part_1=}")


def read_input() -> list[str]:
    with open("day08.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
