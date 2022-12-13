#!/usr/bin/env python
from dataclasses import dataclass


@dataclass
class Grid:
    heights: dict
    start: int
    end: int

    @classmethod
    def from_lines(cls, lines):
        heights = {}
        for j, line in enumerate(lines):
            for i, letter in enumerate(line):
                if letter == "S":
                    start = (i, j)
                    letter = "a"
                elif letter == "E":
                    end = (i, j)
                    letter = "z"
                # use integer for height to make comparisons easier
                height = ord(letter) - ord("a")
                heights[(i, j)] = height
        return Grid(heights, start, end)

    def neighbours(self, point, ignore_a_neighbours):
        x, y = point
        current_height = self.heights[point]
        for i, j in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_point = (x + i, y + j)
            if self.heights.get(new_point, 100) - current_height <= 1:
                if ignore_a_neighbours and self.heights[new_point] == 0:
                    # No point considering a route that visits another 'a' for part 2
                    pass
                else:
                    yield new_point

    def solve(self, starting_point, ignore_a_neighbours=False):
        queue = [starting_point]
        num_steps_dict = {starting_point: 0}
        while self.end not in num_steps_dict and queue:
            point = queue.pop(0)
            num_steps = num_steps_dict[point] + 1
            for neighbour in self.neighbours(
                point, ignore_a_neighbours=ignore_a_neighbours
            ):
                if neighbour not in num_steps_dict:
                    num_steps_dict[neighbour] = num_steps
                    queue.append(neighbour)

        return num_steps_dict.get(self.end)


def do_part_2(grid):
    starting_points = [point for point, height in grid.heights.items() if height == 0]
    steps = (grid.solve(point, ignore_a_neighbours=True) for point in starting_points)
    return min(s for s in steps if s is not None)


def main():
    lines = read_input()
    grid = Grid.from_lines(lines)

    part_1 = grid.solve(grid.start)
    print(f"{part_1=}")

    part_2 = do_part_2(grid)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day12.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
