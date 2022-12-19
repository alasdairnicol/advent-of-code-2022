#!/usr/bin/env python
import functools


def parse_blueprint(line):
    words = line.split()
    # return (
    #     (3, (int(words[27]), 0, int(words[30]),0)),
    #     (2, (int(words[18]), int(words[21]), 0,0)),
    #     (1, (int(words[12]), 0, 0,0)),
    #     (0, (int(words[6]), 0, 0,0)),
    #     # Don't build a robot
    #     (4, (0, 0, 0,0)),
    # )

    return (
        (int(words[6]), 0, 0, 0),
        (int(words[12]), 0, 0, 0),
        (int(words[18]), int(words[21]), 0, 0),
        (int(words[27]), 0, int(words[30]), 0),
        # Don't build a robot
        (0, 0, 0, 0),
    )


@functools.cache
def calc_quality_level(
    blueprint, max_robots, resources, robots, days_remaining, early_exit=1
):
    # print(resources, robots, blueprint[3], days_remaining)
    if days_remaining == 1:
        return resources[-1] + robots[-1]
    if days_remaining < early_exit and not resources[-1]:
        # Hack to narrow down search space for part 2
        return None
    quality_level = None

    for i in (3, 2, 1, 0, 4):
        if i < 3 and robots[i] >= max_robots[i]:
            continue
        requirements = blueprint[i]
        new_resources_after_build = tuple(
            x - y for x, y in zip(resources, requirements)
        )
        if all(x >= 0 for x in new_resources_after_build):
            new_robots = tuple(x + 1 if i == j else x for j, x in enumerate(robots))
            new_resources = tuple(
                x + y for x, y in zip(robots, new_resources_after_build)
            )
            new_days_remaining = days_remaining - 1
            new_quality_level = calc_quality_level(
                blueprint,
                max_robots,
                new_resources,
                new_robots,
                new_days_remaining,
                early_exit,
            )
            if new_quality_level is not None and (
                quality_level is None or new_quality_level > quality_level
            ):
                quality_level = new_quality_level
            if i == 3:
                # Always make a geode robot if you can
                # print("Always make a geode!")
                break

    return quality_level


test_input = [
    "Blueprint 1: Each ore robot costs 4 ore.\
Each clay robot costs 2 ore.\
Each obsidian robot costs 3 ore and 14 clay.\
Each geode robot costs 2 ore and 7 obsidian.",
    "Blueprint 2: Each ore robot costs 2 ore.\
Each clay robot costs 3 ore.\
Each obsidian robot costs 3 ore and 8 clay.\
Each geode robot costs 3 ore and 12 obsidian.",
]


def do_part_1(blueprints):
    import time

    total = 0

    for id_number, blueprint in enumerate(blueprints, 1):
        max_robots = tuple(max(col) for col in zip(*blueprint))
        print(calc_quality_level.cache_info())
        calc_quality_level.cache_clear()
        t = time.time()
        quality_level = calc_quality_level(
            blueprint, max_robots, (0, 0, 0, 0), (1, 0, 0, 0), 24
        )
        print(id_number, quality_level, time.time() - t)
        total += id_number * quality_level

    return total


# 12, 35, 52
def do_part_2(blueprints):
    import time

    total = 1

    for blueprint, early_exit in zip(blueprints[:3], [1, 1, 10]):
        max_robots = tuple(max(col) for col in zip(*blueprint))
        print(calc_quality_level.cache_info())
        calc_quality_level.cache_clear()
        t = time.time()
        quality_level = calc_quality_level(
            blueprint, max_robots, (3, 0, 0, 0), (1, 0, 0, 0), 29, early_exit
        )
        print(quality_level, time.time() - t)
        total *= quality_level

    return total


def main():
    lines = read_input()

    # lines = test_input

    blueprints = [parse_blueprint(line) for line in lines]
    # quality_level = calc_quality_level(blueprints[0], (0, 0, 0, 0), (1, 0, 0, 0), 24)
    # raise

    part_1 = do_part_1(blueprints)
    print(f"{part_1=}")
    part_2 = do_part_2(blueprints)
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day19.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
