# CS170-EightPuzzle

## About the Code

Assignment 1 for CS170: Intro to AI at UCR. We were tasked to create a program that would take a given Eight Puzzle and solve it with A* utilizing one of three possible heuristics: Uniform Cost Search, Misplaced Tiles, and Manhattan Distance.

To run the program please typle in ```python eightpuzzle.py``` which will then allow you to use the GUI interface to insert a puzzle and choose the heuristic.

## Results

The following graphs show the Nodes Expanded vs. Solution Depth and Max Queue Size vs. Solution Depth respectively. Please note that Uniform Cost Search timed out after depth 20. Nodes Expanded helps us get an idea of the time complexity of the heuristics while Max Queue Size helps us get an idea of the space complexity for each heuristic.
