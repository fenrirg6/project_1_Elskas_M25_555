def show_inventory(game_state):
    inventory = game_state['inventory']

    if len(inventory) == 0:
        print("\nВаш инвентарь пуст.")
    else:
        print("\nВаш инвентарь:")
        for item in inventory:
            print(f"  - {item}")

def get_input(prompt=">"):
    try:
        pass
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"