#!/usr/bin/env python


def parse_elf_string(elf_string: str) -> list[int]:
    return [int(num) for num in elf_string.split("\n")]


def parse_input(input_string: str) -> list[int]:
    elves = input_string.split("\n\n")
    return [sum(parse_elf_string(elf)) for elf in elves]


def main():
    elves = sorted(parse_input(read_input()), reverse=True)

    part_1 = elves[0]
    print(f"{part_1=}")

    part_2 = sum(elves[:3])
    print(f"{part_2=}")


def read_input() -> str:
    with open("day01.txt") as f:
        return f.read().strip()


if __name__ == "__main__":
    main()
