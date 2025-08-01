import sys
import os
import random
import json
import logging

screen_width = 100

logging.basicConfig(filename='Combat_errors.log', level=logging.ERROR)

## Character Setup ###
class Character:
    def __init__(self):
        self.name = ''
        self.life = 100
        self.attack = 15
        self.location = 'start_zone'

    def to_dict(self):
        return {
            "name": self.name,
            "life": self.life,
            "attack": self.attack,
            "location": self.location
        }
    def from_dict(self, data):
        self.name = data.get("name", "")
        self.life = data.get("life", 100)
        self.attack = data.get("attack", 15)
        self.location = data.get("location", "start_zone")

class Enemy(Character):
    def __init__(self, name, life, description, attack):
        super().__init__()
        self.name = name
        self.life = life
        self.description = description
        self.attack = attack
goblin = Enemy("Goblin", 30, "A meek but feral goblin!", 4)
skeleton = Enemy("Skeleton", 25, "Animated bones with rusted weapons.", 8)
fishman = Enemy("Fishman", 40, "An ancient corrupted human with fish like features and serraded claws.", 10)
corrupt_guardsman = Enemy("Corrupt Guardsman", 35, "They're eyes are filled with dark energy, being controlled by another entity.", 8)
impostor_king = Enemy("Impostor King", 80, "A doppelganger of the true king stands before you, Death to the false king!", 15)
ancient_demon = Enemy("Ancient Demon", 100, "An ancient evil with unholy powers.", 20)

class Inventory:
    def __init__(self):
        self.items = []
    
    def add(self, item):
        self.items.append(item)

    def remove(self, item):
        self.items.remove(item)
        

class Item:
    def __init__(self, name, description, effect=None):
        self.name = name
        self.description = description
        self.effect = effect 

MyCharacter = Character()
MyCharacter.inventory = Inventory()
        
def game_state_to_dict():
    return {
        "character": MyCharacter.to_dict(),
        "inventory": [vars(item) for item in MyCharacter.inventory.items],
        "solved_places": solved_places,
    }

def load_game_state(data):
    MyCharacter.from_dict(data.get("character", {}))
    MyCharacter.inventory.items = [Item(**item) for item in data.get("inventory", [])]
    for k, v in data.get("solved_places", {}).items():
        solved_places[k] = v

def save_game(filename="savegame.json"):
    try:
        with open(filename, "w") as f:
            json.dump(game_state_to_dict(), f)
            print("Game saved.")
    except Exception as e:
        print(f"Error saving character: {e}")
    
def load_game(filename="savegame.json"):
    try:
        with open(filename, "r") as f:
                data = json.load(f)
                load_game_state(data)
                print("Game loaded.")
    except FileNotFoundError:
            print("No saved game found.")
    except Exception as e:
        print(f"Error loading game: {e}")

### Menu Screen ###
def menu_screen_selections():
    while True:
        selection = input("> ")
        if selection.lower() == ("start"):
            start_game() #PH
        elif selection.lower() == ("help"):
            help_menu()
        elif selection.lower() in ("load", "load_game"):
            load_game()
            print("Game Loaded.")
            start_game(new_game=False)
        elif selection.lower() == ("quit"):
            sys.exit()
        else:
            print("Please enter a valid command ('start', 'help', 'quit', 'load'.).")

def menu_screen():
    os.system('clear')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~ Welcome to Perilous Python RPG! ~')
    print('            - Start -               ')
    print('            - Help -               ')
    print('            - Load -               ')
    print('            - Quit -               ')
    print('    Copyright 2025 CW Software     ')
    menu_screen_selections()

def help_menu():
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~ Welcome to Perilous Python RPG! ~')
    print('- use up, down, left, right to move')
    print('- Type your commands to execute moves in the game')
    print('- Use "look" to inspect elements in the world')
    print('- to save progress type save')
    print('- GG & Have Fun!')
    menu_screen_selections()
