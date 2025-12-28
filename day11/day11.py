#!/usr/bin/env python3
import time
import functools

def parse_input(filename: str) -> dict[str, list[str]]:
    res = {}
    with open(filename) as file:
        for line in file:
            splitted = line.split(":")
            children = []
            for s in splitted[1].split(" "):
                c = s.strip()
                if c:
                    children.append(c)
            res[splitted[0]] = children
    return res

def part_1() -> int:
    graph = parse_input("input.txt")
    # Apply BFS to count paths that lead from 'you' to 'out'
    count = 0
    q = [graph['you']]
    while q:
        current: list[str] = q.pop(0)
        children: list[list[str]] = []
        for child in current:
            children.append(child)
        if 'out' in children:
            count += 1
        else:
            for child in children:
                q.append(graph[child])
    return count

# Part 2
# Here we use recursive DFS + caching
# The trick is to 'memorize' if we passed through fft and dac with a bitmask
# bitmask = 1 -> passed through fft
# bitmask = 2 -> passed through dac
# bitmask = 3 -> passed through both
@functools.cache
def dfs(node: str, bitmask: int) -> int:
    if node == 'out' and bitmask == 3:
        return 1
    elif node == 'out' or not graph[node]:
        return 0

    sum = 0
    new_bitmask = bitmask
    if node == 'fft':
        new_bitmask += 1
    elif node == 'dac':
        new_bitmask +=2
    for child in graph[node]:
        sum += dfs(child, new_bitmask)
    return sum

def part_2() -> int:
    return dfs('svr', 0)

graph = parse_input("input.txt")

start_time = time.time()
print(f"Part 1: {part_1()}")
print(f"Elapsed time: {time.time() - start_time} seconds")

start_time = time.time()
print(f"Part 2: {part_2()}")
print(f"Elapsed time: {time.time() - start_time} seconds")
