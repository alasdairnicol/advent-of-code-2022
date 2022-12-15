#!/usr/bin/env python
from dataclasses import dataclass
import functools


@dataclass
class Beacon:
    x: int
    y: int


@dataclass
class Sensor:
    x: int
    y: int
    distance_to_nearest_beacon: int

    def exclude_points_on_row(self, row_y):
        y_dist = abs(self.y - row_y)
        x_dist = self.distance_to_nearest_beacon - y_dist
        return range(self.x - x_dist, self.x + x_dist + 1)


def extract_int(word):
    """e.g. 'y=2016823:' -> 2016823"""
    if not word[-1].isdigit():
        word = word[:-1]
    return int(word.split("=", maxsplit=1)[1])


def parse_line(line):
    words = line.split()
    sensor_x = extract_int(words[2])
    sensor_y = extract_int(words[3])
    beacon_x = extract_int(words[8])
    beacon_y = extract_int(words[9])

    distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
    beacon = Beacon(beacon_x, beacon_y)
    sensor = Sensor(sensor_x, sensor_y, distance)

    return sensor, beacon


def find_gap_in_row(ranges, start, end):
    highest_stop = start
    for r in ranges:
        if r.start > highest_stop:
            # Found a gap
            return highest_stop
        else:
            highest_stop = max(r.stop, highest_stop)
        if highest_stop > end:
            # We've reached the end
            return None
    # We never covered the end
    return end


def main():
    lines = read_input()
    for line in lines:
        parse_line(line)

    sensors_and_beacons = [parse_line(line) for line in lines]
    sensors, beacons = zip(*sensors_and_beacons)

    row = 2000000

    excluded_sets = [set(sensor.exclude_points_on_row(row)) for sensor in sensors]
    excluded_set = functools.reduce(lambda x, y: x | y, excluded_sets)
    beacons_in_row = {beacon.x for beacon in beacons if beacon.y == row}
    excluded_set -= beacons_in_row

    part_1 = len(excluded_set)
    print(f"{part_1=}")

    num_rows = 4000000

    for y in range(num_rows + 1):
        excluded_ranges = [sensor.exclude_points_on_row(y) for sensor in sensors]
        sorted_ranges = sorted(
            [sensor for sensor in excluded_ranges if sensor.stop > sensor.start],
            key=lambda x: x.start,
        )

        x = find_gap_in_row(sorted_ranges, 0, num_rows)
        if x is not None:
            # Found a gap
            break

    part_2 = 4000000 * x + y
    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day15.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
