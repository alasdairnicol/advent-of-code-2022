#!/usr/bin/env python
from collections import deque


def do_mixing(
    initial_numbers: list[int], multiplier: int = 1, num_rounds: int = 1
) -> int:
    zero = initial_numbers.index(0)

    length = len(initial_numbers)
    numbers_dict = dict(enumerate(x * multiplier for x in initial_numbers))
    rotate_dict = {k: v % (length - 1) for k, v in numbers_dict.items()}

    positions = deque(range(length))

    for round in range(num_rounds):
        for position in range(length):
            number = rotate_dict[position]
            # Rotate deque so that position is at the beginning
            positions.rotate(-positions.index(position))

            positions.popleft()
            positions.rotate(-number)
            positions.appendleft(position)

    zero_index = positions.index(zero)

    return sum(
        [
            numbers_dict[positions[(zero_index + 1000) % length]],
            numbers_dict[positions[(zero_index + 2000) % length]],
            numbers_dict[positions[(zero_index + 3000) % length]],
        ]
    )


def main():
    lines = read_input()
    numbers = [int(x) for x in lines]

    part_1 = do_mixing(numbers)
    print(f"{part_1=}")
    part_2 = do_mixing(numbers, multiplier=811589153, num_rounds=10)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day20.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
