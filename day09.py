#!/usr/bin/env python
Knot = tuple[int, int]


def do_moves(moves, num_knots: int) -> int:
    knots = [[0, 0] for _ in range(num_knots)]
    visited: set[Knot] = set()
    for direction, count in moves:
        for x in range(count):
            head = knots[0]
            if direction == "U":
                head[1] += 1
            if direction == "D":
                head[1] -= 1
            if direction == "L":
                head[0] -= 1
            if direction == "R":
                head[0] += 1

            for i in range(1, num_knots):
                knot_a = knots[i - 1]
                knot_b = knots[i]

                if abs(knot_a[0] - knot_b[0]) == 2 or abs(knot_a[1] - knot_b[1]) == 2:
                    if knot_a[0] > knot_b[0]:
                        knot_b[0] += 1
                    elif knot_a[0] < knot_b[0]:
                        knot_b[0] -= 1

                    if knot_a[1] > knot_b[1]:
                        knot_b[1] += 1
                    elif knot_a[1] < knot_b[1]:
                        knot_b[1] -= 1

            # build tuple because mypy doesn't like tuple(knots[-1])
            tail_tuple = (knots[-1][0], knots[-1][1])
            visited.add(tail_tuple)

    return len(visited)


def main():
    lines = read_input()
    moves = (line.split(" ") for line in lines)
    moves = [[direction, int(count)] for (direction, count) in moves]

    part_1 = do_moves(moves, 2)
    print(f"{part_1=}")

    part_2 = do_moves(moves, 10)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day09.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
