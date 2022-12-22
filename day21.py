#!/usr/bin/env python
import operator


operators = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}


def parse_line(line: str) -> tuple:
    name, value = line.split(":")
    words = value.strip().split()
    return name, words


def get_monkey_value(monkeys: dict, name: str) -> int:
    words = monkeys[name]
    if len(words) == 3:
        value = operators[words[1]](
            get_monkey_value(monkeys, words[0]), get_monkey_value(monkeys, words[2])
        )
        words = [value]
        monkeys[name] = words
    return int(words[0])


def solve_monkey(monkeys: dict, name: str, value: int) -> None:
    words = monkeys[name]
    if words == [None]:
        # We've found the leaf
        monkeys[name] = [value]
        return

    try:
        left = get_monkey_value(monkeys, words[0])
    except:
        left = None

    try:
        right = get_monkey_value(monkeys, words[2])
    except:
        right = None
    if left is None:
        assert isinstance(right, int)
        if words[1] == "+":
            solve_monkey(monkeys, words[0], value - right)
        if words[1] == "-":
            solve_monkey(monkeys, words[0], value + right)
        if words[1] == "*":
            solve_monkey(monkeys, words[0], value // right)
        if words[1] == "/":
            solve_monkey(monkeys, words[0], value * right)
    elif right is None:
        assert isinstance(left, int)
        if words[1] == "+":
            solve_monkey(monkeys, words[2], value - left)
        if words[1] == "-":
            solve_monkey(monkeys, words[2], left - value)
        if words[1] == "*":
            solve_monkey(monkeys, words[2], value // left)
        if words[1] == "/":
            solve_monkey(monkeys, words[2], left // value)


def main():
    lines = read_input()

    monkeys = dict(parse_line(line) for line in lines)

    part_1 = get_monkey_value(monkeys, "root")
    print(f"{part_1=}")

    monkeys = dict(parse_line(line) for line in lines)
    # this is the leaf that we want to find the value for
    monkeys["humn"][0] = None
    # solving the root node left == right is equivalent
    # to solving left - right == 0
    monkeys["root"][1] = "-"
    solve_monkey(monkeys, "root", 0)
    part_2 = monkeys["humn"][0]
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day21.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
