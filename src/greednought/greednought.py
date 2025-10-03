import time  # noqa: F401
import sys
import random

def handle_exit(exc_type, exc_value, exc_traceback):
    if exc_type is KeyboardInterrupt:
        print("You run screaming in fear so loudly that you don't even think to use the 'quit' command.")
        sys.exit(0)
    else:
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

def init_game():
    player = {
        "location": "spawn",
        "coins": 60,
        "inventory": [],
        "battle": "",
        "weapon": "fists",
        "armor": "clothes",
        "min_dmg": 3,
        "max_dmg": 10,
        "hp": 30,
        "max_hp": 30
    }
    rooms = {
        "spawn": {
            "flavor": "A hidden room at the back of a tavern.",
            "text": "You enter into the room at the back of the tavern and \n"
                    "notice a gaping hole at the back of it. What lies at the end \n"
                    "is unknown, but it's thought that it contains the legendary \n"
                    "treasure of the Schmamework 69.",
            "exits": {
                "north": "entrance",
                "south": "tavern",
            },
            "items": ["moldybaguette"],
            "enemies": []
        },
        "entrance": {
            "flavor": "A gaping, dusty, damp cave.",
            "text": "The cave begins to widen. You can tell something is definitely\n"
                    "down here, althought you have no clue where to even begin knowing\n"
                    "what it might be.",
            "exits": {
                "south": "spawn",
                "north": "entrance2"
            },
            "items": ["gruehair"],
            "enemies": ["grue"]
        },
        "tavern": {
            "flavor": "A bustling tavern full of drunken men.",
            "text": "You decide that the rumored treasure isn't worth the loss\n"
                    "of your sleep schedule and return to the tavern, drinking\n"
                    "with your buddies and trying to forget about the cave.",
            "exits": {},
            "items": [],
            "enemies": []
        },
    }
    items = {
        "moldybaguette": {
            "name": "Moldy Baguette",
            "flavor": "It's been here for two or three weeks.",
            "type": "junk",  # potion, armor, weapon, jewelry, junk
            "description": "A certain red-haired pear dropped this on her way to starting\n"
                           "on this quest a few weeks ago. There are drool stains and teeth marks.\n"
                           "Please don't eat this if you don't want to turn sillier than you are.",
        },
        "gruehair": {
            "name": "Grue Hair",
            "flavor": "It's simply a distinctive hair fallen off a grue.",
            "type": "junk",
            "description": "This is a good sign that a grue is nearby, but that's always the case,\n"
                           "so it means nothing at all. Be ready to fight a grue."
        },
        "gruepaw": {
            "name": "Grue's Paw",
            "flavor": "It's a grue's paw, with its claws permanently extended.",
            "type": "weapon",
            "max_dmg": 12,
            "min_dmg": 1,
            "description": "The grue doesn't part with its hand very easily. But I suppose a human\n"
                           "probably wouldn't part with its hand very easily either."
        },
        "grueshield": {
            "name": "Grue's Hide",
            "flavor": "It's the tough hide of a Grue.",
            "type": "armor",
            "hp": 40,
            "description": "The grue doesn't part with its hand very easily. But I suppose a human\n"
                           "probably wouldn't part with its hand very easily either."
        },
        "fists": {
            "name": "Fists",
            "flavor": "Your bare fists.",
            "type": "weapon",
            "max_dmg": 10,
            "min_dmg": 3,
            "description": "You have poor form, but your sheer strength seems to make up for it for the moment."
        },
        "clothes": {
            "name": "Plainclothes",
            "flavor": "Your average every day clothes.",
            "type": "armor",
            "hp": 30,
            "description": "The clothes of a jester. Just like you! What a coincidence"
        }
    }
    enemies = {
        "grue": {
            "name": "Grue",
            "hitpoints": 20,
            "attacktext": "The Grue swings its hairy fist, dealing ",
            "misstext": "The Grue swings and misses you by a single grue hair.",
            "damage": 5,
            "killtext": "You have been eaten by a Grue",
            "flavor": "It's just doing grue things.",
            "drops": ["gruehair", "gruepaw", "grueshield"]
        }
    }
    return player, rooms, items, enemies

def help():
    print("Welcome to Greednought! \n"
          "look: Take another look around \n"
          "get/take item: Pick an item up \n"
          "use item: Activate a consumable item \n"
          "drop item: Get rid of an item \n"
          "equip item: Put on armor or hold a weapon \n"
          "examine item: Look closer at an item \n"
          "inventory/inv: View your backpack \n"
          "go north/east/south/west/up/down: Move around \n"
          "attack creature: Swing at a creature \n"
          "run: Escape a battle \n"
          "win: Naturally... \n"
          "quit: Why would you ever want to do that?"
          )

def get_item(item, player, rooms, items, enemies):
    if item in rooms[player["location"]]["items"]:
        player["inventory"].append(item)
        rooms[player["location"]]["items"].remove(item)
        print(f"Picked up a {items[item]['name']}. {items[item]['flavor']}")
    else:
        print(f"You can't see any {item} here")
        return None

