import math

from ortools.sat.python import cp_model
import os


class SolutionPrinterClass(cp_model.CpSolverSolutionCallback):
    def __init__(self, fighters, rounds, styles, sols):
        val = cp_model.CpSolverSolutionCallback.__init__(self)
        self._fighters = fighters
        self._rounds = rounds
        self._styles = styles
        self._solutions = set(sols)
        self._solution_count = 0
        self.style_names = ["R", "P", "S"]

    def on_solution_callback(self):
        output = ""
        if self._solution_count in self._solutions:
            for y in range(self._rounds + 1):
                participants = pow(2, self._rounds - y)
                for x in range(participants):
                    for z in range(self._styles):
                        if self.Value(self._fighters[(y, x, z)]):
                            output += self.style_names[z]
        self._solution_count += 1
        return output

    def solution_count(self):
        return self._solution_count


def handle_tournament(n, m, amounts):
    output = []
    for i in range(n):
        output.append(handle(m, amounts[i]) + "\n")

    return output


def handle(m, amounts):
    model = cp_model.CpModel()
    fighters = {}
    styles = 3
    rounds = int(math.log2(m))
    rocks = amounts[0]
    papers = amounts[1]
    scissors = amounts[2]
    style_names = ["R", "P", "S"]

    for round in range(rounds + 1):
        participants = pow(2, rounds - round)
        for participant in range(participants):
            for style in range(styles):
                fighters[(round, participant, style)] = model.NewBoolVar(
                    "fighter r:" + str(round) + " p:" + str(participant) + " s:" + str(style))

    for round in range(rounds + 1):
        participants = pow(2, rounds - round)
        for participant in range(participants):
            model.Add(sum(fighters[(round, participant, style)] for style in range(styles)) == 1)

    model.Add(sum(fighters[(0, participant, 0)] for participant in range(pow(2, rounds))) == rocks)
    model.Add(sum(fighters[(0, participant, 1)] for participant in range(pow(2, rounds))) == papers)
    model.Add(sum(fighters[(0, participant, 2)] for participant in range(pow(2, rounds))) == scissors)

    combinations = {}
    for round in range(1, rounds + 1):
        for participant in range(pow(2, rounds - round)):
            combinations[(round, participant, "RR")] = model.NewBoolVar(f"RR r:{round}, p:{participant}")
            combinations[(round, participant, "RP")] = model.NewBoolVar(f"RS r:{round}, p:{participant}")
            combinations[(round, participant, "RS")] = model.NewBoolVar(f"SR r:{round}, p:{participant}")
            combinations[(round, participant, "PR")] = model.NewBoolVar(f"RR r:{round}, p:{participant}")
            combinations[(round, participant, "PP")] = model.NewBoolVar(f"RS r:{round}, p:{participant}")
            combinations[(round, participant, "PS")] = model.NewBoolVar(f"SR r:{round}, p:{participant}")
            combinations[(round, participant, "SR")] = model.NewBoolVar(f"RR r:{round}, p:{participant}")
            combinations[(round, participant, "SP")] = model.NewBoolVar(f"RS r:{round}, p:{participant}")
            combinations[(round, participant, "SS")] = model.NewBoolVar(f"SR r:{round}, p:{participant}")

            model.AddBoolOr(fighters[(round - 1, participant * 2, 0)].Not(),
                            fighters[(round - 1, participant * 2 + 1, 0)].Not(),
                            combinations[(round, participant, "RR")])
            model.AddImplication(combinations[(round, participant, "RR")], fighters[(round - 1, participant * 2, 0)])
            model.AddImplication(combinations[(round, participant, "RR")],
                                 fighters[(round - 1, participant * 2 + 1, 0)])

            model.AddBoolOr(fighters[(round - 1, participant * 2, 0)].Not(),
                            fighters[(round - 1, participant * 2 + 1, 1)].Not(),
                            combinations[(round, participant, "RP")])
            model.AddImplication(combinations[(round, participant, "RP")], fighters[(round - 1, participant * 2, 0)])
            model.AddImplication(combinations[(round, participant, "RP")],
                                 fighters[(round - 1, participant * 2 + 1, 1)])

            model.AddBoolOr(fighters[(round - 1, participant * 2, 0)].Not(),
                            fighters[(round - 1, participant * 2 + 1, 2)].Not(),
                            combinations[(round, participant, "RS")])
            model.AddImplication(combinations[(round, participant, "RS")], fighters[(round - 1, participant * 2, 0)])
            model.AddImplication(combinations[(round, participant, "RS")],
                                 fighters[(round - 1, participant * 2 + 1, 2)])

            model.AddBoolOr(fighters[(round - 1, participant * 2, 1)].Not(),
                            fighters[(round - 1, participant * 2 + 1, 0)].Not(),
                            combinations[(round, participant, "PR")])
            model.AddImplication(combinations[(round, participant, "PR")], fighters[(round - 1, participant * 2, 1)])
            model.AddImplication(combinations[(round, participant, "PR")],
                                 fighters[(round - 1, participant * 2 + 1, 0)])

            model.AddBoolOr(fighters[(round - 1, participant * 2, 1)].Not(),
                            fighters[(round - 1, participant * 2 + 1, 1)].Not(),
                            combinations[(round, participant, "PP")])
            model.AddImplication(combinations[(round, participant, "PP")], fighters[(round - 1, participant * 2, 1)])
            model.AddImplication(combinations[(round, participant, "PP")],
                                 fighters[(round - 1, participant * 2 + 1, 1)])

            model.AddBoolOr(fighters[(round - 1, participant * 2, 1)].Not(),
                            fighters[(round - 1, participant * 2 + 1, 2)].Not(),
                            combinations[(round, participant, "PS")])
            model.AddImplication(combinations[(round, participant, "PS")], fighters[(round - 1, participant * 2, 1)])
            model.AddImplication(combinations[(round, participant, "PS")],
                                 fighters[(round - 1, participant * 2 + 1, 2)])

            model.AddBoolOr(fighters[(round - 1, participant * 2, 2)].Not(),
                            fighters[(round - 1, participant * 2 + 1, 0)].Not(),
                            combinations[(round, participant, "SR")])
            model.AddImplication(combinations[(round, participant, "SR")], fighters[(round - 1, participant * 2, 2)])
            model.AddImplication(combinations[(round, participant, "SR")],
                                 fighters[(round - 1, participant * 2 + 1, 0)])

            model.AddBoolOr(fighters[(round - 1, participant * 2, 2)].Not(),
                            fighters[(round - 1, participant * 2 + 1, 1)].Not(),
                            combinations[(round, participant, "SP")])
            model.AddImplication(combinations[(round, participant, "SP")], fighters[(round - 1, participant * 2, 2)])
            model.AddImplication(combinations[(round, participant, "SP")],
                                 fighters[(round - 1, participant * 2 + 1, 1)])

            model.AddBoolOr(fighters[(round - 1, participant * 2, 2)].Not(),
                            fighters[(round - 1, participant * 2 + 1, 2)].Not(),
                            combinations[(round, participant, "SS")])
            model.AddImplication(combinations[(round, participant, "SS")], fighters[(round - 1, participant * 2, 2)])
            model.AddImplication(combinations[(round, participant, "SS")],
                                 fighters[(round - 1, participant * 2 + 1, 2)])

            model.AddImplication(combinations[(round, participant, "RR")], fighters[(round, participant, 0)])
            model.AddImplication(combinations[(round, participant, "RP")], fighters[(round, participant, 1)])
            model.AddImplication(combinations[(round, participant, "RS")], fighters[(round, participant, 0)])
            model.AddImplication(combinations[(round, participant, "PR")], fighters[(round, participant, 1)])
            model.AddImplication(combinations[(round, participant, "PP")], fighters[(round, participant, 1)])
            model.AddImplication(combinations[(round, participant, "PS")], fighters[(round, participant, 2)])
            model.AddImplication(combinations[(round, participant, "SR")], fighters[(round, participant, 0)])
            model.AddImplication(combinations[(round, participant, "SP")], fighters[(round, participant, 2)])
            model.AddImplication(combinations[(round, participant, "SS")], fighters[(round, participant, 2)])

    model.AddAbsEquality(fighters[(rounds, 0, 2)], True)

    # solve the model
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    # solve it and check if solution was feasible
    solutionrange = range(1)  # we want to display 1 feasible results (the first one in the feasible set)
    solution_printer = SolutionPrinterClass(fighters, rounds, styles, solutionrange)
    solver.Solve(model, solution_printer)
    output = ""
    for participant in range(pow(2, rounds)):
        for style in range(styles):
            if solver.Value(fighters[0, participant, style]):
                output += style_names[style]
    return output


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


def solve(lines, name):
    print(f"Solving {name}")
    n, m, amounts = parse(lines)
    output = handle_tournament(n, m, amounts)
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