### Functionality ###
def move_player(direction):
    try:
        row = MyCharacter.location[0]
        col = int(MyCharacter.location[1])
        new_location = None

        if direction in UP and row > 'a':
            new_row = chr(ord(row) - 1)
            new_location = f"{new_row}{col}"
        elif direction in DOWN and row < 'd':
            new_row = chr(ord(row) + 1)
            new_location = f"{new_row}{col}"
        elif direction in LEFT and col > 1:
            new_location = f"{row}{col - 1}"
        elif direction in RIGHT and col < 4:
            new_location = f"{row}{col + 1}"
        else:
            print("You can't go that way.")
            return
    
        if new_location in solved_places:
            MyCharacter.location = new_location
            print(f"You moved to {new_location}")
            print(zonemap[new_location]['description'])
            #combat trigger
            enemy = zonemap[MyCharacter.location].get('enemy')
            if enemy and enemy.life > 0:
                print(f"You encounter a {enemy.name}!")
                combat(MyCharacter, enemy)
        else:
            print("That location doesn't exist")
    except Exception as e:
        print(f"Error moving player: {e}")


def print_location():
    try:
        print('# ' + MyCharacter.location.upper() + ' #')
        print('# ' + zonemap[MyCharacter.location] [DESCRIPTION] + ' #')
    except KeyError:
        print("Error: Current location is invalid")

def trigger_event(event_name):
    print(f"Encounter Triggered: {event_name}")
    print("Attempting to resolve conflict")
    roll = random.randint(1, 20)
    print(f"You rolled a {roll}!")
    if roll < 10:
        MyCharacter.life -= 10
        print("You failed the roll! you take 10 points of damage.")
        print(f"Current Health: {MyCharacter.life}.")
    else:
        print("Success!")
    
def combat(player, enemy):
    while True:
        print(f"\nAmbush from {enemy.name}: {enemy.description}!!")
        # Store OG health to reset encounter if needed.
        original_player_life = player.life
        original_enemy_life = enemy.life

        while player.life > 0 and enemy.life > 0:
            try:
                input("\nPress Enter to roll for attack damage..")
                player_roll = random.randint(1, 20)
                if player_roll == 20:
                    player_damage = player.attack * 2 #Crit 
                    print(f"Critical Hit! You rolled a 20 and deal {player_damage} damage!")
                elif player_roll >= 10:
                    player_damage = random.randint(5, player.attack)
                    print(f"You hit! Rolled {player_roll} and deal {player_damage}.")
                else:
                    player_damage = 0
                    print(f"You missed! Rolled {player_roll}.")
                enemy.life -= player_damage
                if enemy.life <= 0:
                    print(f"You Killed {enemy.name}")
                    break

                input("Press enter to roll for defence..")
                enemy_roll = random.randint(1, 20)
                if enemy_roll == 20:
                    enemy_damage = enemy.attack * 2
                    print(f"Critical! {enemy.name} rolled a 20 and deals {enemy_damage} damage!")
                elif enemy_roll >= 10:
                    enemy_damage = random.randint(1, enemy.attack)
                    print(f"{enemy.name} hits! Rolled {enemy_roll} and deals {enemy_damage} damage.")
                else:
                    enemy_damage = 0
                    print(f"{enemy.name} missed! Rolled {enemy_roll}.")
                player.life -= enemy_damage
                print(f"Your health: {player.life} | {enemy.name}'s health: {enemy.life}")
    
            except ValueError as ve:
                print("Input error during combat. Please try again.")
                logging.error(f"ValueError in combat: {ve}")
            except AttributeError as ae:
                print("A Character attribute was missing during combat.")
                logging.error(f"AttributeError in combat: {ae}")
            except Exception as e:
                print("Unexpected error occurred during combat. Please contact dev.")
                logging.error(f"Unexpected error in combat: {e}")

        if player.life <= 0:
            print(f"You have been slain by {enemy.name}")
            while True:
                retry = input("Do you want to retry the encounter? (yes/no): ").lower().strip()
                if retry == "yes" or retry == "":
                    player.life = original_player_life
                    enemy.life = original_enemy_life
                    break
                elif retry == "no":
                    print("returning to menu...")
                    return
                else: 
                    print("Please enter 'yes' or 'no'.")
        elif enemy.life <= 0:
            print(f"You have slain the {enemy.name}!!")
            solved_places[player.location] = True
            zonemap[player.location]['solved'] = True
            # Win Cond Check
            if enemy.name == "Ancient Demon":
                print("\nCongratulations!!! You have slain the Ancient Demon and Succeeded!!")
                sys.exit()
            break
