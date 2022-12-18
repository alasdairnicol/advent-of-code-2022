#!/usr/bin/env python
import itertools


def shape_a(height):
    return {(2, height), (3, height), (4, height), (5, height)}


def shape_b(height):
    return {
        (3, height),
        (2, height + 1),
        (3, height + 1),
        (4, height + 1),
        (3, height + 2),
    }


def shape_c(height):
    return {(2, height), (3, height), (4, height), (4, height + 1), (4, height + 2)}


def shape_d(height):
    return {(2, height), (2, height + 1), (2, height + 2), (2, height + 3)}


def shape_e(height):
    return {(2, height), (3, height), (2, height + 1), (3, height + 1)}


shapes = [shape_a, shape_b, shape_c, shape_d, shape_e]


def draw_shape(points):
    for y in range(4, -1, -1):
        print("".join("#" if (x, y) in points else "." for x in range(7)))


def move_left(shape):
    return


def relative_heights(points):
    absolutes = [max(y for (x, y) in points if x == i) for i in range(7)]
    min_height = min(absolutes)
    return tuple(y - min_height for y in absolutes)


def simplify_points(points, shape_points):
    """
    Check for completed rows, and if so, remove all points below
    """
    ys = sorted((y for x, y in shape_points), reverse=True)
    for y in ys:
        if all((x, y) in points for x in range(7)):
            # we have a complete row
            points = {p for p in points if p[1] >= y}
            break
    return points


def calc_highest_point(moves_string, num_shapes):
    """
    Returns the highest point after dropping num_shapes blocks
    """
    shapes_iterable = itertools.cycle(shapes)
    moves = itertools.cycle(moves_string)

    highest_point = 0
    points = {(x, 0) for x in range(7)}

    for n in range(num_shapes):
        shape_points = next(shapes_iterable)(highest_point + 4)

        while True:
            move = next(moves)

            if move == "<":
                new_shape_points = {(x - 1, y) for (x, y) in shape_points}
            elif move == ">":
                new_shape_points = {(x + 1, y) for (x, y) in shape_points}
            if any(((x, y) in points or x in (-1, 7)) for (x, y) in new_shape_points):
                # shape can't move
                pass
            else:
                shape_points = new_shape_points

            # Try to move down
            new_shape_points = {(x, y - 1) for (x, y) in shape_points}
            if any(point in points for point in new_shape_points):
                # We've reached the bottom
                points |= shape_points
                # update highest point so that next shape is dropped from correct height
                highest_point = max(y for (x, y) in points)
                break
            else:
                shape_points = new_shape_points

    return highest_point


def detect_cycle(moves_string):

    shapes_iterable = itertools.cycle(shapes)
    moves = itertools.cycle(moves_string)

    highest_point = 0
    points = {(x, 0) for x in range(7)}

    # seen = defaultdict(list)
    moves_count = 0
    moves_len = len(moves_string)
    loops = [0]
    highest_points = [0]

    seen_positions = {}

    for n in range(10000):
        shape_points = next(shapes_iterable)(highest_point + 4)

        while True:
            # Try to move left/right
            move = next(moves)
            moves_count += 1
            if moves_count % moves_len == 0:
                loops.append(n)
                highest_points.append(highest_point)

            if move == "<":
                new_shape_points = {(x - 1, y) for (x, y) in shape_points}
            elif move == ">":
                new_shape_points = {(x + 1, y) for (x, y) in shape_points}
            if any(((x, y) in points or x in (-1, 7)) for (x, y) in new_shape_points):
                # shape can't move
                pass
            else:
                shape_points = new_shape_points

            # Try to move down
            new_shape_points = {(x, y - 1) for (x, y) in shape_points}
            if any(point in points for point in new_shape_points):
                # We've reached the bottom
                points |= shape_points
                break
            else:
                shape_points = new_shape_points

        points = simplify_points(points, shape_points)
        highest_point = max(y for (x, y) in points)

        key = (
            relative_heights(points),
            moves_count % len(moves_string),
            n % len(shapes),
        )
        if key in seen_positions:
            old_n, old_highest_point = seen_positions[key]

            offset = old_n
            cycle_length = n - old_n
            height_per_cycle = highest_point - old_highest_point
            return cycle_length, offset, height_per_cycle
        else:
            seen_positions[key] = n, highest_point


def do_part_2(moves_string):
    target_moves = 1_000_000_000_000

    cycle_length, offset, height_per_cycle = detect_cycle(moves_string)
    num_cycles, extra = divmod(target_moves - offset, cycle_length)
    return (
        calc_highest_point(moves_string, offset + extra) + num_cycles * height_per_cycle
    )


def main():
    moves_string = read_input()

    part_1 = calc_highest_point(moves_string, 2022)
    print(f"{part_1=}")

    part_2 = do_part_2(moves_string)
    print(f"{part_2=}")


def read_input() -> str:
    with open("day17.txt") as f:
        return f.read().rstrip()


if __name__ == "__main__":
    main()
