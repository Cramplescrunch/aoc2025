#!/usr/bin/env python3

from typing import List
import functools

def parse_input(filename: str) -> List[str]:
    with open(filename) as file:
        return [line.rstrip() for line in file]

def get_largest_joltage_from_bank(bank: str) -> int:
    # First find max left
    max_left: int = -1
    max_left_idx: int = -1
    for idx, b_str in enumerate(bank[:-1]):
        b: int = int(b_str)
        if b_str == 9:
            max_left, max_left_idx = 9, idx
            break
        elif b > max_left:
            max_left, max_left_idx = b, idx
    #print(f"max left: {max_left}, idx: {max_left_idx}")

    # Then iterate on reversed list until max_left_idx to find max_right
    max_right: int = -1
    for idx, b_str in reversed(list(enumerate(bank[max_left_idx+1:]))):
        b = int(b_str)
        if b_str == 9:
            max_right = 9
            break
        elif b > max_right:
            max_right = b
    #print(f"max right: {max_right}")

    result = int(str(max_left) + str(max_right))
    #print(f"result: {result}")
    return result

def part_1():
    result = 0
    for line in parse_input("input.txt"):
        result += get_largest_joltage_from_bank(line)
    print(f"Part 1 result: {result}")

@functools.cache
def get_largest_joltage_part2(bank: str, joltage_size: int) -> int:
    if len(bank) == 0 or joltage_size == 0:
        return 0
    current_first: int = int(bank[0])
    # Option 1: we take current number and add the (size-1) next batteries to it
    take_current_option: int = int(str(current_first) + str(get_largest_joltage_part2(bank[1:], joltage_size - 1)))
    # Option 2: we take the (size) next batteries
    move_to_next_batteries_option: int = get_largest_joltage_part2(bank[1:], joltage_size)

    #print(f"Options: current: {take_current_option}, next: {move_to_next_batteries_option}")
    # Recursively try all options: which one is the highest between the case where we take the current first vs we move on to the next ones
    return max(take_current_option, move_to_next_batteries_option)

def part_2():
    result = 0
    for line in parse_input("input.txt"):
        # Need to strip extra 0 (recursion stop case)
        result += int(str(get_largest_joltage_part2(line, 12))[:-1])
    print(f"Part 2 result: {result}")

part_1()
part_2()