def use_item(item, player, rooms, items, enemies):
    if item not in items:
        print("That item does not exist.")
        return
    if items[item]["type"] == "potion":
        if item == "healthpotion":
            player["hp"] = min(player["hp"] + 10, player["max_hp"])
            print("You heal for 10 HP.")
            player["inventory"].remove(item)
        elif item == "poisonpotion":
            player["hp"] -= 10
            print("It tastes like acid and burns away 10 HP. Why would you drink this?")
            player["inventory"].remove(item)
    else:
        print("You can't use this item! Try 'equip'ping it?")

def drop_item(item, player, rooms, items, enemies):
    if item in player["inventory"]:
        if item == player["weapon"]:
            print(f"Unequipped your {item}\n")
            equip_item("fists", player, rooms, items, enemies)
        if item == player["armor"]:
            print(f"Unequipped your {item}\n")
            equip_item("clothes", player, rooms, items, enemies)
        rooms[player["location"]]["items"].append(item)
        player["inventory"].remove(item)
        print(f"You dropped the {items[item]['name']}.")
    else:
        print("You don't have that item.")

def equip_item(item, player, rooms, items, enemies):
    if item not in items:
        print("That item does not exist.")
        return
    if items[item]["type"] == "weapon":
        player["weapon"] = item
        player["min_dmg"] = items[item]["min_dmg"]
        player["max_dmg"] = items[item]["max_dmg"]
        print(f"Equipped your {items[item]['name']}.")
    elif items[item]["type"] == "armor":
        player["armor"] = item
        player["max_hp"] = items[item]["hp"]
        if player["hp"] > player["max_hp"]:
            player["hp"] = player["max_hp"]
        print(f"Equipped your {items[item]['name']}.")
    else:
        print("That's not armor or a weapon. Maybe you meant to 'use' this?")

def move_player(direction, player, rooms, items, enemies):
    location = player["location"]
    if direction not in rooms[location]["exits"]:
        print("You can't go that way.")
        return
    next_room = rooms[location]["exits"][direction]
    player["location"] = next_room
    print(f"You move {direction} into {rooms[next_room]['flavor'].lower()}")
    print(rooms[next_room]["text"])
    for i in rooms[next_room]["items"]:
        print(f"There is a {i} here. {items[i]['flavor']}")
    if rooms[next_room]["enemies"]:
        enemy = rooms[next_room]["enemies"][0]
        player["battle"] = enemy
        print(f"A {enemies[enemy]['name']} appears! {enemies[enemy]['flavor']}")

def attack(target_name, player, rooms, items, enemies):
    if player["battle"] == "":
        print("There is nothing to fight.")
        return
    enemy = player["battle"]
    if target_name != enemy:
        print(f"There is no {target_name} here.")
        return

    dmg = random.randint(player["min_dmg"], player["max_dmg"])
    enemies[enemy]["hitpoints"] -= dmg
    print(f"You strike the {enemies[enemy]['name']} for {dmg} damage.")

    if enemies[enemy]["hitpoints"] <= 0:
        print(f"You defeated the {enemies[enemy]['name']}!")
        for drop in enemies[enemy]["drops"]:
            rooms[player["location"]]["items"].append(drop)
        player["battle"] = ""
        return

    if random.random() < 0.75:
        print(f"{enemies[enemy]['attacktext']}{enemies[enemy]['damage']} damage!")
        player["hp"] -= enemies[enemy]["damage"]
        if player["hp"] <= 0:
            print(enemies[enemy]["killtext"])
            sys.exit(0)
    else:
        print(enemies[enemy]["misstext"])

def run(player, rooms, items, enemies):
    if player["battle"] == "":
        print("You aren't in combat.")
        return
    if random.random() < 0.5:
        print("You successfully escape!")
        player["battle"] = ""
    else:
        print("You failed to escape!")
        enemy = player["battle"]
        if random.random() < 0.75:
            print(f"{enemies[enemy]['attacktext']}{enemies[enemy]['damage']} damage!")
            player["hp"] -= enemies[enemy]["damage"]
            if player["hp"] <= 0:
                print(enemies[enemy]["killtext"])
                sys.exit(0)
        else:
            print(enemies[enemy]["misstext"])

def check_location(location, player, rooms, items, enemies):
    if location == "tavern":
        print("Game Over! Neutral ending...?")
        sys.exit(0)
    elif location == "gamble":
        print("A man would like to gamble with you. He proposes a 5 coin toss-up.")
        choice = input("[Y/N]? > ")
        if choice.lower() == "y":
            flip = random.randint(0, 1)
            if flip == 0:
                player["coins"] -= 5
                print(f"Bad luck! You lost 5 of your coins. You're down to {player['coins']}")
                print("Man (?): Come back if you ever want to try your luck again :3")
            else:
                player["coins"] += 5
                print(f"You win! You're up 5 coins, with your total now being {player['coins']}")
                print("(the man sighs): Maybe you'll come back another time and give me another chance")
    elif location == "temp":
        pass

