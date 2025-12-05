#!/usr/bin/env python3

def parse_input(filename: str) -> tuple[list[list[int]], list[int]]:
    ranges: list[list[int]] = []
    ingredients: list[int] = []
    with open(filename) as file:
        for line in file:
            if "-" in line:
                ranges.append(list(map(int, line.rstrip().split("-"))))
            elif not line.isspace():
                ingredients.append(int(line.rstrip()))
    return ranges, ingredients

def part_1() -> int:
    ranges, ingredients = parse_input("input.txt")
    count: int = 0
    for i in ingredients:
        for r in ranges:
            start, stop = r[0], r[1]
            if start <= i and i <= stop:
                count += 1
                break
    return count

def merge_range(r: list[int], sorted_ranges: list[list[int]]) -> list[int]:
    merged_range = []
    next_range = sorted_ranges[0]
    if next_range[0] <= r[1]:
        merged_range = [r[0], next_range[1]]
    else:
        merged_range = r
    if len(sorted_ranges) <= 1:
        return r
    return merge_range(merged_range, sorted_ranges[1:])

def dedup_ranges(ranges: list[list[int]]) -> list[list[int]]:
    merged = [ranges[0]]

    for r in ranges[1:]:
        if r[0] <= merged[-1][1]:
            merged[-1][1] = max(r[1], merged[-1][1])
        else:
            merged.append(r)
    return merged


def part_2() -> int:
    ranges, _ = parse_input("input.txt")
    count = 0
    # Need to merge/dedup ranges
    sorted_ranges = sorted(ranges, key=lambda r: r[0])
    deduped_ranges = dedup_ranges(sorted_ranges)
    for r in deduped_ranges:
        start, stop = r[0], r[1]
        count += stop - start + 1
    return count

print(part_1())
print(part_2())
