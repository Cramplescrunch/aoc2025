#!/usr/bin/env python3

from typing import List

def parse_input(filename: str) -> List[str]:
    with open(filename) as file:
        return [line.rstrip() for line in file]

def get_num_from_line(line: str) -> int:
    sign_str = line[0]
    num_str = line[1::]
    if sign_str == "L":
        return - 1 * int(num_str)
    else:
        return int(num_str)

def part_1() -> int:
    lines = parse_input("input.txt")
    zero_count = 0
    sum = 50
    for line in lines:
        num = get_num_from_line(line)
        sum = (sum + num) % 100
        if sum == 0:
            zero_count += 1
    return zero_count

# The trick is to reflect the dial and consider every rotation as a right rotation to avoid weird edge cases when rotating left
# For example, when dial pos is 10 we reflect it to 90 and consider next rotations as right rotations
def part_2() -> int:
    lines = parse_input("input.txt")
    zero_count = 0
    sum = 50
    for line in lines:
        num = get_num_from_line(line)
        sign = 1 if num > 0 else -1

        sum_p_num = sum + num
        if sign < 0:
            reflected_sum = (100 - sum) % 100
            zero_count += (abs(num) + reflected_sum) // 100
        else:
            zero_count += (num + sum) // 100
        sum = sum_p_num % 100
    return zero_count


print(part_1())
print(part_2())
