#!/usr/bin/env python3
import re

class Area():
    def __init__(self, area: int, presents: list[int]):
        self.area = area
        self.presents = presents

class Present():
    def __init__(
            self,
            shape: list[list[str]],
            area: int,
            box_area: int
    ):
        self.shape = shape
        self.area = area
        self.box_area = box_area

class Input():
    def __init__(
            self,
            presents: dict[int, Present],
            areas: list[Area]
    ):
        self.presents = presents
        self.areas = areas

def count_present_area(p: list[list[str]]) -> int:
    area = 0
    for r in p:
        for cell in r:
            if cell == '#':
                area +=1
    return area

def count_present_box_area(p: list[list[str]]) -> int:
    return len(p) * len(p[0])

def parse_input(filename: str) -> Input:
    with open(filename) as file:
        presents = {}
        current_pres = 0
        present_num_re = r"^([0-9]):"
        present_shape_re= r"[#.]+"
        first_area_idx = None
        areas = []
        area_re = r"^([0-9]+)x([0-9]+):(.*)"
        for idx, line in enumerate(file):
            match_pres_num = re.search(present_num_re, line)
            match_pres_shape = re.search(present_shape_re, line)
            match_area = re.search(area_re, line)
            if match_pres_num:
                current_pres = int(match_pres_num[1])
                if not current_pres in presents:
                    presents[current_pres] = []
            elif match_pres_shape:
                presents[current_pres].append([c for c in line.split()[0]])
            elif match_area:
                if not first_area_idx:
                    first_area_idx = idx
                area = int(match_area[1]) * int(match_area[2])
                area_presents = list(map(int, match_area[3].split()))
                areas.append(Area(area, area_presents))

        final_presents = {}
        for p in presents:
            pres = Present(presents[p],
                           count_present_area(presents[p]),
                           count_present_box_area(presents[p]))
            final_presents[p] = pres
        return Input(final_presents, areas)

def get_compacted_presents_area(region: Area, presents: dict[int, Present]) -> int:
    area = 0
    for idx, p in enumerate(region.presents):
        area += p * presents[idx].area
    return area

def get_expanded_presents_area(region: Area, presents: dict[int, Present]) -> int:
    area = 0
    for idx, p in enumerate(region.presents):
        area += p * presents[idx].box_area
    return area

def can_fit_presents(area: Area, presents: dict[int, Present]) -> bool:
    #print(f"area={area.area}")
    # If area is smaller than most compacted presents -> False
    compacted_pres_area = get_compacted_presents_area(area, presents)
    #print(f"compacted_presents={compacted_pres_area}")
    if area.area < compacted_pres_area:
        return False
    # If area is bigger than most expanded presents -> True
    expanded_pres_area = get_expanded_presents_area(area, presents)
    #print(f"expanded_presents={expanded_pres_area}")
    if area.area >= expanded_pres_area:
        return True
    # Else you are fucked
    print(f"Can't decide, returning false (area={area.area}, compacted={compacted_pres_area}, expanded={expanded_pres_area})")
    return False

def part_1() -> int:
    input = parse_input("input.txt")
    presents = input.presents
    sum = 0
    for area in input.areas:
        if can_fit_presents(area, presents):
            sum += 1
    return sum

print(part_1())
