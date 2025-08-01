# Perilous Python V1.0 #

Welcome to the first iteration of my first Python based Game!

The game is designed only using python, currently.

The game is a text based Adventure/RPG

- The aim of the game is simple, to find the ancient demon and defeat them.
- Features of the game;
  - Turn based combat that uses dice rolls to modify damage/defences.
  - Exploration is encouraged as there are events/items to discover to enrich the player experience.
  - Fully functioning inventory, at this stage effect health/attack rating in future iterations plan to include triggers and item based quests.

- The game is set on a column based map, a1 -d4. Navigation is simple at this stage but will be iterated upon in further development.

## Setup/Install ##

To run this code based game you will need the following installed.

1. VS Code running at the current version, or another code interpreting software (sublime, Atom etc.)
2. Python language installed to version 3.12.3.
3. No packages need to be installed libraries that have been utilised do not require any installation.
4. Ensure you are currently in the same file location as the main.py file otherwise the program will not execute.

## System Requirements ##

- Operating system, minimum Windows 10 or Mac OS 10.11 or later or Ubuntu 16.04+ for linux.
- Processor 1.6GHz or faster
  - 4GB of RAM
  - VS code only requires 500mb of storage & this application would be smaller than this.
  - Display resolution recommended is 1024 by 768 as a minumum.
  - No GPU requirements as all code based.

### Running Program ###

To run the program, simply enter the below into your terminal.

- python3 main.py

### How to Play ###

To engage with the program the instructions are provided through prompts and error handling throughout the game.

To engage in the functions of the game it is broken down as per below.

- Movement
  - To move in the game simply typing (UP, LEFT, RIGHT, DOWN) to navigate. there is no visual map however the program will advise if your able to travel.
- Combat
  - Combat is currently set as a location based encounters and is triggered when entering specific locations. Currently there is one main boss and a secondary optional boss.
    - Combat is turn-based and uses dice rolls to determine damage numbers/defence.
    - Item use can be used during and outside of combat (Health Potions as an example)
- Save Game
  - You can save at any time to save your progress, simply type 'save' or 'save_game' at any time. it will save your stats, location and completed events. However enemies will respawn if you load into the game. This is intentional to give an additional challenge.
- Load Game
  - Load game is simple in the main menu type 'load' and you will be returned to where you left off!.
- Interactions
  - To interact with the world you can type 'look' to gain a decription of your environment.
  - 'interact' will allow you to interact with events and items in the world.

## Libraries Utilised ##

Currently all libraries utilised are part of Pythons library packages that come installed with the product, they do require a import statement. However no requirement for users to do this.

- OS Library.
  - OS has been utilised for clearing excess data on the terminal for ease of reading for users.
  - Is covered under the Python Sofware foundation license (PSFL).
  - It is considered open source use for all projects.
  - Classed as ethical use and non-breach of terms of license.

- SYS Library
  - SYS library is utilised for app kill functions, for game completion or user requesting to quit the app.
  - SYS is covered by the PSFL V2, it is permissive open source license that allows free use of the components.
  - No breach or implications of copywright.

- Random Library.
  - Random has been utilised for dice rolls in the form of integers to modify damage and defence numbers.
  - random is covered under the PSF license.
  - The license is permissive open source, if in wider distribution more robust copyright messaging will be included in future.

- JSON Library
  - JSON has been utilised to create save states and load state based files for ongoing play of the game.
  - JSON is covered under the PSF License, permissive open source, same as above with Random library.
  - JSON Software shall be used for Good, not Evil.

- Logging Library.
  - Logging is utilised for combat error logs, used for DEV purposes.
  - Covered under the PSF license, permissive open source.
  - Does not breach any ethical or copyright breaches as used solely or bug fixing.

## Errors ##

There is error logging in use during combat, if you encounter any error please copy a file that will be in your folder. Please review and contact the DEV team.
