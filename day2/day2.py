#!/usr/bin/env python3

import re
from typing import List

def parse_input(filename: str) -> List[str]:
    with open(filename) as file:
        return [line.split(",") for line in file][0]

def process_range_part_1(range_str: str) -> int:
    splitted_range = range_str.split("-")
    start, end = splitted_range[0], splitted_range[1]
    result: int = 0
    for num in range(int(start), int(end)+1, 1):
        num_str = str(num)
        num_len = len(num_str)
        if num_len % 2 == 0 and num_str[:num_len//2] == num_str[num_len//2:]:
            result += num
    return result

def part_1() -> int:
    ranges = parse_input("input.txt")
    result = 0
    for r in ranges:
        result += process_range_part_1(r)
    return result

def process_range_part_2(range_str: str) -> int:
    splitted_range = range_str.split("-")
    start, end = splitted_range[0], splitted_range[1]
    result: int = 0
    for num in range(int(start), int(end)+1, 1):
        num_str = str(num)
        pattern = r"^([0-9]+)\1+$"
        match = re.search(pattern, num_str)
        if match:
            result += num
    return result


def part_2() -> int:
    ranges = parse_input("input.txt")
    result = 0
    for r in ranges:
        result += process_range_part_2(r)
    return result

#print(part_1())
print(part_2())
