#!/usr/bin/env python
from typing import Generator

Point = tuple[int, int, int]


def parse_line(line) -> Point:
    x, y, z = (int(x) for x in line.split(","))
    return (x, y, z)


def neighbours(point: Point) -> Generator[Point, None, None]:
    x, y, z = point
    yield (x + 1, y, z)
    yield (x - 1, y, z)
    yield (x, y + 1, z)
    yield (x, y - 1, z)
    yield (x, y, z + 1)
    yield (x, y, z - 1)


def do_part_1(lava: set[Point]) -> int:
    return 6 * len(lava) - sum(
        sum(1 if neighbour in lava else 0 for neighbour in neighbours(point))
        for point in lava
    )


def do_part_2(lava: set[Point]) -> int:
    min_x = min(x for (x, y, z) in lava)
    max_x = max(x for (x, y, z) in lava)

    min_y = min(y for (x, y, z) in lava)
    max_y = max(y for (x, y, z) in lava)

    min_z = min(z for (x, y, z) in lava)
    max_z = max(z for (x, y, z) in lava)

    surface_count = 0

    # Find the points that water can reach
    water = set()
    water_start = (min_x - 1, min_y - 1, min_z - 1)
    remaining = {water_start}

    while remaining:
        (x, y, z) = remaining.pop()
        water.add((x, y, z))
        for nx, ny, nz in neighbours((x, y, z)):

            if any(
                [
                    nx < min_x - 1,
                    nx > max_x + 1,
                    ny < min_y - 1,
                    ny > max_y + 1,
                    nz < min_z - 1,
                    nz > max_z + 1,
                ]
            ):
                # We've reached the edge
                pass
            elif (nx, ny, nz) in lava:
                # Found lava
                surface_count += 1
            else:
                if (nx, ny, nz) not in water:
                    remaining.add((nx, ny, nz))

    return surface_count


def main():
    lines = read_input()
    lava = {parse_line(line) for line in lines}

    part_1 = do_part_1(lava)
    print(f"{part_1=}")

    part_2 = do_part_2(lava)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day18.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
