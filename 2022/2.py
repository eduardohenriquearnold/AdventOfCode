from enum import Enum


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(Enum):
    WIN = 6
    DRAW = 3
    LOOSE = 0


adv_mapping = {"A": Shape.ROCK, "B": Shape.PAPER, "C": Shape.SCISSORS}
own_mapping = {"X": Shape.ROCK, "Y": Shape.PAPER, "Z": Shape.SCISSORS}
goal_mapping = {"X": Outcome.LOOSE, "Y": Outcome.DRAW, "Z": Outcome.WIN}


def outcome(s0: Shape, s1: Shape) -> Outcome:
    assert isinstance(s0, Shape) and isinstance(s1, Shape)

    if s0 == s1:
        return Outcome.DRAW

    if (s0, s1) in (
        (Shape.ROCK, Shape.SCISSORS),
        (Shape.SCISSORS, Shape.PAPER),
        (Shape.PAPER, Shape.ROCK),
    ):
        return Outcome.LOOSE

    return Outcome.WIN


def shape_needed_for_outcome(s0: Shape, outcome: Outcome):
    assert isinstance(s0, Shape) and isinstance(outcome, Outcome)

    if outcome == Outcome.DRAW:
        return s0

    strategy = {
        Shape.ROCK: Shape.SCISSORS,
        Shape.PAPER: Shape.ROCK,
        Shape.SCISSORS: Shape.PAPER,
    }
    if outcome == Outcome.WIN:
        strategy = {v: k for k, v in strategy.items()}

    return strategy[s0]


lines = open("inputs/2.txt", "r").readlines()

# Part 1
score = 0
for line in lines:
    adv, me = line.strip().split(" ")
    adv = adv_mapping[adv]
    me = own_mapping[me]
    score += me.value + outcome(adv, me).value
print(score)


# Part 2
score = 0
for line in lines:
    adv, goal = line.strip().split(" ")
    adv = adv_mapping[adv]
    goal = goal_mapping[goal]
    me = shape_needed_for_outcome(adv, goal)
    score += me.value + goal.value
print(score)
