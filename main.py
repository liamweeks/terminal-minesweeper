import getch
import random
import os
from typing import List
import math


def get_char() -> str:
    return getch.getch()


def colour_text(text: str, r: int, g: int, b: int) -> str:
    # convert rgb to ANSI 256-colour code
    colour_code = 16 + (36 * r // 256) + (6 * g // 255) + (b // 255)
    end_colour = '\033[0m'
    return f"\033[38;5;{colour_code}m{text}{end_colour}"


def get_command(char: str) -> str:
    match char:
        case "w":
            return "up"
        case "a":
            return "left"
        case "s":
            return "down"
        case "d":
            return "right"

        case "l":
            return "flag"

        case "k":
            return "open"

        case 'j':
            return 'debug'


def find_adjacent_tiles(tile: tuple[int]) -> List[tuple[int]]:
    x = tile[0]
    y = tile[1]

    adjacent_tiles: List[(int, int)] = [
        # 1 2 3
        # 4 T 5
        # 6 7 8

        (x - 1, y - 1),  # 1
        (x, y - 1),  # 2
        (x + 1, y - 1),  # 3
        (x - 1, y),  # 4
        (x + 1, y),  # 5
        (x - 1, y + 1),  # 6
        (x, y + 1),  # 7
        (x + 1, y + 1),  # 8
    ]

    return adjacent_tiles


def find_empty_tiles(active_tile: (int, int)) -> List[tuple[int, int]]:
    tiles_to_clear = [active_tile]

    while not (len(tiles_to_clear) == 0):
        for _tile in tiles_to_clear:
            tile = tiles_to_clear.pop()
            adjacent_mines = count_adjacent_mines(tile, mines)

            if adjacent_mines > 0:
                tiles_to_search = find_adjacent_tiles(tile)
                tiles_to_clear += tiles_to_search
            else:
                return tiles_to_clear

    return tiles_to_clear.append(active_tile)


def move_active_tile(active_tile: (int, int), direction: str) -> tuple[int, int]:
    tile_x = active_tile[0]
    tile_y = active_tile[1]
    match direction:
        case "up":
            tile_y -= 1
        case "down":
            tile_y += 1
        case "right":
            tile_x += 1
        case "left":
            tile_x -= 1
        case _:
            pass

    return (tile_x, tile_y)


def count_adjacent_mines(active_tile: (int, int), coordinates_of_mines: List[tuple]) -> int:
    x = active_tile[0]
    y = active_tile[1]
    adjacent_tiles: List[(int, int)] = [
        # 1 2 3
        # 4 5 6
        # 7 8 9

        (x - 1, y - 1),  # 1
        (x, y - 1),  # 2
        (x + 1, y - 1),  # 3
        (x - 1, y),  # 4
        (x + 1, y),  # 6
        (x - 1, y + 1),  # 7
        (x, y + 1),  # 8
        (x + 1, y + 1),  # 9
    ]

    mines = 0

    for tile in adjacent_tiles:
        if tile in coordinates_of_mines:
            mines += 1

    return mines


if __name__ == "__main__":

    width = 16
    height = 16
    mines = 40

    directions = [
        "up",
        "down",
        "left",
        "right"
    ]

    actions = [
        'open',
        'flag',
        'debug'
    ]

    board = [(x, y) for y in range(height) for x in range(width)]
    mines = [coordinate for coordinate in random.sample(board, mines)]
    uncovered_mines = 0
    flagged = []
    # uncovered_tiles = []
    game_over = False
    show_mines = False

    centre_x = width // 2
    centre_y = height // 2

    active_tile = (centre_x, centre_y)
    empty_tiles: List[tuple[int, int]] = []

    while True:
        for index, coordinate in enumerate(board):
            mines_around = count_adjacent_mines(coordinate, mines)
            display_mine_num = ' ' if mines_around == 0 else mines_around

            symbol = 'C'

            # <minesweeper logic>

            # if (coordinate in uncovered_tiles) and not (coordinate in mines):
            #     symbol = f'{display_mine_num}'

            if (coordinate in empty_tiles) and not (coordinate in mines):
                symbol = display_mine_num

            if coordinate in flagged:
                symbol = colour_text('F', 255, 0, 0)

            # </minesweeper logic>

            if coordinate in mines and show_mines:
                symbol = colour_text('M', 255, 0, 0)

            if coordinate == active_tile:
                symbol = f'[{symbol}]'
            else:
                symbol = f' {symbol} '

            if (coordinate in empty_tiles) and not (coordinate in mines):  # if coordinate in uncovered_tiles:
                match mines_around:
                    case 1:
                        symbol = colour_text(symbol, 0, 220, 0)
                    case 2:
                        symbol = colour_text(symbol, 50, 214, 9)
                    case 3:
                        symbol = colour_text(symbol, 161, 3, 252)
                    case 4:
                        symbol = colour_text(symbol, 0, 0, 220)
                    case 5:
                        symbol = colour_text(symbol, 255, 255, 255)
                    case 6:
                        symbol = colour_text(symbol, 252, 3, 3)
                    case 7:
                        symbol = colour_text(symbol, 214, 214, 9)
                    case 8:
                        symbol = colour_text(symbol, 0, 220, 0)
                    case _:
                        pass

            print(symbol, end=colour_text('|', 0, 0, 0))

            if index % width == width - 1:
                print('')
                print(colour_text('--', 0, 0, 0) * width * 2)

        message: str = ''
        if active_tile in empty_tiles:
            message = 'in uncovered_tiles'
        else:
            message = 'missing from uncovered_tiles'
        print(f"{active_tile} {message}")
        char = get_char()
        os.system("clear" if os.name == "posix" else "cls")
        command = get_command(char)

        if command in directions:
            active_tile = move_active_tile(active_tile, command)
        elif command in actions:
            match command:
                case "open":
                    if active_tile in mines:
                        game_over = True
                        print("GAME OVER")
                        show_mines = True
                    elif active_tile in empty_tiles:
                        # TODO: logic for when someone opens an empty mine
                        empty_tiles += find_empty_tiles(active_tile)
                        pass

                    empty_tiles += find_empty_tiles(active_tile)
                    # empty_tiles += active_tile
                case "flag":
                    if active_tile in flagged:
                        flagged.pop()
                        # uncovered_tiles += active_tile
                        empty_tiles += active_tile
                    else:
                        flagged.append(active_tile)

                case 'debug':
                    show_mines = not show_mines

                case _:
                    pass
