#!/usr/bin/env python3
import re
import time
import pulp

class MachineManual:
    def __init__(
            self,
            ld: list[bool],
            buttons: list[tuple[int, ...]],
            joltages: list[int]
    ):
        self.light_diagram = ld
        self.buttons = buttons
        self.joltages = joltages

    def get_buttons_for_joltage(self, joltage_idx: int) -> list[int]:
        """
        Returns the indices of the buttons that increment given joltage
        """
        res = []
        for idx, b in enumerate(self.buttons):
            if joltage_idx in b:
                res.append(idx)
        return res
        

def get_manual(line: str) -> MachineManual:
    pattern = r"^(\[.*\]) (\(.*\)) (\{.*\})"
    match = re.search(pattern, line)
    if match:
        ld_str, buttons_str, joltages_str = match[1], match[2], match[3]
        ld = list(map(lambda x: False if x == '.' else True, ld_str[1:-1]))
        buttons = []
        for b in buttons_str.split(' '):
            buttons.append(tuple(map(int, b[1:-1].split(','))))
        joltages = list(map(int, joltages_str[1:-1].split(',')))
        return MachineManual(ld, buttons, joltages)
    # Shouldn't be possible
    return MachineManual([], [], [])

def parse_input(filename: str) -> list[MachineManual]:
    with open(filename) as file:
        return [get_manual(line) for line in file]

# Mutates diagram
def apply_button_sequence_on_diagram(sequence: tuple[()] | tuple[tuple[int, ...]], diagram: list[bool]):
    for button in sequence:
        for b in button:
            diagram[b] = not diagram[b]

def generate_buttons_sequence(buttons, n: int):
    if n == 0:
        yield ()
        return

    for b in buttons:
        for rest in generate_buttons_sequence(buttons, n-1):
            yield (b,) + rest

def does_configure(count: int, manual: MachineManual) -> bool:
    for s in generate_buttons_sequence(manual.buttons, count):
        diagram = [False] * len(manual.light_diagram)
        apply_button_sequence_on_diagram(s, diagram)
        if diagram == manual.light_diagram:
            #print(f"sequence={s}")
            return True
    return False


def get_min_press(manual: MachineManual) -> int:
    # Iterate over all combinations: first try pressing only one button, then all combinations of two buttons, then all comb of three buttons, etc...
    # Stop when you have a first res
    press_count = 1
    while True:
        if does_configure(press_count, manual):
            return press_count
        else:
            press_count += 1
    return 0

def find_min_count_for_manual(manual: MachineManual) -> int:
    res, count = False, 0
    while not res:
        count += 1
        res = does_configure(count, manual)
    return count


def part_1() -> int:
    input = parse_input("input.txt")
    sum = 0
    for man in input:
        sum += find_min_count_for_manual(man)
    return sum

# Part 2
def get_fewest_presses_to_reach_joltages(machine: MachineManual) -> int:
    model = pulp.LpProblem("MachineJoltageSolver", pulp.LpMinimize)
    btn_count = len(machine.buttons)
    x = pulp.LpVariable.dicts("x", range(btn_count), lowBound=0, cat='Integer')
    model += pulp.lpSum(x[i] for i in range(btn_count))
    for idx, j in enumerate(machine.joltages):
        buttons_j = machine.get_buttons_for_joltage(idx)
        model += pulp.lpSum(x[i] for i in buttons_j) == j
    model.solve(pulp.PULP_CBC_CMD(msg=0))
    return pulp.value(model.objective)

def part_2() -> int:
    input = parse_input("input.txt")
    sum = 0
    for man in input:
        sum += get_fewest_presses_to_reach_joltages(man)
    return sum
    

manual = get_manual("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}")
#diagram = [False, False, False, False]
#for s in generate_buttons_sequence(manual.buttons, 2):
#    apply_button_sequence_on_diagram(s, diagram)
#    print(f"sequnce={s}, diagram={diagram}")
#find_min_count_for_manual(manual)

#start_time = time.time()
#print(f"Part 1: {part_1()}")
#print(f"Elapsed time: {time.time() - start_time} seconds")

start_time = time.time()
print(f"Part 2: {part_2()}")
print(f"Elapsed time: {time.time() - start_time} seconds")
        

