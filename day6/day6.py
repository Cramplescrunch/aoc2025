#!/usr/bin/env python3

from functools import reduce


def parse_input(filename: str) -> list[list[str]]:
    result = []
    with open(filename) as file:
        for line in file:
            result.append(line.split())
    return result


def part_1() -> int:
    input: list[list[str]] = parse_input("input.txt")
    nb_rows = len(input)
    nb_cols = len(input[0])
    sum = 0
    for i in range(nb_cols):
        operator = input[nb_rows - 1][i]
        nums: list[int] = []
        res_row: int = 0
        for j in range(nb_rows - 1):
            nums.append(int(input[j][i]))
        if operator == "*":
            res_row = reduce(lambda x, y: x * y, nums)
        elif operator == "+":
            res_row = reduce(lambda x, y: x + y, nums)
        sum += res_row
    return sum

def parse_input_p2(filename: str) -> list[list[str]]:
    """
    First we parse the input to retrieve numbers for each lines with whitespaces preserved
    """
    result = []
    file = []
    with open(filename) as file_buf:
        for line in file_buf:
            file.append(line)

    nb_rows: int = len(file)
    first_line = file[0]
    cut_indexes: list[int] = []
    for i in range(len(first_line)):
        if first_line[i] == " ":
            is_cutting_idx = True
            for j in range(1, nb_rows):
                if file[j][i] != " ":
                    is_cutting_idx = False
                    break
            if is_cutting_idx:
                cut_indexes.append(i)
    for i in range(nb_rows):
        row_nums: list[str] = []
        line: str = file[i]
        prev_idx = 0
        for idx in cut_indexes:
            if prev_idx == 0:
                row_nums.append(line[:idx])
            else:
                row_nums.append(line[(prev_idx + 1):idx])
            prev_idx = idx
        row_nums.append(line[(prev_idx + 1):-1])
        result.append(row_nums)
    return result

def compute_p2_col(col_nums: list[str], operator: str) -> int:
    """
    col_nums are all the numbers for a column with whitespace preserved!
    """
    nums: list[int] = []
    max_num_len: int = max(map(lambda x: len(x), col_nums))
    for i in reversed(range(max_num_len)):
        digits: list[str] = []
        for j in range(len(col_nums)):
            try:
                digits.append(col_nums[j][i])
            except Exception:
                # Ignore index out of range
                pass
        nums.append(int(reduce(lambda x,y: x+y, digits)))
    if operator == "*":
        return reduce(lambda x, y: x * y, nums)
    elif operator == "+":
        return reduce(lambda x, y: x + y, nums)
    # Should never occur
    return 0

def part_2() -> int:
    input: list[list[str]] = parse_input_p2("input.txt")
    nb_rows = len(input)
    nb_cols = len(input[0])
    sum = 0
    for i in range(nb_cols):
        operator = input[nb_rows - 1][i].strip()
        col_nums = []
        for j in range(nb_rows - 1):
            col_nums.append(input[j][i])
        sum += compute_p2_col(col_nums, operator)
    return sum


#print(part_1())
print(part_2())
