#!/usr/bin/env python

WIN = 6
DRAW = 3
LOSS = 0

shape_scores = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}

round_1_move_scores = {
    ("A", "X"): DRAW,
    ("A", "Y"): WIN,
    ("A", "Z"): LOSS,
    ("B", "X"): LOSS,
    ("B", "Y"): DRAW,
    ("B", "Z"): WIN,
    ("C", "X"): WIN,
    ("C", "Y"): LOSS,
    ("C", "Z"): DRAW,
}

round_2_shapes = {
    ("A", "X"): "Z",
    ("A", "Y"): "X",
    ("A", "Z"): "Y",
    ("B", "X"): "X",
    ("B", "Y"): "Y",
    ("B", "Z"): "Z",
    ("C", "X"): "Y",
    ("C", "Y"): "Z",
    ("C", "Z"): "X",
}

round_2_move_scores = {
    "X": LOSS,
    "Y": DRAW,
    "Z": WIN,
}


def parse_line(line: str) -> tuple[str, str]:
    shape_1, shape_2 = line.split(" ", maxsplit=1)
    return (shape_1, shape_2)


def score_round_1(round):
    return round_1_move_scores[round] + shape_scores[round[1]]


def do_part_1(rounds):
    scores = [score_round_1(r) for r in rounds]
    return sum(scores)


def score_round_2(round):
    shape = round_2_shapes[round]
    return round_2_move_scores[round[1]] + shape_scores[shape]


def do_part_2(rounds):
    scores = [score_round_2(r) for r in rounds]
    return sum(scores)


def main():
    lines = read_input()
    rounds = [parse_line(line) for line in lines]

    part_1 = do_part_1(rounds)
    print(f"{part_1=}")

    part_2 = do_part_2(rounds)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day02.txt") as f:
        return f.read().strip().split("\n")


if __name__ == "__main__":
    main()
