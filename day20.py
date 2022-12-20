#!/usr/bin/env python
from collections import deque


def do_mixing(
    initial_numbers: list[int], multiplier: int = 1, num_rounds: int = 1
) -> int:
    zero = initial_numbers.index(0)

    len_numbers = len(initial_numbers)
    numbers_dict = dict(enumerate(x * multiplier for x in initial_numbers))
    rotate_dict = {k: v % (len_numbers - 1) for k, v in numbers_dict.items()}

    positions = deque(range(len_numbers))

    for round in range(num_rounds):
        for position in range(len_numbers):
            number = rotate_dict[position]
            while positions[0] != position:
                positions.rotate()

            positions.popleft()
            positions.rotate(-number)
            positions.appendleft(position)

    while positions[0] != zero:
        positions.rotate()

    return sum(
        [
            numbers_dict[positions[1000 % len_numbers]],
            numbers_dict[positions[2000 % len_numbers]],
            numbers_dict[positions[3000 % len_numbers]],
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
