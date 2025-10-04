from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, attempt_open_treasure, random_event

def show_inventory(game_state):
    inventory = game_state["inventory"]

    if len(inventory) == 0:
        print("\nВаш инвентарь пуст.")
    else:
        print("\nВаш инвентарь:")
        for item in inventory:
            print(f"  - {item}")

def get_input(prompt = ">"):
    try:
        user_input = input(prompt)
        return user_input.strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state, direction):
    """
    Функция перемещения по комнатам.
    """
    current_room_name = game_state["current_room"]
    current_room = ROOMS[current_room_name]
    exits = current_room["exits"]

    if direction in exits:
        new_room = exits[direction]
        if new_room == "treasure_room":
            if "treasure_key" in game_state["player_inventory"] or "rusty_key" in game_state["player_inventory"]:
                print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
                game_state["current_room"] = new_room
                game_state["steps_taken"] += 1
                describe_current_room(game_state)
                random_event(game_state)
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
        else:
            print(f"\nВы идете на {direction}...")
            game_state["current_room"] = new_room
            game_state["steps_taken"] += 1
            random_event(game_state)
            describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    current_room_name = game_state["current_room"]
    current_room = ROOMS[current_room_name]
    items_in_room = current_room["items"]

    if item_name in items_in_room:
        if item_name == "treasure_chest":
            print("Вы не можете поднять сундук, он слишком тяжелый.")
            return
        # items_in_room.remove(item_name)
        game_state["player_inventory"].append(item_name)
        current_room["items"].remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    inventory = game_state["player_inventory"]

    if item_name in inventory:
        match item_name:
            case "sword":
                print("Вы чувствуете себя намного уверенее...")
            case "torch":
                print("Стало немножко светлее...")
            case "bronze_box":
                print("Вы открываете бронзовую шкатулку...")
                if "rusty_key" not in inventory:
                    print("Внутри нее оказался ржавый ключ!")
                    inventory.append("rusty_key")
                else:
                    print("Внутри шкатулки ничего не оказалось...")
            case "rusty_key":
                attempt_open_treasure(game_state)
            case _:
                print(f"Вы не знаете, как использовать {item_name}.")
    else:
        print("У вас нет такого предмета.")