#!/usr/bin/venv python3

from labyrinth_game.constants import ROOMS # import of room constants

game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Значения окончания игры
    'steps_taken': 0  # Количество шагов
}


def main():
    print("Первая попытка запустить проект!")
