![Static Badge](https://img.shields.io/badge/Version%201.0-blue)

# Boomfinder
A minesweeper-like game

## It's Playable!
The game isn't finished, but we can call this version 1.0! Player can now flag spaces and clear regions. I want to optimize some of the functions, but pretty much everything is working! 

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
#### 3. Select Your Move
The first thing the game will ask is for the player to select a move type. This can be "Reveal" - select a square to see if there's a bomb or not, "Clear" - select an already-revealed spot to clear the adjacent squares (if you've flagged the right number of spaces), or "Flag/Unflag" - mark a square as having a bomb; this square can not be revealed until it is unflagged.

#### 4. Select Your Space
The game will ask for a row and a column in the form of `row, column`. The first selection should never be a bomb (if I've done this right!), but after that, all bets are off! The game progresses until the player either chooses a space that has a bomb, or has uncovered all of the spaces. If the player selects a space they've already explored, the game will alert them and ask for another choice. 

## Customizing the Game
Originally, I set the game to be a 6x6 grid with 5 bombs. If you wanted to tweak the game, you needed a text editor to edit `grid.py` file, in the lines:

```python
board_width = 6
board_height = 6
number_of_bombs = 5
```

However, since then, I've added user input to determine the size of the game. At the moment, it only asks when you start the program for the first time, and all continue plays use the same parameters. The defaults are 6x6 with 5 bombs. The max width is 10 and the max height is 40. Anything wider than 10 looks wonky in CLI. 40 is also way too tall, but if you really want a challenge. Max number of bombs is `width x height - 1`.

## To Come
At some point, I need to clean up all the code, organize it better, and create a shell script to simplify running.

Also, more information about game progress. [done-ish]

A way to clear swathes of the board (as in the classic game - if you select a space with no bombs around it, they should all clear). THIS IS WAY MORE COMPLEX THAN I'D THOUGHT IT WOULD BE!

A "help" or "instructions" option. I don't think the game is too confusing, but I wrote it, so who knows?

And, once I get that all working - GRAPHICS!