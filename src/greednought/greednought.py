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
        "weapon": "",
        "armor": "",
    }
    rooms = {
        "spawn": {
            "flavor": "A hidden room at the back of a tavern.",
            "text": "You enter into the room at the back of the tavern and \n"
            "notice a gaping hole at the back of it. What lies at the end \n"
            "is unknown, but it's thought that it contains the legendary \n"
            "treasure of the Schmamework 69. \n",
            "exits": {
                "north": "entrance",
                "south": "tavern",
            },
            "items": ["moldybaguette"],
            "enemies": []
        },
        "entrance": {
            "flavor": "A gaping, dusty, damp cave.",
            "text": """add text
            right here""",
            "exits": {
                "south": "spawn",
                "north": "entrance2"
            },
            "items": ["gruehair"],
            "enemies": []
        },
        "tavern": {
            "flavor": "A bustling tavern full of drunken men.",
            "text": "You decide that the rumored treasure isn't worth the loss\n"
            "of your sleep schedule and return to the tavern, drinking\n"
            "with your buddies and trying to forget about the cave.\n",
            "exits": {},
            "items": [],
            "enemies": []
        },
    }
    items = {
        "moldybaguette": {
            "name": "Moldy Baguette",
            "flavor": "It's been here for two or three weeks.",
            "type": "junk", # potion, armor, weapon, jewlery, junk
            "description": "A certain red-haired pear dropped this on her way to starting\n"
            "on this quest a few weeks ago. There are drool stains and teeth marks.\n"
            "Please don't eat this if you don't want to turn sillier than you are.\n",
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
          "quit: Why would you ever want to do that? \n"
        )

def get_item(item, player, rooms, items, enemies):
    if (item in rooms[player["location"]]["items"]):
        player["inventory"].append(item)
        print(f"Picked up a {items[item]["name"]}. {items[item]["flavor"]}")
    else:
        print(f"You can't see any {item} here")
        return None

def use_item(item, player, rooms, items, enemies):
    if items[item]["type"] == "potion":
        if item == "healthpotion":
            pass
        elif item == "poisonpotion":
            pass
    else:
        print("You can't use this item! Try 'equip'ping it?")

def drop_item(item, player, rooms, items, enemies):
    rooms[player["location"]]["items"].append(item)
    player["inventory"].remove(item)

def equip_item(item, player, rooms, items, enemies):
    if items[item]["type"] == "weapon":
        if item == "gruepaw":
            player["weapon"] = "gruepaw"
            print(f"Equipped your {items[item]["name"]}.")
        elif item == "item":
            pass
    elif items[item]["type"] == "armor":
        if item == "grueshield":
            player["weapon"] = "grueshield"
            print(f"Equipped your {items[item]["name"]}.")
        elif item == "item":
            pass
    else:
        print("That's not armor or a weapon. Maybe you meant to 'use' this?")
    
def move_player(direction, player, rooms, items, enemies):
    pass

def attack(enemy, player, rooms, items, enemies):
    pass

def run():
    pass

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
                print(f"Bad luck! You lost 5 of your coins. You're down to {player["coins"]}")
                print("Man (?): Come back if you ever want to try your luck again :3")
            else:
                player["coins"] += 5
                print(f"You win! You're up 5 coins, with your total now being {player["coins"]}")
                print("(the man sighs): Maybe you'll come back another time and give me another chance")
        else:
            pass
    elif location == "aaa":
        pass

def input_parser(cmd_in, player, rooms, items, enemies):
    command = cmd_in.lower()
    fail = ["What are you trying to do?", "You screwed SOMETHING up.", "You feel a disturbance in the Force.", "You feel a disturbance in the Schwartz.", "Do better", "Something's wrong, but you don't know what...", "How do you mess up this bad??", "Work on your typing skills!"]
    random.shuffle(fail)
    if command == "help":
        help()
        
    elif command == "look":
        print(f"You are in {rooms[player["location"]]["flavor"]}")
        print(rooms[player["location"]]["text"])
        for i in rooms[player["location"]]["items"]:
            print(f"There is a {i} here. {items[i]["flavor"]}")
        
    elif command.startswith("get") or command.startswith("take"):
        get = command.split(" ", 1)[1]
        try:
            get_item(get, player, rooms, items, enemies)
        except Exception:
            print(fail[1])
    
    elif command.startswith("use"):
        use = command.split(" ", 1)[1]
        try:
            use_item(use, player, rooms, items, enemies)
        except Exception:
            print(fail[1])
    
    elif command.startswith("drop"):
        drop = command.split(" ", 1)[1]
        try:
            drop_item(drop, player, rooms, items, enemies)
        except Exception:
            print(fail[1])
            
    elif command.startswith("equip"):
        equip = command.split(" ", 1)[1]
        try:
            equip_item(equip, player, rooms, items, enemies)
        except Exception:
            print(fail[1])
    
    elif command.startswith("examine"):
        item = command.split(" ", 1)[1]
        if item in player["inventory"]:
            print(f"It's a {items[item]["name"]}.")
            print(items[item]["flavor"])
            print(items[item]["description"])
        else:
            print("You don't have that item.")
        
    elif command == "inventory" or command == "inv":
        print("Your backpack contains:")
        for i in player["inventory"]:
            print(f"{i}: {items[i]["flavor"]}")
        
    elif command.startswith("go"):
        direction = command.split(" ", 1)[1]
        if player["battle"] != "":
            move_player(direction, player, rooms, items, enemies)
        else:
            print("You can't just leave, you're in a fight!")
        
    elif command.startswith("attack"):
        attack = command.split(" ", 1)[1]
        try:
            attack(attack, player, rooms, items, enemies)
        except Exception:
            print(fail[1])
            
    elif command == "run":
        run(player, rooms, items, enemies)

    elif command == "win":
        win = ["It won't be that easy...", "What about alcohol?", "Naturally.", "Yes, but not at this game", "Lose!", "Six seven or something idk i hate slang", "Peanut butter jelly time!", "badgers badgers badgers badgers MUSHROOM MUSHROOM", "Do the work first!", "nuh uh", "Pong!", "COOL FLAVOR TEXT", "FUNNY REPLY", "Traceback (most recent call last):"]
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
        print("I don't understand.")
    

def game_loop(player, rooms, items, enemies):
    first_time = True
    while(1):
        location = player["location"]
        if first_time:
            first_time = False
            print(f"You are in {rooms[location]["flavor"].lower()}")
            print(rooms[player["location"]]["text"])
            for i in rooms[player["location"]]["items"]:
                print(f"There is a {i} here. {items[i]["flavor"]}")

        command = input("\n...> ")
        if player["location"] != location:
            first_time = True
            location = player["location"]
            check_location(location, player, rooms, items, enemies)
            
        input_parser(command, player, rooms, items, enemies)

def main():
    sys.excepthook = handle_exit
    player, rooms, items, enemies = init_game()
    print("Welcome to Greednought!")
    print("Type help if you need assistance.\n")
    game_loop(player, rooms, items, enemies)

main()