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