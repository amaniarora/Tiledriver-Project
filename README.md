# Tiledriver-Project


The tiledriver is a game aider in which players input a series of shuffled numbers that repersent tiles on a 2 x 2 or a 4 x 4 board. There will be one square on each "board" that is empty and allows the other tiles to slide past. The empty square is repersented with a 0 during player input. The goal is to order the "tiles" in ascending order by sliding the "tiles" up, down, right, or left.

There are three functions within the Tiledriver project that help the player solve the problem:

1) MAKE ADJACENT: the program finds all the possible next moves for the initial "tile" placement
2) SOLVABLE: the program uses a merge sort algorithm to determine whether the inputted tile configuration is solvable or not
3) SOLVE: the program uses a uniform cost search method to find the solution of the game in the least number of moves