def generic_event(description, roll_threshold, fail_effect=None, fail_msg="", success_effect=None, success_msg=""):
    print(description)
    roll = random.randint(1,20)
    print(f"You roll a {roll}")
    if roll < roll_threshold:
        if fail_effect:
            fail_effect()
        print(fail_msg)
    else:
        if success_effect:
            success_effect()
        print(success_msg)


def event_city_guard():
    def fail(): MyCharacter.life -= 10
    solved_places[MyCharacter.location] = True
    zonemap[MyCharacter.location]['solved'] = True
    def success():
        health_potion = Item("Health Potion", "Heals for 20hp", effect={"heal": 20})
        MyCharacter.inventory.add(health_potion)
        solved_places[MyCharacter.location] = True
        zonemap[MyCharacter.location]['solved'] = True
    generic_event("The Guards try to arrest you. You must roll to escape!",
        10,
        fail_effect=fail,
        fail_msg="You fail to escape and take 10 damage.",
        success_effect=success,
        success_msg="You escape and steal a potion!")

def event_grizzly():
    def fail(): MyCharacter.life -= 15
    solved_places[MyCharacter.location] = True
    zonemap[MyCharacter.location]['solved'] = True
    def success():
         healing_potion = Item("Healing Potion", "Heals for 20hp", effect={"heal": 20})
         MyCharacter.inventory.add(healing_potion)
         solved_places[MyCharacter.location] = True
         zonemap[MyCharacter.location]['solved'] = True
    generic_event("You are charged at by a grizzly, roll to dodge!",
                  10,
                  fail_effect=fail,
                  fail_msg="You were mauled and lose 15 health, You manage to escape without further damage.",
                  success_effect=success,
                  success_msg="You dodge the grizzly and find some berries (Created +1 Healing potion)!")

def event_field():
    def fail(): solved_places[MyCharacter.location] = True
    zonemap[MyCharacter.location]['solved'] = True
    def success():
        magicians_brick = Item("Magicians Brick", "Appears to be useless", effect={'attack': 0})
        MyCharacter.inventory.add(magicians_brick)
        solved_places[MyCharacter.location] = True
        zonemap[MyCharacter.location]['solved'] = True
    generic_event("You approach a strange object embedded in the grass, roll to attempt to pick it up.",
                  15,
                  fail_effect=fail,
                  fail_msg="You aren't strong enough to lift the strange object, it feels as though it doesnt wish to be moved.",
                  success_effect=success,
                  success_msg="You lift the strange object, upon further inspection it appears to be a brick, carved into it is 'Magicians Brick' You have no idea what this does.")

def event_skeleton_axe():
    def fail(): MyCharacter.life -= 10
    solved_places[MyCharacter.location] = True
    zonemap[MyCharacter.location]['solved'] = True
    def success():
        ancient_axe = Item("Ancient Axe", "Adds 10 points of damage", effect={'attack': 10})
        MyCharacter.inventory.add(ancient_axe)
        solved_places[MyCharacter.location] = True
        zonemap[MyCharacter.location]['solved'] = True
    generic_event("You attempt to take the rare and well crafted axe from the corpse, roll to take it.",
                  12,
                  fail_effect=fail,
                  fail_msg="You are unable to take the axe, The Skeleton falls on top of you, you take damage and the axe breaks! you lose 10hp!",
                  success_effect=success,
                  success_msg="You take the Axe! you feel stronger holding the ancient axe, Adds 10 points of attack damage")
        
