import math

from labyrinth_game.constants import (
    COMMANDS,
    CREATURE_DEATH_LIMIT,
    CREATURE_HIT_CHANCE,
    EVENT_PROBABILITY,
    RANDOM_EVENT_TYPES,
    ROOMS,
    TRAP_DEATH_LIMIT,
    TRAP_HIT_CHANCE,
)


def describe_current_room(game_state):
    """
    Показывает полное описание текущей комнаты игрока.
    """
    current_room_name = game_state["current_room"]
    current_room = ROOMS[current_room_name]

    # Название комнаты в верхнем регистре
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
    """
    Решение загадки в текущей комнате игрока.
    Награда зависит от типа комнаты.
    """
    current_room_name = game_state["current_room"]
    current_room = ROOMS[current_room_name]
    puzzle = current_room["puzzle"]

    # Возможность принимать альтернативные варианты ответов
    alt_answers = {
        "10": ["10", "десять"],
        "3": ["3", "три"],
        "4": ["4", "четыре"],
        "8": ["8", "восемь"],
        "2": ["2", "два"]
    }

    if puzzle is None:
        print("Загадок здесь нет.")
        return

    question, answer = puzzle
    answer = answer.strip().lower()
    print(f"\n{question}: ")

    player_answer = input("Ваш ответ: ").strip().lower()

    if player_answer == answer or player_answer in alt_answers.get(answer, []):
        print("\nПравильно! Загадка решена.")
        current_room["puzzle"] = None
        if (current_room_name == "hall" and
                "treasure_key" not in game_state["player_inventory"]):
            reward = "treasure_key"
        elif (current_room_name == "library" and
              "rusty_key" not in game_state["player_inventory"]):
            reward = "rusty_key"
        else:
            reward = current_room["items"].pop(0)

        print(f"Вы получили {reward}!")
        game_state["player_inventory"].append(reward)
    else:
        print("Неверно. Попробуйте снова.")
        if current_room_name == "trap_room":
            trigger_trap(game_state)

def attempt_open_treasure(game_state):
    """
    Открыть treasure_chest в комнате с помощью ключа или решить загадку.
    """
    current_room_name = game_state["current_room"]
    current_room = ROOMS[current_room_name]
    items_in_room = current_room["items"]
    inventory = game_state["player_inventory"]

    if "treasure_chest" not in items_in_room:
        print("Сундук уже открыт или отсутствует в данной комнате.")
        return

    has_treasure_key = "treasure_key" in inventory

    if has_treasure_key:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        items_in_room.remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    try_code = input("Сундук заперт. ... Ввести код? (да\нет)\n> ").strip().lower()

    if try_code == "да" or try_code == 'yes':
        puzzle = current_room["puzzle"]
        print(puzzle[0])
        player_code = input("Введите код: ").strip().lower()

        if puzzle is not None:
            solution = puzzle[1]

            if player_code == solution or player_code in ["десять", "10"]:
                print("\nЗамок открывается с щелчком!")
                items_in_room.remove("treasure_chest")
                print("\nВ сундуке сокровища! Вы победили!")
                game_state["game_over"] = True
            else:
                print("Неверный код. Замок остается закрытым.")
    else:
        print("Вы отступаете от сундука.")

def pseudo_random(seed, modulo):
    """
    Генератор псевдослучайных чисел для рандомных событий в игре.
    """
    x = math.sin(seed * 12.9898) * 43758.5453
    fraction = x - math.floor(x)
    return int(fraction * modulo)

def trigger_trap(game_state):
    """
    Активировать ловушку в trap_room при неверном ответе на загадку.
    Либо убирает случайный предмет из инвентаря, либо убивает
    игрока с заданной вероятностью.
    """
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state["player_inventory"]
    if inventory:
        item_id = pseudo_random(game_state["steps_taken"], len(inventory))
        lost_item = inventory.pop(item_id)
        print(f"Вы потеряли предмет: {lost_item}")
    else:
        hit = pseudo_random(game_state["steps_taken"], TRAP_HIT_CHANCE)
        if hit < TRAP_DEATH_LIMIT:
            print("Ловушка смертельна! Вы проиграли.")
            game_state["game_over"] = True
        else:
            print("Вы лишь чудом выжили, отделавшись сильным испугом!")

def random_event(game_state):
    """
    Генерация рандомного события и обработка исходов через pseudo_random.
    """
    roll = pseudo_random(game_state["steps_taken"], EVENT_PROBABILITY)
    if roll != 0:
        return
    event_type = pseudo_random(game_state["steps_taken"] + 666, RANDOM_EVENT_TYPES)
    current_room = ROOMS[game_state["current_room"]]
    inventory = game_state["player_inventory"]

    if event_type == 0:
        print("\nВы находите на полу блестящую монетку!")
        current_room["items"].append("coin")
    elif event_type == 1:
        print("\nРядом раздается подозрительный шорох...")
        if "sword" in inventory:
            print("Вы крепко сжимаете меч в руках ",
                  "и существо, затаившееся в тенях, скрывается.")
        else:
            hit = pseudo_random(game_state["steps_taken"], CREATURE_HIT_CHANCE)
            if hit < CREATURE_DEATH_LIMIT:
                print("Существо нанесло смертельный удар из темноты! Вы проиграли.")
                game_state["game_over"] = True
            else:
                print("Существо решило отступить, но вы все равно страшно напуганы!")
    else:
        if game_state["current_room"] == "trap_room" and "torch" not in inventory:
            print("\nВы чувствуете, что сейчас произойдет ",
                  "что-то угрожающее вашей жизни.")
            trigger_trap(game_state)

def show_help() -> None:
    """
    Показать список доступных команд.
    """
    print("\nДоступные команды:\n")
    for cmd, desc in COMMANDS.items():
        print(f"{cmd:<16} {desc}")