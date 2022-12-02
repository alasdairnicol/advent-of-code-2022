#!/usr/bin/env python

# Outcome score
WIN = 6
DRAW = 3
LOSS = 0

# Shape scores
ROCK = 1
PAPER = 2
SCISSORS = 3

elf_move_to_shape = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS,
}

round_1_move_to_shape = {
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS,
}

round_2_outcome_scores = {
    "X": LOSS,
    "Y": DRAW,
    "Z": WIN,
}

score_round = {
    # (elf_move, your_move): outcome
    (ROCK, ROCK): DRAW,
    (ROCK, PAPER): WIN,
    (ROCK, SCISSORS): LOSS,
    (PAPER, ROCK): LOSS,
    (PAPER, PAPER): DRAW,
    (PAPER, SCISSORS): WIN,
    (SCISSORS, ROCK): WIN,
    (SCISSORS, PAPER): LOSS,
    (SCISSORS, SCISSORS): DRAW,
}

round_2_shapes = {
    # (elf_move, outcome): your_move
    (ROCK, LOSS): SCISSORS,
    (ROCK, DRAW): ROCK,
    (ROCK, WIN): PAPER,
    (PAPER, LOSS): ROCK,
    (PAPER, DRAW): PAPER,
    (PAPER, WIN): SCISSORS,
    (SCISSORS, LOSS): PAPER,
    (SCISSORS, DRAW): SCISSORS,
    (SCISSORS, WIN): ROCK,
}


def parse_line(line: str) -> tuple[str, str]:
    pieces = line.split(" ", maxsplit=1)
    return (pieces[0], pieces[1])


def score_round_1(round: tuple[str, str]) -> int:
    elf_shape = elf_move_to_shape[round[0]]
    your_shape = round_1_move_to_shape[round[1]]
    outcome_score = score_round[(elf_shape, your_shape)]
    shape_score = your_shape
    return outcome_score + shape_score


def do_part_1(rounds: list[tuple[str, str]]) -> int:
    scores = [score_round_1(r) for r in rounds]
    return sum(scores)


def score_round_2(round: tuple[str, str]) -> int:
    elf_shape = elf_move_to_shape[round[0]]
    your_outcome = round[1]
    outcome_score = round_2_outcome_scores[your_outcome]
    your_shape = round_2_shapes[(elf_shape, outcome_score)]
    shape_score = your_shape
    return outcome_score + shape_score


def do_part_2(rounds: list[tuple[str, str]]) -> int:
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
