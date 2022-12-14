#!/usr/bin/env python
import itertools

Point = tuple[int, int]


def parse_point(point_str: str) -> Point:
    x, y = point_str.split(",", maxsplit=1)
    return (int(x), int(y))


def draw_line(grid: dict, start: Point, end: Point) -> None:
    if start[0] == end[0]:
        # vertical line
        y_min, y_max = sorted([start[1], end[1]])
        points = {(start[0], y): "#" for y in range(y_min, y_max + 1)}
    else:
        # horizontal line
        x_min, x_max = sorted([start[0], end[0]])
        points = {(x, start[1]): "#" for x in range(x_min, x_max + 1)}
    grid |= points
    return None


def make_grid(lines: list[str]) -> dict:
    grid: dict = {}
    for line in lines:
        points = [parse_point(p) for p in line.split(" -> ")]
        for start, end in itertools.pairwise(points):
            draw_line(grid, start, end)

    return grid


def drop_grain(grid: dict, max_y: int, has_floor, visited) -> None | Point:
    pos = visited[-1]
    while True:
        for next_pos in [
            (pos[0], pos[1] + 1),
            (pos[0] - 1, pos[1] + 1),
            (pos[0] + 1, pos[1] + 1),
        ]:
            if next_pos not in grid:
                if has_floor and next_pos[1] == max_y + 2:
                    # we've hit the floor
                    continue
                elif not has_floor and next_pos[1] == max_y:
                    # it's going to flow out the bottom
                    return None
                else:
                    pos = next_pos
                    visited.append(pos)
                    break
        else:
            # none of the possible moves are free, grain can't move
            return visited.pop()


def do_part_1(grid: dict, max_y: int) -> int:
    start = (500, 0)
    visited = [start]

    while (
        pos := drop_grain(grid, max_y, has_floor=False, visited=visited)
    ) is not None:
        if len(pos) > 100:
            raise
        grid[pos] = "o"

    return count_grains(grid)


def do_part_2_by_dropping_grains(grid: dict, max_y: int) -> int:
    """
    Original appraoch of dropping grains until start position
    is filled
    """
    visited = [(500, 0)]

    while True:
        pos = drop_grain(grid, max_y, has_floor=True, visited=visited)
        grid[pos] = "o"

        if pos == (500, 0):
            break

    return count_grains(grid)


def do_part_2(grid: dict, max_y: int) -> int:
    """
    Faster approach of working from starting position and going
    row by row to the bottom, filling points the row above.
    """
    grid[(500, 0)] = "o"
    points = {(500, 0): "o"}
    for y in range(1, max_y + 2):
        new_points = {}
        for point in points:
            for offset in [-1, 0, 1]:
                new_points[(point[0] + offset, y)] = "o"

        for point in list(new_points):
            if grid.get(point) == "#":
                del new_points[point]
        grid |= new_points
        points = new_points

    return count_grains(grid)


def count_grains(grid: dict) -> int:
    return len([x for x, y in grid.items() if y == "o"])


def main():
    lines = read_input()
    grid = make_grid(lines)
    max_y = max(y for (x, y) in grid if grid[(x, y)] == "#")

    part_1 = do_part_1(grid, max_y)
    print(f"{part_1=}")

    part_2 = do_part_2(grid, max_y)
    # part_2 = do_part_2_by_dropping_grains(grid, max_y)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day14.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
