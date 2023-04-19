import os
from dataclasses import dataclass


def parse(lines):
    n = int(lines.pop(0))
    styles = []
    for i in range(n):
        styles.append(lines.pop(0))
    return n, styles


def winner(styles: str) -> str:
    if styles[0] == "P" and styles[1] == "R":
        return "P"
    if styles[0] == "P" and styles[1] == "P":
        return "P"
    if styles[0] == "P" and styles[1] == "S":
        return "S"
    if styles[0] == "R" and styles[1] == "R":
        return "R"
    if styles[0] == "R" and styles[1] == "P":
        return "P"
    if styles[0] == "R" and styles[1] == "S":
        return "R"
    if styles[0] == "S" and styles[1] == "R":
        return "R"
    if styles[0] == "S" and styles[1] == "P":
        return "S"
    if styles[0] == "S" and styles[1] == "S":
        return "S"


def handle(n: int, styles: [str]):
    winners = []
    for style in styles:
        winners.append(winner(style))
    return winners


def solve(lines, name):
    print(f"Solving {name}")
    n, styles = parse(lines)
    output = handle(n, styles)
    with open("output/" + name + ".out", 'w') as out_file:
        out_file.writelines(["\n".join(output)])


def main():
    folder = "/home/thomas/Downloads/level1/"
    for file in sorted(os.listdir(folder)):
        with open(folder + file) as f:
            lines = f.readlines()
            solve(lines, file.split(".")[0])


if __name__ == "__main__":
    main()
