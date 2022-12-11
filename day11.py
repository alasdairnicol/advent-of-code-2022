#!/usr/bin/env python
from dataclasses import dataclass
from typing import Callable


@dataclass
class Monkey:
    operation: Callable
    divisor: int
    if_true: int
    if_false: int
    items: list
    num_items: int = 0

    @property
    def size(self):
        if not hasattr(self, "_size"):
            self._size = sum(f.size for f in self.files.values())
        return self._size


def operation_monkey_0(old):
    return old * 5


monkey_0 = Monkey(
    operation=operation_monkey_0,
    divisor=7,
    if_true=6,
    if_false=7,
    items=[89, 84, 88, 78, 70],
)


def operation_monkey_1(old):
    return old + 1


monkey_1 = Monkey(
    operation=operation_monkey_1,
    divisor=17,
    if_true=0,
    if_false=6,
    items=[76, 62, 61, 54, 69, 60, 85],
)


def operation_monkey_2(old):
    return old + 8


monkey_2 = Monkey(
    operation=operation_monkey_2,
    divisor=11,
    if_true=5,
    if_false=3,
    items=[83, 89, 53],
)


def operation_monkey_3(old):
    return old + 4


monkey_3 = Monkey(
    operation=operation_monkey_3,
    divisor=13,
    if_true=0,
    if_false=1,
    items=[95, 94, 85, 57],
)


def operation_monkey_4(old):
    return old + 7


monkey_4 = Monkey(
    operation=operation_monkey_4,
    divisor=19,
    if_true=5,
    if_false=2,
    items=[82, 98],
)


def operation_monkey_5(old):
    return old + 2


monkey_5 = Monkey(
    operation=operation_monkey_5,
    divisor=2,
    if_true=1,
    if_false=3,
    items=[69],
)


def operation_monkey_6(old):
    return old * 11


monkey_6 = Monkey(
    operation=operation_monkey_6,
    divisor=5,
    if_true=7,
    if_false=4,
    items=[82, 70, 58, 87, 59, 99, 92, 65],
)


def operation_monkey_7(old):
    return old * old


monkey_7 = Monkey(
    operation=operation_monkey_7,
    divisor=3,
    if_true=4,
    if_false=2,
    items=[91, 53, 96, 98, 68, 82],
)

monkeys = [
    monkey_0,
    monkey_1,
    monkey_2,
    monkey_3,
    monkey_4,
    monkey_5,
    monkey_6,
    monkey_7,
]


def play_round(monkeys):
    for monkey in monkeys:
        while monkey.items:
            value = monkey.items.pop(0)
            new_value = monkey.operation(value) // 3

            if new_value % monkey.divisor == 0:
                destination = monkey.if_true
            else:
                destination = monkey.if_false

            monkeys[destination].items.append(new_value)
            monkey.num_items += 1


def main():
    for i in range(20):
        play_round(monkeys)

    items_processed = sorted((monkey.num_items for monkey in monkeys), reverse=True)
    print(items_processed[0] * items_processed[1])

    # part_1 = sum(computer.part_1_output)
    # print(f"{part_1=}")

    # part_2 = display_part_2(computer.lit)
    # print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day11.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