def input_parser(cmd_in, player, rooms, items, enemies):
    command = cmd_in.lower()
    fail = [
        "What are you trying to do?", "You screwed SOMETHING up.", "You feel a disturbance in the Force.",
        "You feel a disturbance in the Schwartz.", "Do better", "Something's wrong, but you don't know what...",
        "How do you mess up this bad??", "Work on your typing skills!"
    ]
    random.shuffle(fail)

    if command == "help":
        help()

    elif command == "look":
        print(f"You are in {rooms[player['location']]['flavor']}")
        print(rooms[player["location"]]["text"])
        for i in rooms[player["location"]]["items"]:
            print(f"There is a {i} here. {items[i]['flavor']}")
        for i in rooms[player["location"]]["exits"]:
            index = rooms[player["location"]]["exits"][i]
            print(f"To your {i}: {rooms[index]['flavor']}")

    elif command.startswith("get") or command.startswith("take"):
        try:
            get = command.split(" ", 1)[1]
            get_item(get, player, rooms, items, enemies)
        except Exception:
            print(fail[1])

    elif command.startswith("use"):
        try:
            use = command.split(" ", 1)[1]
            use_item(use, player, rooms, items, enemies)
        except Exception:
            print(fail[1])

    elif command.startswith("drop"):
        try:
            drop = command.split(" ", 1)[1]
            drop_item(drop, player, rooms, items, enemies)
        except Exception:
            print(fail[1])

    elif command.startswith("equip"):
        try:
            equip = command.split(" ", 1)[1]
            equip_item(equip, player, rooms, items, enemies)
        except Exception:
            print(fail[1])

    elif command.startswith("examine"):
        try:
            item = command.split(" ", 1)[1]
            if item in player["inventory"]:
                print(f"It's a {items[item]['name']}.")
                print(items[item]["flavor"])
                print(items[item]["description"])
            else:
                print("You don't have that item.")
        except Exception:
            print(fail[1])

    elif command == "inventory" or command == "inv":
        print(f"Player | HP: {player['hp']}/{player['max_hp']} | Coins: {player['coins']}")
        print(f"Armor: {player['armor']} | Weapon: {player['weapon']} ({player['min_dmg']}-{player['max_dmg']} dmg)\n")
        print("Your backpack contains:")
        for i in player["inventory"]:
            print(f"{i}: {items[i]['flavor']}")

    elif command.startswith("go"):
        try:
            direction = command.split(" ", 1)[1]
            if player["battle"] == "":
                move_player(direction, player, rooms, items, enemies)
            else:
                print("You can't just leave, you're in a fight!\n")
        except Exception:
            print(fail[1])

    elif command.startswith("attack"):
        try:
            target = command.split(" ", 1)[1]
            attack(target, player, rooms, items, enemies)
        except Exception:
            print(fail[1])

    elif command == "run":
        run(player, rooms, items, enemies)

    elif command == "win":
        win = [
            "It won't be that easy...", "What about alcohol?", "Naturally.", "Yes, but not at this game",
            "Lose!", "Six seven or something idk i hate slang", "Peanut butter jelly time!",
            "badgers badgers badgers badgers MUSHROOM MUSHROOM", "Do the work first!", "nuh uh", "Pong!",
            "COOL FLAVOR TEXT", "FUNNY REPLY", "Traceback (most recent call last):"
        ]
        random.shuffle(win)
        print(win[0])

    elif command == "quit" or command == "exit":
        print("You give up. Don't worry... you'll be back...")
        sys.exit(0)

    elif command == "hi" or command == "hello":
        print("Good afternoon.")

    elif command == "i like men":
        print("Me too")

    else:
        print(f"I don't understand. {fail[1]}")

def game_loop(player, rooms, items, enemies):
    first_time = True
    while True:
        location = str(player["location"])
        if first_time:
            first_time = False
            print(f"You are in {rooms[location]['flavor'].lower()}")
            print(rooms[player["location"]]["text"])
            for i in rooms[player["location"]]["items"]:
                print(f"There is a {i} here. {items[i]['flavor']}")
            for i in rooms[player["location"]]["exits"]:
                index = rooms[player["location"]]["exits"][i]
                print(f"To your {i}: {rooms[index]['flavor']}")

        command = input("\n...> ")
        input_parser(command, player, rooms, items, enemies)
        if player["location"] != location:
            first_time = True
            location = str(player["location"])
            check_location(location, player, rooms, items, enemies)

def main():
    sys.excepthook = handle_exit
    player, rooms, items, enemies = init_game()
    print("Welcome to Greednought!")
    print("Type help if you need assistance.\n")
    game_loop(player, rooms, items, enemies)

if __name__ == "__main__":
    main()