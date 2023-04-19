import os
from dataclasses import dataclass


def parse(lines):
    tokens = lines.pop(0).split(" ")
    n = int(tokens[0])
    m = int(tokens[1])
    styles = []
    for i in range(n):
        styles.append(lines.pop(0).strip())
    return n, m, styles


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


def handle(n: int, m: int, styles: [str]):
    winners = []
    round_winners = []
    for fighters in styles:
        round_winners = fighters
        for round in range(2):
            print(f"Round {round}")
            print(f"Attendees: {round_winners}")
            pairs = [round_winners[i:i + 2] for i in range(0, int(m / (1 + round)), 2)]

            print(f"Pairs: {pairs}")
            round_winners = ""
            for pair in pairs:
                round_winners += winner(pair)
            print(f"Round winners: {round_winners}")
        winners.append(round_winners)
    return winners


def solve(lines, name):
    print(f"Solving {name}")
    n, m, styles = parse(lines)
    output = handle(n, m, styles)
    with open("output/" + name + ".out", 'w') as out_file:
        out_file.writelines(["\n".join(output)])


def main():
    folder = "/home/thomas/Downloads/level2/"
    for file in sorted(os.listdir(folder)):
        with open(folder + file) as f:
            lines = f.readlines()
            solve(lines, file.split(".")[0])


if __name__ == "__main__":
    main()
