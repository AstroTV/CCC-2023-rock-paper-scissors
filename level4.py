import math
import os
from dataclasses import dataclass
import random
from itertools import permutations

from ortools.sat.python import cp_model


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
    r = 0
    while len(round_winners) > 1:
        print(f"Round {r}")
        pairs = [round_winners[i:i + 2] for i in range(0, int(m / (pow(2, r))), 2)]
        print(f"Pairs: {pairs}")
        round_winners = ""
        for pair in pairs:
            round_winners += winner(pair)
        print(f"Round winners: {round_winners}")
        r += 1
    print(f"Winners: {round_winners}")
    return round_winners == "S"


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
        rocks = amounts[t][0]
        papers = amounts[t][1]
        scissors = amounts[t][2]
        pairings = ""
        # How many round do we have to eliminate rocks
        rounds = int(math.log2(m))
        print(f"We play {rounds} rounds with the {m} fighters")
        for r in reversed(range(rounds)):
            if rocks == 0:
                break
            assert papers
            # For every 2^r rocks there has to be one paper
            pairings += "P"
            papers -= 1
            pairings += "R" * min(rocks, pow(2, r) - 1)
            rocks -= min(rocks, pow(2, r) - 1)

        while papers:
            pairings += "P"
            papers -= 1
        while scissors:
            pairings += "S"
            scissors -= 1
        assert check(n, m, pairings)
        styles += (pairings + "\n")
    return styles


def solve(lines, name):
    print(f"Solving {name}")
    n, m, amounts = parse(lines)
    output = handle(n, m, amounts)
    with open("output/" + name + ".out", 'w') as out_file:
        out_file.writelines(["".join(output)])


def main():
    folder = "/home/thomas/Downloads/level4/"
    for file in sorted(os.listdir(folder)):
        with open(folder + file) as f:
            lines = f.readlines()
            solve(lines, file.split(".")[0])


if __name__ == "__main__":
    main()
