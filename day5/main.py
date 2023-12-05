from pathlib import Path
import re
from functools import reduce

_ROOT = Path(__file__).resolve().parents[0]


def _lookup(seed_index: int, seed_map: map):
    for range_beginning, range_end, range_delta in seed_map:
        if seed_index > range_end:
            continue
        elif seed_index < range_beginning:
            return seed_index
        else:
            return seed_index + range_delta
    return seed_index


def _find_boundary(seed_index_start, seed_index_end, seed_map: map):
    recordset = []
    for range_beginning, range_end, range_delta in seed_map:
        if seed_index_start > range_end or seed_index_end < range_beginning:
            continue

        if seed_index_start < range_beginning:
            recordset += [
                (seed_index_start, range_beginning - 1),
                (
                    range_beginning + range_delta,
                    min(range_end, seed_index_end) + range_delta,
                ),
            ]
        else:
            recordset += [
                (
                    seed_index_start + range_delta,
                    min(range_end, seed_index_end) + range_delta,
                )
            ]

        if range_end > seed_index_end:
            return recordset
        seed_index_start = range_end
    if not recordset:
        recordset = [(seed_index_start, seed_index_end)]
    return recordset


def _process_seed_tuples(seed_tuple, seed_map):
    seed_location = [(seed_tuple[0], seed_tuple[0] + seed_tuple[1])]
    for m in seed_map:
        recordset = []
        for seed_index_start, seed_index_end in seed_location:
            recordset += _find_boundary(seed_index_start, seed_index_end, m)
        seed_location = recordset
    print(min(recordset))
    return min(recordset)[0]


def execute(filename: str):
    with open(Path(_ROOT, "data", filename), "r") as f:
        lines = f.read().rstrip()
        entries = lines.split("\n\n")
        seeds = list(map(int, re.findall(r"\d+", entries[0])))
        seed_map = []
        for entry in entries[1:]:
            temp_map = []
            for line in entry.split("\n")[1:]:
                range_end, range_beginning, range_delta = map(
                    int, re.findall(r"\d+", line)
                )
                temp_map.append(
                    [
                        range_beginning,
                        range_beginning + range_delta - 1,
                        range_end - range_beginning,
                    ]
                )
            seed_map.append(sorted(temp_map))

        locations = [reduce(_lookup, seed_map, seed) for seed in seeds]
        part2 = [
            _process_seed_tuples((seeds[i : i + 2]), seed_map)
            for i in range(0, len(seeds), 2)
        ]
        return min(locations), min(part2)


if __name__ == "__main__":
    print(f"Output: {execute('input.txt')}")
