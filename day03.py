#!/usr/bin/env python
from collections.abc import Iterable
from functools import reduce


priority = {
    k: v
    for v, k in enumerate("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)
}


def grouper(n: int, iterable: Iterable) -> Iterable:
    """
    Split an iterable into chunks of 3

    e.g. ABCDEFGHI -> ABC, DEF, GHI

    NB Discards elements if len(iterable) is not divisible by n
    """
    return zip(*[iter(iterable)] * n)


def split_line(line):
    return set(line[: len(line) // 2]), set(line[len(line) // 2 :])


def find_duplicate_item(items: Iterable) -> str:
    item_sets = (set(item) for item in items)
    return reduce(lambda a, b: a & b, item_sets).pop()


def do_part_1(lines: list[str]) -> int:
    return sum(priority[find_duplicate_item(split_line(line))] for line in lines)


def do_part_2(lines: list[str]) -> int:
    return sum(priority[find_duplicate_item(items)] for items in grouper(3, lines))


def main():
    lines = read_input()

    part_1 = do_part_1(lines)
    print(f"{part_1=}")

    part_2 = do_part_2(lines)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day03.txt") as f:
        return f.read().strip().split("\n")


if __name__ == "__main__":
    main()
