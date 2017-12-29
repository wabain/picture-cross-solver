import json
import argparse
from itertools import count

import voluptuous


ALLOWED_ITERATIONS = 100


class Puzzle:
    def __init__(self, puzzle):
        validate_puzzle(puzzle)

        self.col_cons = puzzle['constraints']['cols']
        self.col_count = len(self.col_cons)

        self.row_cons = puzzle['constraints']['rows']
        self.row_count = len(self.row_cons)


def solve_puzzle(puzzle):
    grid = [[None] * puzzle.col_count for _ in range(puzzle.row_count)]

    for iteration in count():
        if all(v is not None for row in grid for v in row):
            break

        process_constraints(puzzle=puzzle, grid=grid)

        if iteration >= ALLOWED_ITERATIONS:
            raise RuntimeError('Allowed iterations exceeded')

    print_grid(grid)


def process_constraints(puzzle, grid):
    # rows
    for i, (row, row_cons) in enumerate(zip(grid, puzzle.row_cons)):
        possible = generate_possibilities(entries=row, cons=row_cons)
        assert possible
        for j in range(puzzle.col_count):
            collated_value = find_unanimous(p[j] for p in possible)
            grid[i][j] = collated_value

    # columns
    cols = [[] for _ in range(puzzle.col_count)]
    for row in grid:
        for j, v in enumerate(row):
            cols[j].append(v)

    for j, (col, col_cons) in enumerate(zip(cols, puzzle.col_cons)):
        possible = generate_possibilities(entries=col, cons=col_cons)
        assert possible
        for i in range(puzzle.row_count):
            collated_value = find_unanimous(p[i] for p in possible)
            grid[i][j] = collated_value


def generate_possibilities(entries, cons):
    """Return all possible complete assignments of values given the constraint
    """
    return generate_bounded(entries, cons, 0)


def generate_bounded(entries, cons, start_idx):
    for i in range(start_idx, len(entries)):
        if entries[i] is not None:
            continue

        # Restriction: true
        v_true = list(entries)
        v_true[i] = True

        # Restriction: false
        v_false = list(entries)
        v_false[i] = False

        return generate_bounded(v_true, cons, i + 1) + \
            generate_bounded(v_false, cons, i + 1)

    # Base case: fully assigned
    if is_consistent(entries, cons):
        return [entries]

    return []


def is_consistent(values, cons):
    """Values are consistent with constraints if the shortest
    conceivable runs are *** and the longest are ***"""
    assert all(isinstance(v, bool) for v in values)
    return get_runs(values) == cons


def get_runs(values):
    runs = []
    i = 0
    while i < len(values):
        if not values[i]:
            i += 1
            continue

        run_start = i
        while i < len(values) and values[i]:
            i += 1
        runs.append(i - run_start)
    return runs


def find_unanimous(vals):
    vals = iter(vals)
    found = next(vals, None)
    for v in vals:
        if v != found:
            return None
    return found


def print_grid(grid):
    formatting = {
        False: '✗',
        True: '▓',
        None: '?',
    }
    for row in grid:
        print(*(formatting[value] for value in row), sep='')


def validate_puzzle(puzzle):
    schema = voluptuous.Schema({
        'constraints': {
            'cols': [[int]],
            'rows': [[int]],
        }
    }, required=True)

    schema(puzzle)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('puzzle',
                        help='JSON file describing the puzzle',
                        type=argparse.FileType('r'))

    args = parser.parse_args()

    try:
        puzzle = json.load(args.puzzle)
    finally:
        args.puzzle.close()

    solve_puzzle(Puzzle(puzzle))


if __name__ == '__main__':
    main()
