#!/usr/bin/env python3

import numpy as np

def parse_input(filename: str) -> list[tuple[int, ...]]:
    with open(filename) as file:
        return [tuple(map(int, line.rstrip().split(","))) for line in file]

def get_distance(p1: tuple[int, ...], p2: tuple[int, ...]) -> float:
    p1_arr = np.array([p1[0], p1[1], p1[2]])
    p2_arr = np.array([p2[0], p2[1], p2[2]])
    squared_dist = np.sum((p1_arr-p2_arr)**2, axis=0)
    return np.sqrt(squared_dist)

class UnionFind:

    def __init__(self, points: list[tuple[int, ...]] | None = None):
        self.parent = []
        self.size = []
        self.id_map = {} # 3D points -> integer ID
        if points:
            for p in points:
                self.make_set(p)

    def _get_id(self, point: tuple[int, ...]) -> int | None:
        if point in self.id_map:
            return self.id_map[point]
        return None

    def make_set(self, point: tuple[int, ...]) -> int:
        existing = self._get_id(point)
        if not existing:
            new_id = len(self.parent)
            self.parent.append(new_id)
            self.size.append(1)
            self.id_map[point] = new_id
            return new_id
        return existing

    def find(self, point: tuple[int, ...] | int) -> int:
        if not isinstance(point, int):
            id = self._get_id(point)
            if id is None:
                id = self.make_set(point)
        else:
            id = point
        if (id is not None) and self.parent[id] != id:
            self.parent[id] = self.find(self.parent[id])
        return self.parent[id]

    def union(self, p1: tuple[int, ...], p2: tuple[int, ...]) -> int:
        id1 = self.find(p1)
        id2 = self.find(p2)

        if id1 == id2:
            return False

        if self.size[id1] < self.size[id2]:
            self.size[id2] += self.size[id1]
            self.parent[id1] = self.parent[id2]
        else:
            self.size[id1] += self.size[id2]
            self.parent[id2] = self.parent[id1]
        return True

    def part1(self) -> int:
        # Find three largest circuits
        size_desc = self.size.copy()
        size_desc.sort(reverse=True)
        return size_desc[0] * size_desc[1] * size_desc[2]

    def union_p2(self, p1: tuple[int, ...], p2: tuple[int, ...], total_points_count: int) -> int | bool:
        id1 = self.find(p1)
        id2 = self.find(p2)

        #print(f"Connecting {p1} (id: {id1}) and {p2} (id: {id2})")
        if id1 == id2:
            return False

        if self.size[id1] < self.size[id2]:
            self.size[id2] += self.size[id1]
            self.parent[id1] = self.parent[id2]
            if self.size[id2] == total_points_count:
                print(f"size matched! p1={p1}, p2={p2}")
                return p1[0] * p2[0]
        else:
            self.size[id1] += self.size[id2]
            self.parent[id2] = self.parent[id1]
            if self.size[id1] == total_points_count:
                print(f"size matched! p1={p1}, p2={p2}")
                return p1[0] * p2[0]
        return True

def part_1() -> int:
    # First we need to compute distances for every point
    # Distances will be stored in a list along with their two points
    # Points are represented by a tuple (or list) of two points (tuples)
    points = parse_input("input.txt")
    circuits = UnionFind(points)
    distances = []
    for idx, p1 in enumerate(points):
        for p2 in points[idx+1:]:
            distances.append([get_distance(p1, p2), p1, p2])
    sorted_distances = sorted(distances, key = lambda d: d[0])
    closest_pairs = sorted_distances[:1000]
    for _, p1, p2 in closest_pairs:
        circuits.union(p1, p2)
    return circuits.part1()

def part_2() -> int:
    # First we need to compute distances for every point
    # Distances will be stored in a list along with their two points
    # Points are represented by a tuple (or list) of two points (tuples)
    points = parse_input("input.txt")
    total_points_count = len(points)
    circuits = UnionFind(points)
    distances = []
    for idx, p1 in enumerate(points):
        for p2 in points[idx+1:]:
            distances.append([get_distance(p1, p2), p1, p2])
    sorted_distances = sorted(distances, key = lambda d: d[0])
    for _, p1, p2 in sorted_distances:
        result = circuits.union_p2(p1, p2, total_points_count)
        if not isinstance(result, bool):
            return result
    return 0

print(part_1())
print(part_2())
