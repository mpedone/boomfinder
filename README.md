![Static Badge](https://img.shields.io/badge/Version%200.1-blue)

# Boomfinder
A minesweeper-like game

## It's Playable!
The game isn't finished, but we can call this version 0.1.

## Getting Started

### Prerequisites
 * [Python3](https://www.python.org/downloads/) (download page on python.org)
 * Some knowledge of [CLI](https://en.wikipedia.org/wiki/Command-line_interface)

#### 1. Clone This Repo
```shell
git clone https://github.com/mpedone/boomfinder.git
cd boomfinder
```

#### 2. Run `grid.py`

As noted, this is very unfinished, thus the playable game isn't in `main.py`, nor do I have a shell script to run it yet.

```shell
python3 grid.py
```

#### 3. Select Your Space
The game will ask for a row and a column. At the moment, the player cannot change their column selection once they press enter, so choose carefully. The first selection should never be a bomb (if I've done this right!), but after that, all bets are off! The game progresses until the player either chooses a space that has a bomb, or has uncovered all of the spaces. If the player selects a space they've already explored, the game will alert them and ask for another choice. There is no way to mark which spaces have bombs (yet), so you have to keep in mind where the bombs are!

## Customizing the Game
I've set the game to be a 6x6 grid with 5 bombs, as the CLI can be a little clunky/confusing to play in. If you'd like to tweak the game, and have a text editor, you can open the `grid.py` file and look for the lines:

```python
89  board_width = 6
90  board_height = 6
91  number_of_bombs = 5
```
Change those as you see fit.

## To Come
My next goal is to give the player the option to set the grid as they see fit, instead of having to edit the code. [done]

Currently working on validating a move. Should be numeric, not already selected, and within the limits of the board.

At some point, I need to clean up all the code, organize it better, and create a shell script to simplify running.

Also, more information about game progress.

A way to flag spaces that (the player thinks) have bombs, and have them not be selectable.

A way to clear swathes of the board (as in the classic game - if you select a space with no bombs around it, they should all clear).

A way to manually clear the surrounding spaces if the correct number of flags have been planted.

And, once I get that all working - GRAPHICS!