#!/usr/bin/env python
import math


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


def num_visibile_trees_from_outside(grid):
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

    return visible_trees


def num_visible_in_direction(heights, value):
    count = 0
    for height in heights:
        count += 1
        if height >= value:
            # this tree blocks the view
            break
    return count


def calc_scenic_score(grid, point):
    """
    This is quite slow at the moment. Two small optimisations are:

    * scenic score for points on edge of grid is zero
    * if num_visible_in_direction is 0 in any direction, no point
      calculating it for the other directions

    A faster approach could be to loop through the columns and calc
    num_visible_north using:

        num_visible_north[(x,y)] = (
            1 if grid[(x, y-1)] < grid[(x, y)]
            else num_visible_north[(x,y-1)] +1

    Then repeat for the other three directions.
    """
    x, y = point
    height = grid[point]
    width = max(i for (i, j) in grid) + 1
    length = max(j for (i, j) in grid) + 1

    north_heights = (grid[(x, y - i)] for i in range(1, y + 1))
    south_heights = (grid[(x, y + i)] for i in range(1, length - y))
    east_heights = (grid[(x - i, y)] for i in range(1, x + 1))
    west_heights = (grid[(x + i, y)] for i in range(1, width - x))
    return math.prod(
        [
            num_visible_in_direction(heights, height)
            for heights in [north_heights, south_heights, east_heights, west_heights]
        ]
    )


def main():
    lines = read_input()
    grid = make_grid(lines)

    part_1 = len(num_visibile_trees_from_outside(grid))
    print(f"{part_1=}")

    part_2 = max(calc_scenic_score(grid, point) for point in grid)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day08.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
