#!/usr/bin/env python
import itertools
import functools
from typing import Generator, Iterable

# Mypy does not appear to support recursive type that lets us do
# list[int|list[int|list[...]]]
Packet = list[int | list]


def grouper(n: int, iterable: Iterable) -> Iterable:
    """
    Split an iterable into chunks of n

    e.g. grouper('ABCDEFGHI', 3) -> 'ABC', 'DEF', 'GHI'

    NB Discards elements if len(iterable) is not divisible by n
    """
    return zip(*[iter(iterable)] * n)


def tokenise(packet: str) -> Generator[str | int, None, None]:
    number = ""
    for char in packet:
        if char in "[],":
            if number:
                yield int(number)
                number = ""
            if char != ",":
                yield char
        else:
            number += char
    return None


def parse_packet(packet: str) -> list:
    stack = []
    for char in tokenise(packet):
        if char == "[":
            current: list = []
            stack.append(current)
        elif char == "]":
            complete = stack.pop()
            if not stack:
                return complete
            else:
                current = stack[-1]
                stack[-1].append(complete)
        else:
            stack[-1].append(int(char))

    raise ValueError("Invalid packet")


def compare(packet_1, packet_2) -> int:
    # Tried to add type hints for packet_1 and packet_2 but couldn't get
    # them to pass with mypy!
    if isinstance(packet_1, int) and isinstance(packet_2, int):
        if packet_1 < packet_2:
            return -1
        elif packet_1 == packet_2:
            return 0
        else:
            return 1

    if isinstance(packet_1, int):
        packet_1 = [packet_1]
    elif isinstance(packet_2, int):
        packet_2 = [packet_2]

    for x, y in itertools.zip_longest(packet_1, packet_2):
        if y is None:
            return 1
        elif x is None:
            return -1

        out = compare(x, y)
        if out:
            return out
    return 0


def parse_packets(lines: list[str]) -> list[Packet]:
    return [parse_packet(packet) for packet in lines if packet]


def do_part_1(packets: list[Packet]) -> int:
    correct_order = [
        compare(packet_1, packet_2) for (packet_1, packet_2) in grouper(2, packets)
    ]
    return sum((i for (i, x) in enumerate(correct_order, 1) if x <= 0))


def do_part_2_by_sorting(packets: list[Packet]) -> int:
    """
    This approach sorts the entire list so does more comparisons than necessary
    """
    divider_packets: list[Packet] = [[[2]], [[6]]]

    all_packets = packets + divider_packets
    all_packets.sort(key=functools.cmp_to_key(compare))
    indexes = [all_packets.index(packet) for packet in divider_packets]

    return (indexes[0] + 1) * (indexes[1] + 1)


def do_part_2(packets: list[Packet]) -> int:
    divider_1 = [[2]]
    divider_2 = [[6]]
    # assert compare(divider_1, divider_2) == -1

    index_1 = 0
    index_2 = 0

    for packet in packets:
        if compare(packet, divider_1) == -1:
            index_1 += 1
            index_2 += 1  # Since we asserted divider_1 < divider_2
        elif compare(packet, divider_2) == -1:
            index_2 += 1

    return (index_1 + 1) * (index_2 + 2)


def main():
    lines = read_input()

    packets = parse_packets(lines)

    part_1 = do_part_1(packets)
    print(f"{part_1=}")

    part_2 = do_part_2(packets)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day13.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