def event_cursed_book():
    def fail(): MyCharacter.life -= 10
    solved_places[MyCharacter.location] = True
    zonemap[MyCharacter.location]['solved'] = True
    def success():
        cleansed_book = Item("Powerful Manuscript", "Heals for 25 Health points", effect={'heal': 25})
        MyCharacter.inventory.add(cleansed_book)
        solved_places[MyCharacter.location] = True
        zonemap[MyCharacter.location]['solved'] = True
    generic_event("You hold the book in your hands the energy surges through you, roll to try and control it",
                  10,
                  fail_effect=fail,
                  fail_msg="You are unable to control it, it burns dark symbols into your hands taking 15 points of damage!! The book disintegrates in your hands",
                  success_effect=success,
                  success_msg="You manage to hold on and feel the energy flow, You gain 25 Health")
        
def event_peaceful_creatures():
    def fail(): 
        solved_places[MyCharacter.location] = True
        zonemap[MyCharacter.location]['solved'] = True
    def success():
        greater_healing_potion = Item("Greater Health Potion", "Restores 50 Health", effect={'heal': 50})
        MyCharacter.inventory.add(greater_healing_potion)
        solved_places[MyCharacter.location] = True
        zonemap[MyCharacter.location]['solved'] = True
    generic_event("You attempt to communicate with the creatures, roll to attempt conversation",
                  7,
                  fail_effect=fail,
                  fail_msg="You attempt communication however they do not understand and go about there day.",
                  success_effect=success,
                  success_msg="They guide you to the corpse of a slain adventurer, they are holding a greater HP potion")

def event_old_god():
    def fail(): MyCharacter.life -= 15
    solved_places[MyCharacter.location] = True
    zonemap[MyCharacter.location]['solved'] = True
    def success():
         health_potion = Item("Health Potion", "Heals for 20 Health", effect={'heal': 20})
         MyCharacter.inventory.add(health_potion)
         solved_places[MyCharacter.location] = True
         zonemap[MyCharacter.location]['solved'] = True
    generic_event("You are drawn to potions in the offerings, roll to attempt to take one.",
                  15,
                  fail_effect=fail,
                  fail_msg="You attempt to grab the potion, however the statue begins to glow and whisper an unknown language, the whisper causes phsychological pain take 15 points of damage.",
                  success_effect=success,
                  success_msg="The statue does not react to your presence, your able to take a health potion!")

def event_dark_presence():
    def fail():
        MyCharacter.life -= 12
        solved_places[MyCharacter.location] = True
        zonemap[MyCharacter.location]['solved'] = True
    def success(): 
        solved_places[MyCharacter.location] = True
        zonemap[MyCharacter.location]['solved'] = True
        pass
    generic_event("The voice beckons you to move deeper into the structure, roll for mental fortitude",
                  12,
                  fail_effect=fail,
                  fail_msg="You feel ethereal tendrils snare your mind, The ancients do not want you hear. Take 12 points of damage.",
                  success_effect=success,
                  success_msg="You are able to withstand the mental onslaught, you overcome and are able to press forward!")

def event_mythos_lake():
    def fail(): 
        MyCharacter.life -= 15
        solved_places[MyCharacter.location] = True
        zonemap[MyCharacter.location]['solved'] = True
    def success():
        solved_places[MyCharacter.location] = True
        zonemap[MyCharacter.location]['solved'] = True 
        pass
    generic_event("The water seems to react to your presence, it beckons you to enter, roll for result",
              12,
              fail_effect=fail,
              fail_msg="As you move closer to the water, a figure obscured by the dark waters grabs your leg, trying to pull you in, Take 15 points of damage!",
              success_effect=success,
              success_msg="You are able to fight off the presence underwater, You now have a clear path forward, the lake appears to be a gateway to another plane.")
 
