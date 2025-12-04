#!/usr/bin/env python3

from typing import List


def parse_input(filename: str) -> List[str]:
   with open(filename) as file:
       return [line.rstrip() for line in file]

def can_access_roll(plan: List[str], max_right_bound: int, max_bottom_bound: int, roll_pos: List[int]) -> bool:
    roll_x, roll_y = roll_pos[0], roll_pos[1]
    adjacent_rolls: int = 0
    for i in range(roll_x-1, roll_x+2):
        for j in range(roll_y-1, roll_y+2):
            if i < 0 or i >= max_right_bound or j < 0 or j >= max_bottom_bound:
                pass
            elif plan[j][i] == "@" and not (roll_x == i and roll_y == j):
                adjacent_rolls += 1
    if adjacent_rolls >= 4:
        return False
    return True

def part_1():
    input: List[str] = parse_input("input.txt")
    max_right_bound: int = len(input[0])
    max_bottom_bound: int = len(input)
    accessible_rolls: int = 0
    for i in range(max_right_bound):
        for j in range(max_bottom_bound):
            if input[j][i] == "@" and can_access_roll(input, max_right_bound, max_bottom_bound, [i, j]):
                accessible_rolls += 1
    return accessible_rolls

def part_2():
    input: List[str] = parse_input("input.txt")
    max_right_bound: int = len(input[0])
    max_bottom_bound: int = len(input)
    accessible_rolls_total: int = 0
    accessible_rolls_round: int = 0
    should_start_loop: bool = True
    while should_start_loop or accessible_rolls_round > 0:
        accessible_rolls_round = 0
        should_start_loop = False
        for i in range(max_right_bound):
            for j in range(max_bottom_bound):
                if input[j][i] == "@" and can_access_roll(input, max_right_bound, max_bottom_bound, [i, j]):
                    accessible_rolls_total += 1
                    accessible_rolls_round += 1
                    # Remove roll
                    input[j] = input[j][:i] + "." + input[j][i+1:]
    return accessible_rolls_total

print(part_1())
print(part_2())
