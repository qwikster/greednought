import time
import sys

def exit_handler(exc_name, exc_type, exc_traceback):
    if exc_type is KeyboardInterrupt:
        sys.exit(0)

def init_game():
    player = {}
    rooms = {}
    return player, rooms

def main():
    player, rooms = init_game()
    time.sleep(10)