from typing import Callable
import re
from math import floor


class Monkey:
    instances = []
    worried = False
    common_divisor = 1

    def __init__(
        self,
        starting_items: list,
        operation: Callable[[int], int],
        test_divisor: int,
        destination_true: int,
        destination_false: int,
    ):
        self.items = starting_items
        self.operation = operation
        self.test_divisor = test_divisor
        self.destination_true = destination_true
        self.destination_false = destination_false
        self.inspections = 0

        __class__.common_divisor *= self.test_divisor
        __class__.instances.append(self)

    def turn(self):
        for worry in self.items:
            new_worry = self.operation(worry)

            if not __class__.worried:
                new_worry = floor(new_worry / 3)
            else:
                # divisors are all prime - we can use the remainder to reduce magnitude after many rounds
                new_worry = new_worry % __class__.common_divisor

            destination = self.destination_true if new_worry % self.test_divisor == 0 else self.destination_false
            __class__.instances[destination].items.append(new_worry)
            self.inspections += 1
        self.items.clear()

    @classmethod
    def round(cls):
        for monkey in cls.instances:
            monkey.turn()

    @classmethod
    def business(cls):
        inspects = sorted((monkey.inspections for monkey in cls.instances), reverse=True)
        return inspects[0] * inspects[1]


def create_operation(expression: str):
    expression = expression.split("=")[1]

    def op(old: int):
        return eval(expression)

    return op


def parse_input(content):
    Monkey.instances.clear()

    exp = re.compile(
        r"Monkey (\d+):\s+"
        r"Starting items: (.+)\s+"
        r"Operation: (.*)\s+"
        r"Test: divisible by (\d+)\s+"
        r"If true: throw to monkey (\d+)\s+"
        r"If false: throw to monkey (\d+)"
    )
    for i, (monkey_id, items, operation, divisor, if_true, if_false) in enumerate(exp.findall(content)):
        assert i == int(monkey_id), "monkeys should be in order!"
        Monkey(
            starting_items=list(map(int, items.split(", "))),
            operation=create_operation(operation),
            test_divisor=int(divisor),
            destination_true=int(if_true),
            destination_false=int(if_false),
        )


input_content = open("inputs/11.txt", "r").read()

# P1
parse_input(input_content)
for _ in range(20):
    Monkey.round()
print(Monkey.business())

# P2
parse_input(input_content)
Monkey.worried = True
for _ in range(10000):
    Monkey.round()
print(Monkey.business())
