#!/usr/bin/venv python3

from labyrinth_game.constants import ROOMS # import of room constants
from labyrinth_game.utils import describe_current_room, solve_puzzle, show_help#, attempt_open_treasure
from labyrinth_game.player_actions import get_input, move_player, take_item, use_item

def process_command(game_state, command):
    user_input = command.split()

    match user_input[0]:
        case 'look':
            describe_current_room(game_state)
        case 'go':
            direction = user_input[1]
            move_player(game_state, direction)
        case 'take':
            item_name = user_input[1]
            take_item(game_state, item_name)
        case 'use':
            item_to_use = user_input[1]
            use_item(game_state, item_to_use)
        case "quit" | "exit" | "q" | "stop":
            print("Спасибо за игру! До свидания.")
            game_state["game_over"] = True
        case 'solve':
            solve_puzzle(game_state)
        case 'help':
            show_help()
        case "inventory":
            print(game_state["player_inventory"])
        case _:
            print(f"Неизвестная комманда: '{command}'. Введите 'help' для вывода списка команд.")


def main():
    # initializing game state dict
    game_state = {
        'player_inventory': [],  # Инвентарь игрока
        'current_room': 'entrance',  # Текущая комната
        'game_over': False,  # Значения окончания игры
        'steps_taken': 0  # Количество шагов
    }
    # starting message
    print("Добро пожаловать в Лабиринт сокровищ!")

    # describe starting room
    describe_current_room(game_state)

    while not game_state["game_over"]:
        player_input = get_input("\nЧто вы хотите сделать?\n> ")
        process_command(game_state, player_input)
