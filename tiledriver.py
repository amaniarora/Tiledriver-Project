# Name:         Amani Arora
# Course:       CPE 202
# Instructor:   Daniel Kauffman
# Assignment:   Tile Driver
# Term:         Spring 2021

import random
from typing import List, Tuple, Optional


class PuzzleState:  # do not modify

    def __init__(self, tiles: Tuple[int, ...], path: str) -> None:
        self.tiles = tiles
        self.width = int(len(tiles) ** 0.5)
        self.path = path

    def __eq__(self, other: "PuzzleState") -> bool:
        return self.tiles == other.tiles and self.path == other.path

    def __repr__(self) -> str:
        return self.path


#make_adjacent


def make_adjacent(state: PuzzleState) -> List[PuzzleState]:
    """
    Return a list of PuzzleState objects that represent valid, non-opposing
    moves from the given PuzzleState. A move is considered valid if it moves a
    tile adjacent to the blank tile into the blank tile. A move is considered
    non-opposing if it does not undo the previous move.

    >>> state = PuzzleState((3, 2, 1, 0), "")
    >>> make_adjacent(state)
    [PuzzleState((3, 0, 1, 2), "J"), PuzzleState((3, 2, 0, 1), "L")]
    """
    moves = []
    start_tiles = list(state.tiles)
    blank = start_tiles.index(0)
    total_tiles = len(start_tiles)
    up = blank + state.width
    down = blank - state.width
    left = blank + 1
    right = blank - 1
    directions = [up, down, left, right]
    direction_str = ["K", "J", "H", "L"]
    for m in range(4):
        if valid(directions, m, blank, state.width, total_tiles) is True:
            if non_opposing(m, state.path) is True:
                entry = new_entry(start_tiles, direction_str[m],
                                  directions[m], blank, state.path)
                moves.append(entry)
        start_tiles = list(state.tiles)
    return moves


def swap(lst: List[int], x: int, y: int) -> List[int]:
    tmp = lst[x]
    lst[x] = lst[y]
    lst[y] = tmp
    return lst


def new_entry(tiles: List[int], direction_str: str,
                     direction_index: int, blank_index: int,
                     initial_path: str) -> PuzzleState:
    new = swap(tiles, direction_index, blank_index)
    entry = PuzzleState(tuple(new), initial_path + direction_str)
    return entry


def valid(directions: List[int],
          index: int, blank: int,
          width: int, total_tiles: int) -> bool:
    if index == 0:
        if directions[index] < total_tiles:
            if blank % width == directions[index] % width:
                return True
    if index == 1:
        if directions[index] >= 0:
            if blank % width == directions[index] % width:
                return True
    if index == 2:
        if directions[index] < total_tiles:
            if blank // width == directions[index] // width:
                return True
    if index == 3:
        if directions[index] >= 0:
            if blank // width == directions[index] // width:
                return True
    return False


def non_opposing(index: int, path: str) -> bool:
    if path == '':
        return True
    if index == 0:
        if path[-1] != 'J':
            return True
    if index == 1:
        if path[-1] != 'K':
            return True
    if index == 2:
        if path[-1] != 'L':
            return True
    if index == 3:
        if path[-1] != 'H':
            return True
    return False


#determine solvability


def is_solvable(tiles: Tuple[int, ...]) -> bool:
    """
    Return a Boolean indicating whether the given tuple represents a solvable
    puzzle. Use the Merge Sort algorithm (possibly in a helper function) to
    efficiently count the number of inversions.

    >>> is_solvable((3, 2, 1, 0))
    True
    >>> is_solvable((0, 2, 1, 3))
    False
    """
    blank = tiles.index(0)
    width = int(len(tiles) ** 0.5)
    blank_row = blank // width
    tiles_lst = list(tiles)
    tiles_lst.pop(blank)
    inversions = merge_sort_starter(tiles_lst, len(tiles_lst))
    if width % 2 == 1:
        if inversions % 2 == 0:
            return True
    else:
        if blank_row % 2 == 0:
            if inversions % 2 == 0:
                return True
        else:
            if inversions % 2 == 1:
                return True
    return False


