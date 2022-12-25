#!/usr/bin/env python

ELVISH_DIGITS = "=-012"
base = len(ELVISH_DIGITS)
offset = ELVISH_DIGITS.index("0")


def elvish_to_integer(elvish: str) -> int:
    total = 0
    multiplier = 1
    for e_digit in reversed(elvish):
        digit = ELVISH_DIGITS.index(e_digit) - offset
        total += multiplier * digit
        multiplier *= base
    return total


def integer_to_elvish(number: int) -> str:
    elvish_digits = []
    while number:
        number, remainder = divmod(number, base)
        if remainder > base - offset - 1:
            remainder -= base
            number += 1
        elvish_digits.append(ELVISH_DIGITS[remainder + offset])
    return "".join(reversed(elvish_digits))


def do_part_1(elvish_numbers: list[str]) -> str:
    total_in_integer = sum(elvish_to_integer(number) for number in elvish_numbers)
    return integer_to_elvish(total_in_integer)


def main():
    lines = read_input()
    part_1 = do_part_1(lines)
    print(f"{part_1=}")


def read_input() -> list[str]:
    with open("day25.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
