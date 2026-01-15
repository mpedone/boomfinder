![Static Badge](https://img.shields.io/badge/Version%201.1-blue)

# Boomfinder
A minesweeper-like game



## Getting Started

### Prerequisites
 * [Python3](https://www.python.org/downloads/) (download page on python.org)
 * Some knowledge of [CLI](https://en.wikipedia.org/wiki/Command-line_interface)

#### 1. Clone This Repo
```shell
git clone https://github.com/mpedone/boomfinder.git
cd boomfinder
```

## Playing the Game
### 1. Run `main.py`

```shell
python3 main.py
```

### 2. Set up the board
The program gives you the option to set the height and width of the game board, as well as the number of bombs. If the field is left blank, the game will revert to its default settings of 6x6 with 4 bombs. If you want to let the game to decide how many bombs to use based on your custom board, leave the third entry blank. There is a math function that will calculate the number of bombs based on the classic Windows version (9x9 with 10 bombs, 16x16 with 40 bombs, and 16x30 with 99 bombs). The max width is 10 (because this is command line, and anything over that gets wonky with the double digits). The max height is 40 (though, again, in command line, this is tough to display). The max number of bombs is `height*width-1`, because you need to be able to select at least one square. Of course, this is a trivial game, as you'll win in one move. Minimum size is 3x3. The minimum number of bombs is 1, because anything less would just be silly.

### 3. Gameplay
Welcome to BOOMFINDER! Your goal is to reveal all of the 'safe' squares on the board, and avoid all of the BOOMs!

To set up the intial game board, select a width (3 - 10), a height (3 - 40), and number of bombs (minimum of 1, max of (width x height)-1). Leave any of these blank to use the default width and height, or to have BOOMFINDER calculate the optimal number of bombs for your grid.

1. Choose an action by typing the first letter (case insensetive) and pressing enter. You can take one of 3 actions: 
    1. You can REVEAL an unflagged square.
    2. You can CLEAR a region of squares.
    3. You can FLAG (or unFLAG) a square.
2. Next, choose a square by entering its coordinate in the form row, column where "row" and "column" are numbers.
3. The board will upated to display the result of the move, the number of flags you have remaining (which is also the number of BOOMs to find), the number of spaces you've cleared, and the number of spaces remaining to clear.
4. The game ends when you either clear all the spaces or reveal a BOOM

Notes:
On your first turn, you can only REVEAL or FLAG. On all other moves, CLEAR is available.

REVEAL: Reveal shows what is beneath the square - either blank, a number, or a BOOM. The number (or blank) indicates how many BOOMs are in the 8 squares surrounding it. '1' means that there is only 1 BOOM in the surrounding squares. 2 means there are 2, and 8 means that square is fully surrounded by BOOMs! Blank means that there are no bombs in any of the surrounding squares. You cannot reveal a flagged square. Revealing a square that has already been revealed has no effect.

If you find a BOOM, it's game over, so be careful!

FLAG: Flag allows you to mark a square that you suspect has a BOOM beneath it. If you've mistakenly flagged a square, simply use the FLAG move again to unflag the square.

CLEAR: Clear allows to to clear all unrevealed and unflagged squares surrounding a revealed square, but only if you have flagged the correct number of squares. For example, if you choose square (3,4) and the number revealed is '2', you must flag 2 of the surrounding squares before you can use CLEAR on (3,4). CLEAR will reveal all the unflagged squares, so if you flagged correctly, it's a quick way to reveal the board. If you haven't, you'll find a BOOM and the game will be over!

When the game ends, you have the option of continuing with the same setup, or resetting the board.

Enter 'q' at any time to quit the game.

## Notes
### Version History
Version 1.0: Game is fully playable. Starting a new game used the same setup. No help/instructions option.
Version 1.1: New game allows user option of resetting board. Instructions included as an option. Modified the selections to be more robust. "q" now quits from any selection. "h" brings up the help/instructions from any selection (except the game over selections). Random ascii-art title graphics.

### To Come
At some point, I need to clean up all the code, organize it better, and create a shell script to simplify running.

Also, more information about game progress. [done-ish]

A way to clear swathes of the board (as in the classic game - if you select a space with no bombs around it, they should all clear). THIS IS WAY MORE COMPLEX THAN I'D THOUGHT IT WOULD BE!

And, once I get that all working - GRAPHICS!

### Title Graphic
I've added some ascii art as a title graphic. As my tastes change, I've added a few different versions, with a randomizer to pick one, so each time you run the program, it might be different. I used two websites: [TAAG](https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type+Something+&x=none&v=4&h=4&w=80&we=false) and [Text to ASCII](https://www.asciiart.eu/text-to-ascii-art). I don't think either requires attribution, but I don't feel right *not* giving them credit. *I* didn't take the time to figure this out!