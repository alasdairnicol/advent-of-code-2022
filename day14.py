#!/usr/bin/env python
import itertools


def parse_point(point_str):
    x, y = point_str.split(",", maxsplit=1)
    return (int(x), int(y))


def draw_line(grid, start, end):
    if start[0] == end[0]:
        # vertical line
        y_min, y_max = sorted([start[1], end[1]])
        points = {(start[0], y): "#" for y in range(y_min, y_max + 1)}
    else:
        # horizontal line
        x_min, x_max = sorted([start[0], end[0]])
        points = {(x, start[1]): "#" for x in range(x_min, x_max + 1)}
    grid |= points


def make_grid(lines):
    # lines = """498,4 -> 498,6 -> 496,6
    # 503,4 -> 502,4 -> 502,9 -> 494,9""".split("\n")
    grid = {}
    for line in lines:
        points = [parse_point(p) for p in line.split(" -> ")]
        for start, end in itertools.pairwise(points):
            draw_line(grid, start, end)

    return grid


def drop_grain(grid, has_floor=False):
    max_y = max(y for (x, y) in grid if grid[(x, y)] == "#")
    pos = (500, 0)
    while True:
        for next_pos in [
            (pos[0], pos[1] + 1),
            (pos[0] - 1, pos[1] + 1),
            (pos[0] + 1, pos[1] + 1),
        ]:
            if next_pos not in grid:
                if not has_floor and next_pos[1] == max_y:
                    # it's going to flow out the bottom
                    return None
                else:
                    pos = next_pos
                    if pos[1] == max_y + 1:
                        # we're reached the bottom
                        return pos
                    break
        else:
            # none of the possible moves are free, grain can't move
            return pos


def main():
    lines = read_input()
    grid = make_grid(lines)

    while (pos := drop_grain(grid, has_floor=False)) is not None:
        grid[pos] = "o"

        # print("New grain at", pos)
        # for y in range(10):
        #     print("".join(grid.get((x, y), '.') for x in range(494, 504)))

    part_1 = len([x for x, y in grid.items() if y == "o"])
    print(f"{part_1=}")

    while True:
        pos = drop_grain(grid, has_floor=True)
        grid[pos] = "o"
        if pos == (500, 0):
            break

    part_2 = len([x for x, y in grid.items() if y == "o"])
    print(f"{part_2=}")

    # part_2 = do_part_2(packets)
    # print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day14.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
