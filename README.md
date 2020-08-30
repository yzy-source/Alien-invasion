# Alien-invasion
A game named 'Alien-invasion'

The player controls a spaceship that initially appears at the bottom center of the screen. Use the left and right arrows to move the spaceship and use the space bar to shoot. At the beginning of the game, a group of aliens appeared in the sky. They moved down to the screen. The player's task was to shoot these aliens. After the player wipes out all the aliens, a new group of aliens will appear, and they will move faster. As long as an alien hits the player’s spaceship or reaches the bottom of the screen, the player will lose a spaceship. After the player loses three spaceships, the game ends.

## alien_invasion.py
The main running file which creates a series of objects used in the game: settings, main surface, a spaceship instance, and the main loop of the game.

## settings.py
Contains the Setting class, and the method init(), which initializes and controls the appearance of the game and the speed properties of the spaceship.

## game_functions.py
Contains a series of functions to complete the game: detecting button pressing and releasing, handling these events, and managing the movement of the spaceship. Contains the function update_screen() to redraw the screen every time the main loop is executed.

## alien.py\/ship.py\/bullet.py\/button.py
Initialize and manage aliens, ships, bullets and buttons

## scoreboard.py
Manage scoreboard: displaying score information, level, highest score, and the number of remaining ships etc..

## game_stats.py
Statistic theinformation of the game score. 

## images
Images representing spaceships and aliens
