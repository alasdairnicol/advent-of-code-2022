#!/usr/bin/env python


def parse_instruction(line):
    words = line.split()
    if len(words) == 1:
        return words
    else:
        return [words[0], int(words[1])]


class Computer:
    def __init__(self, instructions):
        self.instructions = instructions
        self.cycle = 1
        self.x_register = 1
        self.part_1_output = []
        self.lit = []

    @classmethod
    def from_lines(cls, lines):
        instructions = [parse_instruction(line) for line in lines]
        return cls(instructions)

    def run(self):
        for instruction in self.instructions:
            old_x = self.x_register
            if instruction[0] == "noop":
                cycles = [self.cycle]
                self.cycle += 1
            elif instruction[0] == "addx":
                self.x_register += instruction[1]
                cycles = [self.cycle, self.cycle + 1]
                self.cycle += 2

            for cycle in cycles:
                if cycle % 40 == 20:
                    self.part_1_output.append(old_x * cycle)

                crt_position = cycle - 1
                if crt_position % 40 in (old_x - 1, old_x, old_x + 1):
                    self.lit.append(crt_position)


def display_lcd(lit):
    for y in range(6):
        positions = [y * 40 + x for x in range(40)]
        line = "".join("#" if pos in lit else "." for pos in positions)
        print(line)


def main():
    lines = read_input()
    computer = Computer.from_lines(lines)

    computer.run()
    part_1 = sum(computer.part_1_output)
    print(f"{part_1=}")

    display_lcd(computer.lit)
    # part_2 = do_moves(moves, 10)
    # print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day10.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
