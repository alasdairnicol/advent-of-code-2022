#!/usr/bin/env python
from dataclasses import dataclass, field


@dataclass
class Directory:
    parent: None
    name: str
    files: dict = field(default_factory=dict)

    @property
    def size(self):
        if not hasattr(self, "_size"):
            self._size = sum(f.size for f in self.files.values())
        return self._size


@dataclass
class File:
    name: str
    size: int


def main():
    lines = read_input()

    cwd = None

    root = Directory(parent=None, name="/")
    directories = [root]

    for line in lines:
        words = line.split(" ")
        if words[:2] == ["$", "cd"]:
            if words[2] == "/":
                cwd = root
            elif words[2] == "..":
                cwd = cwd.parent
            else:
                cwd = cwd.files[words[2]]
        elif words[:2] == ["$", "ls"]:
            pass
        else:
            name = words[1]
            if words[0] == "dir":
                cwd.files[name] = Directory(parent=cwd, name=name)
                directories.append(cwd.files[name])
            else:
                size = int(words[0])
                cwd.files[name] = File(name=name, size=size)

    sizes = [d.size for d in directories]
    part_1 = sum(s for s in sizes if s < 100000)
    print(f"{part_1=}")

    total = 70000000
    required = 30000000

    used = root.size
    current_free = total - used
    need_to_free = required - current_free

    sizes.sort()

    part_2 = next(s for s in sizes if s >= need_to_free)

    print(f"{part_2=}")


def read_input() -> list[str]:
    with open("day07.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
