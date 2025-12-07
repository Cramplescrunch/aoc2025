
from functools import cache

def parse_input(filename: str) -> list[list[str]]:
    with open(filename) as file:
            return [line.rstrip() for line in file]

diagram = parse_input("input.txt")
width, height = len(diagram[0]), len(diagram)

def part_1() -> int:
    beam_idxs = {diagram[0].find('S')}
    split_count = 0
    for i in range(1, height):
        current_beam_idxs = list(beam_idxs)
        line = diagram[i]
        for b in current_beam_idxs:
            if line[b] == "^":
                split_count += 1
                beam_idxs.remove(b)
                left = b - 1
                right = b + 1
                if left >= 0:
                    beam_idxs.add(left)
                if right < width:
                    beam_idxs.add(right)
    return split_count

@cache
def count_routes(node: tuple[int, int]):
    """
    node: tuple of (row,col) representing a beam state

    The idea is that we use recursion + memoization to count the number of possible timelines.
    When processing a node, either:
    - the next row is out of bound: we return 1 to notify we reach and endpoint
    - the beam lands on a splitter: in this case it is split into a left and right beam (if not out of bounds) and we recursively coun the possible timelines for each beams and add them
    - the beams doesn't land on a splitter: we continue on the same column and next row
    Each time we reach an endpoint, we return 1 and these are added up to produce final count.
    A same node can be processed several time through different routes, thus the use of memoization to avoid recomputing it each time.
    """
    row, col = node[0], node[1]
    #print(f"Counting routes for node {node}...")
    if row + 1 == len(diagram):
        return 1
    if diagram[row][col] == "^":
        # Define subsequent nodes
        left, right = (row, col-1), (row, col+1)
        left_count, right_count = 0, 0
        if left[1] >= 0:
            left_count = count_routes(left)
        if right[1] < width:
            right_count = count_routes(right)
        return left_count + right_count
    else:
        return count_routes((row+1, col))

def part_2() -> int:
    return count_routes((0, diagram[0].find('S')))
    

print(part_1())
print(part_2())
                
