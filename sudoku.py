#!/usr/bin/env python3
import argparse
import logging
from typing import List

import sys


# default_file = './puzzles/sudoku-com-hard-20221206T153200.txt'
default_file = './puzzles/rps-20221103.txt'


def parse_args():
    parser = argparse.ArgumentParser(__file__.replace('.py', '').split('/')[-1])
    parser.add_argument('-f', '--file', default=default_file, help='Sudoko starting board file', type=str)
    parser.add_argument('-ll', '--log-level', default='INFO', help='Logging level')
    return parser.parse_args()


args = parse_args()
log_level = args.log_level.upper()
logger = logging.getLogger(__file__.split('/')[-1].replace('.py', ''))
logger.setLevel(log_level)
ch = logging.StreamHandler()
ch.setLevel(log_level)
formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)d - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_rows(path) -> List[List[int]]:
    with open(path, 'r') as f:
        txt = [*filter(
            lambda x: len(x) and x[0] != "#",
            map(str.strip, f.readlines())
        )]
    assert len(txt) == 9, 'Malformed sudoku grid, needs 9 rows'
    g = [[0 for _ in range(9)] for _ in range(9)]
    for i, line in enumerate(txt):
        chars = line.strip().split(',')
        assert len(chars) == 9, 'Malformed sudoku row %d needs 9 cells' % i
        for j, c in enumerate(chars):
            if c.isnumeric():
                g[i][j] = int(c)
    assert len(g) == 9, f'invalid grid len {len(g)}'
    return g


def find_next_cell_to_fill(grid, i, j):
    for x in range(i, 9):
        for y in range(j, 9):
            if grid[x][y] == 0:
                return x, y
    for x in range(0, 9):
        for y in range(0, 9):
            if grid[x][y] == 0:
                return x, y
    logger.info("")
    return -1, -1


def is_valid(grid, i, j, e):
    if all([e != grid[i][x] for x in range(9)]):
        if all([e != grid[x][j] for x in range(9)]):
            # finding the top left x,y co-ordinates of the section containing the i,j cell
            sec_top_x, sec_top_y = 3 * (i // 3), 3 * (j // 3)
            for x in range(sec_top_x, sec_top_x + 3):
                for y in range(sec_top_y, sec_top_y + 3):
                    if grid[x][y] == e:
                        return False
            return True
    return False


def solve_grid(grid, i=0, j=0):
    i, j = find_next_cell_to_fill(grid, i, j)
    if i == -1:
        return True
    for e in range(1, 10):
        if is_valid(grid, i, j, e):
            grid[i][j] = e
            if solve_grid(grid, i, j):
                return True
            # Undo the current cell for backtracking
            grid[i][j] = 0
    return False


def print_board(g):
    return "\n".join(map(str, g))


def main():
    grid: List[List[int]] = get_rows(args.file)
    logger.info("starting grid:\n" + print_board(grid))
    if solve_grid(grid):
        logger.info("solved grid:\n" + print_board(grid))
        return
    else:
        raise Exception("unable to solve grid")


if __name__ == '__main__':
    sys.exit(main())
