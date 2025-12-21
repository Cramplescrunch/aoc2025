#!/usr/bin/env python3
import matplotlib.pyplot as plt

def parse_input(filename: str) -> list[tuple[int, ...]]:
    with open(filename) as file:
        return [tuple(map(int, line.rstrip().split(","))) for line in file]

def get_area(p1: tuple[int, ...], p2: tuple[int, ...]) -> int:
    area = (abs((p2[1] - p1[1])) + 1) * (abs((p2[0] - p1[0])) + 1)
    return area

def part_1() -> int:
    points = parse_input("input.txt")
    max_area = 0
    for idx, p1 in enumerate(points):
        for p2 in points[idx+1:]:
            max_area = max(max_area, get_area(p1, p2))
    return max_area

class CompressedPoints:
    def __init__(self, cpoints, x_map, y_map):
        self.points = cpoints
        self.x_map = x_map
        self.y_map = y_map

def compress_points(points: list[tuple[int, ...]]) -> CompressedPoints:
    Xs, Ys = [], []
    for p in points:
        Xs.append(p[0])
        Ys.append(p[1])
    Xs, Ys = sorted(set(Xs)), sorted(set(Ys))
    # map index -> actual coordinate
    x_map, y_map, rev_x_map, rev_y_map = {}, {}, {}, {}
    compressed_points = []
    for i in range(len(Xs)):
        x_val, y_val = Xs[i], Ys[i]
        x_map[i] = x_val
        y_map[i] = y_val
        rev_x_map[x_val] = i
        rev_y_map[y_val] = i
    for p in points:
        px, py = p[0], p[1]
        compressed_points.append(tuple([rev_x_map[px], rev_y_map[py]]))
    return CompressedPoints(compressed_points, x_map, y_map)

def init_matrix(points: list[tuple[int, ...]]) -> list[list[int]]:
    min_x, min_y, max_x, max_y = points[0][0], points[0][1], 0, 0
    for p in points:
        min_x, min_y = min(min_x, p[0]), min(min_y, p[1])
        max_x, max_y = max(max_x, p[0]), max(max_y, p[1])
    matrix = [[0] * (max_x+1) for i in range(max_y+1)]
    for p in points:
        matrix[p[1]][p[0]] = 1
    return matrix


def connect_edges_and_fill(omatrix: list[list[int]]) -> list[list[int]]:
    front = set()
    matrix = omatrix.copy()
    for y in range(len(matrix)):
        hfill = False
        sorted_front = sorted(list(front))
        ranges = []
        while sorted_front:
            ranges.append(range(sorted_front[0], sorted_front[1]))
            sorted_front = sorted_front[2:]
        for idx, x in enumerate(matrix[y]):
            # Vertical fill based on previous front
            if idx in front and matrix[y][idx] == 0:
                matrix[y][idx] = 1

            # Inside fill
            for r in ranges:
                if idx in r:
                    matrix[y][idx] = 1

            # Horizontal fill + front computation
            if x == 1:
                hfill = not hfill
                if idx not in front:
                    front.add(idx)
                else:
                    front.remove(idx)
            elif hfill:
                matrix[y][idx] = 1
    return matrix

def is_rect_in_polygon(
        p1: tuple[int, ...],
        p2: tuple[int, ...],
        matrix: list[list[int]]
) -> bool:
    min_x, min_y, max_x, max_y = min(p1[0], p2[0]), min(p1[1], p2[1]), max(p1[0], p2[0]), max(p1[1], p2[1])
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if matrix[y][x] == 0:
                return False
    return True

def get_max_inside_area(
        compressed_points: CompressedPoints,
        matrix: list[list[int]]
):
    max_area = 0
    cpoints = compressed_points.points
    x_map, y_map = compressed_points.x_map, compressed_points.y_map
    for idx, p1 in enumerate(cpoints):
        for p2 in cpoints[idx+1:]:
            actual_p1 = (x_map[p1[0]], y_map[p1[1]])
            actual_p2 = (x_map[p2[0]], y_map[p2[1]])
            area = get_area(actual_p1, actual_p2)
            if area > max_area and is_rect_in_polygon(p1, p2, matrix):
                max_area = max(max_area, area)
    return max_area

def display_matrix(mat: list[list[int]]):
    for i in range(len(mat)):
        print(mat[i])
    #plt.matshow(mat)
    #plt.show()

def part_2() -> int:
    points = parse_input("input.txt")
    cpoints_obj = compress_points(points)
    cpoints = cpoints_obj.points
    matrix = connect_edges_and_fill(init_matrix(cpoints))
    #display_matrix(matrix)
    return get_max_inside_area(cpoints_obj, matrix)

#print(part_1())
print(part_2())
