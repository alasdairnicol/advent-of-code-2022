#!/usr/bin/env python
import copy


def rearrange_crates(crates, instructions, reverse=True):
    # Copy crates because we are going to mutate crates
    # We need to use deepcopy because values are mutable lists
    crates = copy.deepcopy(crates)
    for number, from_stack, to_stack in instructions:
        moving = crates[from_stack][-number:]
        if reverse:
            moving.reverse()
        crates[to_stack].extend(moving)
        crates[from_stack][-number:] = []
    top_crates = [crates[i][-1] for i in range(1, 10)]
    return "".join(top_crates)


def parse_line(line):
    words = line.split()
    return int(words[1]), int(words[3]), int(words[5])


def main():
    lines = read_input()
    crates, moves = lines.split("\n\n")
    moves = moves.split("\n")

    instructions = [parse_line(m) for m in moves]

    zipped = zip(*crates.split("\n"))
    zipped = [x for x in zipped if x[-1].isdigit()]

    crates = {int(x[-1]): [i for i in reversed(x[:-1]) if i.isalpha()] for x in zipped}

    part_1 = rearrange_crates(crates, instructions, reverse=True)
    print(f"{part_1=}")

    part_2 = rearrange_crates(crates, instructions, reverse=False)
    print(f"{part_2=}")


def read_input() -> str:
    with open("day05.txt") as f:
        return f.read().rstrip()


if __name__ == "__main__":
    main()
