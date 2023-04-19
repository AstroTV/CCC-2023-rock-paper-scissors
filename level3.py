import os
from dataclasses import dataclass
import random
from itertools import permutations


def parse(lines):
    tokens = lines.pop(0).split(" ")
    n = int(tokens[0])
    m = int(tokens[1])

    amounts = []
    for i in range(n):
        tokens = lines.pop(0).strip().split(" ")
        amountR = int(tokens[0][:-1])
        amountP = int(tokens[1][:-1])
        amountS = int(tokens[2][:-1])
        amounts.append([amountR, amountP, amountS])
    return n, m, amounts


def check(n: int, m: int, fighters: str):
    print(f"Fighters: {fighters}")
    round_winners = fighters
    for r in range(2):
        print(f"Round {r}")
        pairs = [round_winners[i:i + 2] for i in range(0, int(m / (1 + r)), 2)]

        print(f"Pairs: {pairs}")
        round_winners = ""
        for pair in pairs:
            round_winners += winner(pair)
        print(f"Round winners: {round_winners}")
    print(f"Winners: {round_winners}")
    return "R" not in round_winners and "S" in round_winners


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


def handle(n: int, m: int, amounts: [[int]]):
    styles = ""
    for t in range(n):
        pairings = ""
        rocks = amounts[t][0]
        papers = amounts[t][1]
        scissors = amounts[t][2]
        # Create as many "RRRP"s as possible
        while rocks >= 3 and papers >= 1:
            pairings += "RRRP"
            rocks -= 3
            papers -= 1
        while rocks >= 2 and papers >= 1 and scissors >= 2:
            pairings += "PRRS"
            rocks -= 2
            papers -= 1
            scissors -= 1
        # Pair as many rocks with paper as possible
        while papers and rocks:
            pairings += "PR"
            papers -= 1
            rocks -= 1
        # Pair one Scissor with Paper if possible
        if scissors >= 2:
            pairings += "SS"
            scissors -= 2
        elif papers and scissors:
            pairings += "SP"
            papers -= 1
            scissors -= 1

        # Eliminate as many rocks as possible by paring them with other rocks
        while rocks >= 2:
            pairings += "RR"
            rocks -= 2

        while rocks:
            pairings += "R"
            rocks -= 1
        while papers:
            pairings += "P"
            papers -= 1
        while scissors:
            pairings += "S"
            scissors -= 1
        assert (check(n, m, pairings))
        styles += (pairings + "\n")
    return styles


def solve(lines, name):
    print(f"Solving {name}")
    n, m, amounts = parse(lines)
    output = handle(n, m, amounts)
    with open("output/" + name + ".out", 'w') as out_file:
        out_file.writelines(["".join(output)])


def main():
    folder = "/home/thomas/Downloads/level3/"
    for file in sorted(os.listdir(folder)):
        with open(folder + file) as f:
            lines = f.readlines()
            solve(lines, file.split(".")[0])


if __name__ == "__main__":
    main()
