#!/usr/bin/env python
from datetime import date
import os
import urllib.request


def main():
    session = os.environ["session"]
    year = int(os.environ["year"])

    headers = {"Cookie": f"session={session}"}

    for day in range(1, 26):
        if date(year, 12, day) > date.today():
            break

        url = f"https://adventofcode.com/{year}/day/{day}/input"
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request)

        if response.status == 200:
            print(f"Writing response for day {day}")
            with open(f"day{day:02}.txt", "wb") as f:
                f.write(response.read())


if __name__ == "__main__":
    main()
