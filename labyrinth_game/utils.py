import math
from labyrinth_game.constants import ROOMS

def describe_current_room(game_state):
    current_room_name = game_state["current_room"]
    current_room = ROOMS[current_room_name]

    # Название комнаты в верхнем регистре (например, == ENTRANCE ==)
    print(f"\n== {current_room_name.upper()} ==")

    # Описание
    print(current_room["description"])

    # Предметы в комнате
    items = current_room["items"]
    if len(items) > 0:
        print("\nЗаметные предметы:")
        for item in items:
            print(f"  - {item}")

    # Выходы
    exits = current_room["exits"]
    print("\nВыходы:")
    for direction in exits.keys():
        print(f"  - {direction}")

    # Загадка
    puzzle = current_room["puzzle"]
    if puzzle is not None:
        print("\nКажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state):
    current_room_name = game_state["current_room"]
    current_room = ROOMS[current_room_name]
    puzzle = current_room["puzzle"][0]

    if puzzle is None:
        print("Загадок здесь нет.")
        return
    else:
        if current_room_name == "treasure_room": # Обработка специального случая, когда игрок может попытаться открыть сундук без ключей -- to refactor
            attempt_open_treasure(game_state)
            return

        solution = ROOMS[current_room_name]["puzzle"][1]

        print(puzzle)
        while True:
            user_guess = input("Ваш ответ: ")
            if user_guess != solution:
                print("Неверно. Попробуйте снова.")
            elif (user_guess == 'quit') or (user_guess == 'exit') or (user_guess == 'cancel'):
                break
            else:
                print("Успешно!")
                ROOMS[current_room_name]["puzzle"] = None
                break
        return

def attempt_open_treasure(game_state):
    current_room_name = game_state["current_room"]
    current_room = ROOMS[current_room_name]
    items_in_room = current_room["items"]
    inventory = game_state["player_inventory"]

    if "treasure_chest" not in items_in_room:
        print("Сундук уже открыт или отсутствует.")
        return

    has_treasure_key = "treasure_key" in inventory
    has_rusty_key = "rusty_key" in inventory

    if has_treasure_key or has_rusty_key:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        items_in_room.remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    try_code = input("Сундук заперт. ... Ввести код? (да/нет)\n> ")
    if try_code.lower() == "да":
        puzzle = current_room["puzzle"][0]
        solution = current_room["puzzle"][1]
        print(puzzle)
        player_code = input("Введите код: ")

        if player_code != solution:
            print("Неверный код. Замок остается закрытым.")
        else:
            print("Замок открывается с щелчком!")
            items_in_room.remove("treasure_chest")
            print("В сундуке сокровища! Вы победили!")
            game_state["game_over"] = True
    else:
        print("Вы отступаете от сундука.")

def pseudo_random(seed, modulo):
    x = math.sin(seed * 12.9898) * 43758.5453
    fraction = x - math.floor(x)
    return int(fraction * modulo)

def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state["player_inventory"]
    if inventory:
        item_id = pseudo_random(game_state["steps_taken"], len(inventory))
        lost_item = inventory.pop(item_id)
        print(f"Вы потеряли предмет: {lost_item}")
    else:
        hit = pseudo_random(game_state["steps_taken"], 10)
        if hit < 3:
            print("Ловушка смертельна! Вы проиграли.")
            game_state["game_over"] = True
        else:
            print("Вы лишь чудом выжили, отделавшись сильным испугом!")

def random_event(game_state):
    roll = pseudo_random(game_state["steps_taken"], 10)
    if roll != 0:
        return
    event_type = pseudo_random(game_state["steps_taken"], 3)
    current_room = ROOMS[game_state["current_room"]]
    inventory = game_state["player_inventory"]

    if event_type == 0:
        print("Вы находите на полу блестящую монетку!")
        current_room["items"].append("coin")
    elif event_type == 1:
        print("Рядом раздается подозрительный шорох...")
        if "sword" in inventory:
            print("Вы крепко сжимаете меч в руках и существо, затаившееся в тенях, скрывается.")
    else:
        if game_state["current_room"] == "trap_room" and "torch" not in inventory:
            print("Вы чувствуете, что сейчас произойдет что-то угрожающее вашей жизни.")
            trigger_trap(game_state)

def show_help() -> None:
    """Показать список доступных команд."""
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")