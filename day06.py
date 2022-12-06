#!/usr/bin/env python
import itertools
from typing import Iterable


def find_start(datastream: Iterable, num_unique_chars: int) -> int:
    iters = itertools.tee(datastream, num_unique_chars)
    for i, x in enumerate(iters):
        for j in range(i):
            next(x)

    start = next(
        i
        for (i, window) in enumerate(zip(*iters), num_unique_chars)
        if len(set(window)) == num_unique_chars
    )
    return start


def main():
    datastream = read_input()
    part_1 = find_start(datastream, 4)
    print(f"{part_1=}")

    part_2 = find_start(datastream, 14)
    print(f"{part_2=}")


def read_input() -> str:
    with open("day06.txt") as f:
        return f.read().rstrip()


if __name__ == "__main__":
    main()
