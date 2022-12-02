#!/usr/bin/env python


letter_to_instruction = {
    "A": 0,
    "B": 1,
    "C": 2,
    "X": 0,
    "Y": 1,
    "Z": 2,
}


def parse_line(line: str) -> tuple[int, int]:
    p1, p2 = line.split(" ", maxsplit=1)
    return (letter_to_instruction[p1], letter_to_instruction[p2])


def score_round_1(player_1: int, player_2: int) -> int:
    outcome_score = ((player_2 + 1 - player_1) % 3) * 3
    shape_score = player_2 + 1
    return outcome_score + shape_score


def do_part_1(rounds: list[tuple[int, int]]) -> int:
    scores = [score_round_1(p1, p2) for (p1, p2) in rounds]
    return sum(scores)


def score_round_2(player_1, player_2) -> int:
    outcome_score = 3 * player_2
    shape_score = (player_1 + player_2 - 1) % 3 + 1
    return outcome_score + shape_score


def do_part_2(rounds: list[tuple[int, int]]) -> int:
    scores = [score_round_2(p1, p2) for (p1, p2) in rounds]
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