def event_old_one():
    def fail(): MyCharacter.life -= 30
    solved_places[MyCharacter.location] = True
    zonemap[MyCharacter.location]['solved'] = True
    def success(): pass
    solved_places[MyCharacter.location] = True
    zonemap[MyCharacter.location]['solved'] = True
    generic_event("You stare into the face of madness, you are unable to move or look away, roll for mental fortitude",
                  15,
                  fail_effect=fail,
                  fail_msg="You succumb to madness, your eyes bleed in the presence of the ancient gods, You take 30 points of damage",
                  success_effect=success,
                  success_msg="You are able to fight off the presence, it tries to ensnare you again you are able to escape.")
        

def prompt():
    print("How would you like to proceed?")
    action = input("> ").lower().strip()
    if action in UP + DOWN + LEFT + RIGHT:
        move_player(action)
    elif action in ['save_game', 'save']:
        save_game()
        print("Game Saved")
    elif action in ['use item', 'use_item']: use_item()
    elif action in ['look', 'examine', 'inspect']:
        print_location()
        if not zonemap[MyCharacter.location].get('solved', False):
            event = zonemap[MyCharacter.location].get('event')
            if event:
                print(f"Event: {event}")
    elif action in ['move', 'go', 'travel', 'walk']:
        print("Which direction? (up, down, left, right)")
        direction = input("> ").lower().strip()
        if direction in UP + DOWN + LEFT + RIGHT:
                move_player(direction)
        else:
            print("Invalid direction.")
    elif action == 'interact':
        if zonemap[MyCharacter.location].get('solved', False):
            print("There's nothing left to do here")
            return
        event = zonemap[MyCharacter.location].get('event')
        event_result = zonemap[MyCharacter.location].get('event_result')
        if event:
            print(f"You interact: {event}")
            if event_result:
                try:
                    event_result()
                    return
                except Exception as e:
                    print(f"Error running event: {e}")
        else:
            print("There's nothing to interact with here.")
    elif action == 'quit':
        print("Returning to menu..")
        return 'quit'
    else: 
        print("Unknown action. Try: look, move, interact, use item, or quit.")
        

def use_item():
    if not MyCharacter.inventory.items:
        print("Your inventory is empty!")
        return
    print("Inventory: ")
    for idx, item in enumerate(MyCharacter.inventory.items):
        print(f"{idx+1}. {item.name} - {item.description}")
    choice = input("Choose an item number to use: ")
    try:
        idx = int(choice) - 1
        item = MyCharacter.inventory.items[idx]
        used = False
        if item.effect:
            for key, value in item.effect.items():
                if hasattr(MyCharacter, key):
                    setattr(MyCharacter, key, getattr(MyCharacter, key) + value)
                    print(f"You used {item.name} and your {key} changed by {value}. Now: {getattr(MyCharacter, key)}")
                    used = True
        if used:
            MyCharacter.inventory.remove(item)
        else:
            print("You can't use that right now.")
    except (ValueError, IndexError):
        print("Invalid choice.")
    except Exception as e:
        print(f"Unexpected error using item {e}")    

def start_game(new_game =True):
    if new_game:
        MyCharacter.location = "a1" #starting location
    print("\nWelcome to Perilous Python RPG!")
    print("\nYou have awoken in front of a dark structure infested with monsters & demons")
    print("\nYour goal is to delve deep into the structure and defeat the Ancient Demon to win")
    print("\nThere is plenty to explore beforehand and gain helpful items to help you in your quest")
    print('\nAll events are solved with dice rolls so each playthrough could change!')
    print("Type 'up', 'down', 'left', or 'right' to move.")
    print("Type 'look' to inspect your surroundings.")
    print("Type 'interact' to interact with events.")
    print("Type 'use item' to use an item from your inventory.")
    print("Type 'save' to save your progress, or 'quit' to exit to the menu.\n")
    print("Game commenced! What will you do?")
    while True:
        result = prompt()
        if result == 'quit':
            break

DESCRIPTION = 'description'
SOLVED = False
UP = 'up', 'north'
DOWN = 'down', 'south'
LEFT = 'left', 'west'
RIGHT = 'right', 'east'



