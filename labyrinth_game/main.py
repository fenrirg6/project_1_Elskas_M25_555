#!/usr/bin/venv python3

from labyrinth_game.constants import ROOMS # import of room constants
from labyrinth_game.utils import describe_current_room, solve_puzzle, show_help, attempt_open_treasure
from labyrinth_game.player_actions import get_input, move_player, take_item, use_item

def process_command(game_state, command):
    user_input = command.split()
    if not user_input:
        print("Введите команду. Наберите 'help' для списка команд.")
        return
    command = user_input[0]

    # 3.2. Движение по односложным командам
    simple_dirs = ["north", "south", "east", "west"]
    if command in simple_dirs:
        move_player(game_state, command)
        return

    match command:
        case 'look':
            describe_current_room(game_state)
        case 'go':
            if len(user_input) < 2:
                print("Укажите направление (north/south/east/west).")
            else:
                direction = user_input[1]
                move_player(game_state, direction)
        case 'take':
            if len(user_input) < 2:
                print("Укажите предмет, который хотите поднять.")
            else:
                item_name = user_input[1]
                take_item(game_state, item_name)
        case 'use':
            if len(user_input) < 2:
                print("Укажите предмет, который хотите использовать.")
            else:
                item_to_use = user_input[1]
                use_item(game_state, item_to_use)
        case "quit":
            print("Спасибо за игру! До свидания.")
            game_state["game_over"] = True
        case 'solve':
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case 'help':
            show_help()
        case "inventory":
            print(game_state["player_inventory"])
        case _:
            print(f"Неизвестная комманда: '{command}'. Введите 'help' для вывода списка команд.")


def main():
    game_state = {
        'player_inventory': [],  # Инвентарь игрока
        'current_room': 'entrance',  # Текущая комната
        'game_over': False,  # Значения окончания игры
        'steps_taken': 0  # Количество шагов
    }
    print("Добро пожаловать в Лабиринт сокровищ!")

    describe_current_room(game_state)

    while not game_state["game_over"]:
        player_input = get_input("\nЧто вы хотите сделать?\n> ")
        process_command(game_state, player_input)
