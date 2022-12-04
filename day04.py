#!/usr/bin/env python

Section = tuple[int, int]
Pair = tuple[Section, Section]


def do_part_1(pairs: list[Pair]) -> int:
    fully_contained_pairs = [
        pair for pair in pairs if is_fully_contained(pair[0], pair[1])
    ]
    return len(fully_contained_pairs)


def do_part_2(pairs: list[Pair]) -> int:
    overlapping_pairs = [pair for pair in pairs if has_overlap(pair[0], pair[1])]
    return len(overlapping_pairs)


def parse_range(range_str: str) -> tuple[int, int]:
    x, y = range_str.split(",")
    return int(x), int(y)


def parse_line(line: str) -> tuple[Section, Section]:
    p1, p2 = (parse_range(p) for p in line.split(","))
    return p1, p2


def is_fully_contained(x: Section, y: Section) -> bool:
    return (x[0] >= y[0] and x[1] <= y[1]) or (y[0] >= x[0] and y[1] <= x[1])


def has_overlap(x: Section, y: Section) -> bool:
    return (y[0] <= x[0] <= y[1] or y[0] <= x[1] <= y[1]) or (
        x[0] <= y[0] <= x[1] or x[0] <= y[1] <= x[1]
    )


def main():
    lines = read_input()
    pairs = [parse_line(line) for line in lines]

    part_1 = do_part_1(pairs)
    print(f"{part_1=}")

    part_2 = do_part_2(pairs)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day04.txt") as f:
        return f.read().strip().split("\n")


if __name__ == "__main__":
    main()