def merge_sort_starter(new: List[int], length: int) -> int:
    hold = [0] * length
    return merge_sort(new, hold, 0, length - 1)


def merge_sort(new: List[int], hold: List[int],
               left: int, right: int) -> int:
    inversions = 0
    if right > left:
        mid = (left + right) // 2
        inversions += merge_sort(new, hold, left, mid)
        inversions += merge_sort(new, hold, mid + 1, right)
        inversions += merge(new, hold, left, mid, right)
    return inversions


def merge(new: List[int], hold: List[int],
          left: int, mid: int, right: int) -> int:
    start_left = left
    start_right = mid + 1
    start_sorted = left
    inversions = 0
    while start_left <= mid and start_right <= right:
        if new[start_left] <= new[start_right]:
            hold[start_sorted] = new[start_left]
            start_sorted += 1
            start_left += 1
        else:
            hold[start_sorted] = new[start_right]
            val = (mid - start_left + 1)
            inversions += val
            start_sorted += 1
            start_right += 1
    while start_left <= mid:
        hold[start_sorted] = new[start_left]
        start_sorted += 1
        start_left += 1
    while start_right <= right:
        hold[start_sorted] = new[start_right]
        start_sorted += 1
        start_right += 1
    for m in range(left, right + 1):
        new[m] = hold[m]
    return inversions

#solve

def solve_puzzle(tiles: Tuple[int, ...]) -> str:
    """
    Return a string (containing characters "H", "J", "K", "L") representing the
    optimal number of moves to solve the given puzzle using Uniform Cost Search.
    A state is considered a solution if its tiles are sorted.

    >>> solve_puzzle((3, 2, 1, 0))
    "JLKHJL"
    """
    tiles_list = list(tiles)
    endgoal = insertion_sort(tiles_list)
    start = PuzzleState(tiles, '')
    path = uniform_cost_search(start, tuple(endgoal), explored=[])
    return path


def uniform_cost_search(start: PuzzleState, endgoal: Tuple,
                        explored: List[PuzzleState]) -> Optional[str]:
    queue = []
    queue.append(start)
    while bool(queue) is True:
        current = queue.pop(0)
        explored.append(current)
        if current.tiles == endgoal:
            return current.path
        else:
            moves = make_adjacent(current)
            for move in moves:
                if in_explored(move, explored) is False:
                    queue = queue_processing(queue, move)
                    queue = insertion_sort_puzzles(queue)
    return None


def in_explored(move: PuzzleState, explored: List[PuzzleState]) -> bool:
    for item in explored:
        if item.tiles == move.tiles:
            return True
    return False


def queue_processing(queue: List[PuzzleState],
                     move: PuzzleState) -> List[PuzzleState]:
    for k in range(len(queue)):
        if queue[k].tiles == move.tiles:
            if len(queue[k].path) > len(move.path):
                queue.pop(k)
                queue.append(move)
                return queue
            else:
                return queue
    queue.append(move)
    return queue


def insertion_sort_puzzles(puzzles: List[PuzzleState]) -> List[PuzzleState]:
    for index in range(1, len(puzzles)):
        cur_val = len(puzzles[index].path)
        pos = index
        while pos > 0 and len(puzzles[pos - 1].path) > cur_val:
            hold = puzzles[pos]
            puzzles[pos] = puzzles[pos - 1]
            puzzles[pos - 1] = hold
            pos -= 1
    return puzzles



def insertion_sort(lst: List[int]) -> List[int]:
    for index in range(1, len(lst)):
        cur_val = lst[index]
        pos = index
        while pos > 0 and lst[pos - 1] > cur_val:
            lst[pos] = lst[pos - 1]
            pos -= 1
            lst[pos] = cur_val
    return lst







def main() -> None:
    random.seed(int(input("Random Seed: ")))
    tiles = list(range(int(input("Puzzle Width: ")) ** 2))  # use 2 or 3
    random.shuffle(tiles)
    print("Tiles:", "[", " ".join(str(t) for t in tiles), "]")
    if not is_solvable(tuple(tiles)):
        print("Unsolvable")
    else:
        print("Solution:", solve_puzzle(tuple(tiles)))


if __name__ == "__main__":
    main()
