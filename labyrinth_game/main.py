#!/usr/bin/venv python3

from labyrinth_game.constants import ROOMS # import of room constants
from labyrinth_game.utils import describe_current_room
from labyrinth_game.player_actions import get_input

game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Значения окончания игры
    'steps_taken': 0  # Количество шагов
}


def main():
    # starting message
    print("Добро пожаловать в Лабиринт сокровищ!")

    # describe current room
    describe_current_room(game_state)

    while True:
        player_input = get_input()
