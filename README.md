# Final Assignment
What the game is about:

The game is a 1v1, PVP fighting game inspired by the combat mechanics found in Dark Souls 3 and other FromSoft games, of which I am a huge fan. Obviously, I'm not at the level where I can replicate the game using Python and Kivy, so instead I decided to make the game based on a top down view to accomodate the 2D movement. My hope is that the game will offer a compelling combat experience which rewards skill and patience and punishes cheesy tactics, much like combat in Souls games.

How to play:

To begin the game, run HappySols.py

The goal of the game is to beat the other player and you win when you manage to drop the other player's health to zero, which is done by attacking them. 

Players share the keyboard and besides the typical up, down, left and right movement keys, have an attack, roll, and special button.

Before starting the game, players will be met with a character and weapon selection screen. While the character selection is purely cosmetic, the three weapon options will change gameplay dramatically as they have different specials, damage, attack speed and other attributes. Players can also change their controls by typing in a string of 7 characters in the order: up, down, right, left, attack, roll, special, then clicking on the confirm controls button.

Attacking:

Each weapon has a unique attack animation and range. Swords are the fastest weapon but do the least damage. Lances have good reach and higher damage but are also narrower and attack slower. Great hammers are the slowest weapon but hit the hardest and have a huge range.

Rolling:

All players are able to roll, giving them i-frames in the midst of it.

Special:

Each weapon has its own special move that changes playstyle dramatically:

Swords - parry: For a brief period, parry any attack that hits you. Players who attack you will are temporarily stunned and you can attack them for extra damage.

Lance - guard: Hold up your shield to halve all incoming damage. You move slower and cannot recover stamina while guarding.

Great Hammer - smash: Charge up your strength and release it to smash the ground beneath you, dealing damage to anyone around you.

Code organization:

The game code has been split into four separate files to make editing easier:

HappySols.py - main game file which is used to run the game

FightArea.py - Contains the screen class which contains information for the game being run, and also contains animation functions

Character.py - Contains the character class and all methods related to the character widget

Weapon.py - Contains the weapon classes and all methods related to the weapons

OtherMenus.py - Contains information on the rest of the screens of the game, as well as functions for when menu buttons are pressed

The rest of the game consists of sound and image files which are used in the game.

HappySols.py:

This file imports custom screen classes from OtherMenus.py and adds them an instance of the kivy screen manager class.
The code then creates a custom class definition of the kivy app which returns the aforementioned screen manager instance under its build function.
Finally the code runs the app using app.run()

FightArea.py:

This file contains the FightArea class which is a custom Screen class. The FightArea class is where the main game takes place. As such it takes in multiple arguments during its instantiation, most importantly the character objects and weapon objects that will be interacting with each other in the game. The class then adds these widgets and starts the kivy Clock.schedule_interval function to repeatedly run the methods of the character and weapon objects to continuously update the game situation.

Character.py:

The bulk of the coding lies in this file where the methods for the custom Widget class named Character can be found. The reason there are so many functions is because the combat requires the character to have different states which last different durations, so there are many functions which simply set the states back to their default values. This is so that I can choose how long I want the state to last using Clock.schedule_once. More importantly are the move_step and damage_check methods which will be repeatedly called every frame in the FightArea Screen. The move_step function checks for keys that are being pressed, and performs the appropriate action accordingly if they correspond to a player control. The move_step function also updates the position of the drawing of the players and weapons, and information on not just movement but also the other three player controls like attacking, etc. The damage_check function checks for collision between a weapon and the opposing player and performs the appropriate calculations based on the receiving player's state. The damage_check function also updates the size of the health bar to reflect damage taken by the players. There is also and update_visuals function to contain information on updating visuals because the move_step function was getting too huge.

Weapon.py:

Contains code for the three different weapon classes. Each weapon type will manifest as an object in the game and have its own drawing and movement pattern, hence three separate classes were made. They all have mostly the same methods but different parameters for things like their damage and stamina cost. Weapon specials abilities are actually coded for in the move_step function in the Character class, due to the special interactions involving the opposing player.

OtherMenus.py:

This file contains code for the Controls and Menu screen. The Controls screen is particularly important as the play button on this screen will create a new instance of FightArea everytime it is pressed, using options selected in the Controls screen as parameters to instantiate the FightArea object. 