zonemap = { 
    'a1': {
        'description': "You are standing before an aging structure, listening closer you hear the sounds of strange inhuman creatures deeper inside the dark structure.",
        'solved': False
    },
    'a2': {
        'description': "You find yourself standing before a towering city, filled with the sounds of the townspeople prospering.",
        'event': "You encounter the city guard they try to arrest you for a crime you did not commit",
        'solved': False,
        'event_result': event_city_guard,
        'enemy': corrupt_guardsman
    },
    'a3': {
        'description': "You stand before a tranquil forest, it's peaceful.. stay awhile and enjoy the peace..",
        'event': "You hear the roar of a grizzly, it approaches quickly..!",
        'event_result': event_grizzly,
        'solved': False
    },
    'a4': {
        'description': "You stand in an empty green field",
        'event': "You see a glimmer in the distance, what could it be?",
        'event_result': event_field,
        'solved': False,
        'enemy': goblin
    },
    'b1': {
        'description': "Entering the dark structure, the light seems to attempt to penetrate the dark, but alas you feel the cold dark presence.",
        'event': "You find a Skeleton holding an axe, do you attempt to take the axe?",
        'event_result': event_skeleton_axe,
        'solved': False,
        'enemy': skeleton
    },
    'b2': {
        'description': "Deep in the city walls you come across a strange hut covered in occult symbols, you feel it draw you in. ",
        'event': "Inside the hut you discover an ancient manuscript, as you hold the book it surges with unknown energy, do you attempt to understand the texts?",
        'event_result': event_cursed_book,
        'solved': False
    },
    'b3': {
        'description': "Deeper in the forest, you come across a peaceful group of creatures they allow you to tread in there lands",
        'event': "You attempt to speak to the creatures, asking for guidance to further your path",
        'event_result': event_peaceful_creatures,
        'solved': False
    },
    'b4': {
        'description': "In the vast nothing you come across a grand structure picturing a god of old.",
        'event': "You see offerings at the shrine to the old god something attracts your attention",
        'event_result': event_old_god,
        'solved': False
    },
    'c1': {
        'description': "In the dark of the structure, you feel a presence older than time itself, you feel it watching in the dark.",
        'event': "You hear a voice in a tongue you don't understand beckoning you to travel deeper into the structure",
        'event_result': event_dark_presence,
        'solved': False,
        'enemy': skeleton
    },
    'c2': {
        'description': "Further into the city you have arrived at the fortress inner gates, walls tower into the clouds unable to see the peaks.",
        'solved': False,
        'enemy': corrupt_guardsman
    },
    'c3': {
        'description': "In the deepest reaches of the forest you come to find a tribe of native neutral creatures, they greet you.",
        'solved': False,
        'enemy': goblin
    },
    'c4': {
        'description': "Further stretched a far, an unnatural body of water stands before you, strange runes carved into the sand stretching the lake.",
        'event': "You see a shape flow the stretch of the lake, it calls to you to enter the water.",
        'event_result': event_mythos_lake,
        'solved': False,
        'enemy': fishman
    },
    'd1': {
        'description': "You Have reached the end of the structure, an ancient demon sits upon the bodies of previous adventurers, it stands tall and laughs in your presence.",
        'solved': False,
        'enemy': ancient_demon
    },
    'd2': {
        'description': "In the Sanctum something is not right, the king on the throne is not who he says he is, You see through his facade. You see a demon puppeteering his hollow shell.",
        'solved': False,
        'enemy': impostor_king
    },
    'd3': {
        'description': "The native creatures lead you into the centre of there village they allow you to stay and rest.",
        'solved': False
    },
    'd4': {
        'description': "Falling into the lake you are transported to another plane of existence, strange creatures all around you are faced with horrors unimagined.",
        'event': "You continue to look into the face of madness",
        'event_result': event_old_one,
        'solved': False,
        'enemy': fishman
    }
}

solved_places = {f"{row}{col}": False for row in "abcd" for col in range(1, 5)}


if __name__ == "__main__":
    menu_screen()