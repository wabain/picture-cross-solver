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
            break

    print_grid(grid)


def process_constraints(puzzle, grid):
    for row, row_cons in zip(puzzle.row_cons, grid):
        possible = generate_possibilities(entries=row, cons=row_cons)
        assert possible
        collated = [
            find_unanimous(p[i] for p in possible)
            for i in range(len(row))
        ]
        if len(possible) == 1:
            pass


def generate_possibilities(entries, cons):
    return [entries]


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
