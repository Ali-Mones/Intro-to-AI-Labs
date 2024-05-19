﻿# Intro-to-AI-Labs
## Lab 1   
### Overview   
An instance of the 8-puzzle game consists of a board holding 8 distinct movable tiles, plus
an empty space. For any such board, the empty space may be legally swapped with any tile
horizontally or vertically adjacent to it. In this assignment, the blank space is going to be
represented with the number 0.
Given an initial state of the board, the search problem is to find a sequence of moves that transitions this state to the goal state; that is, the configuration with all tiles arranged in ascending order 0,1,2,3,4,5,6,7,8.
The search space is the set of all possible states reachable from the initial state. The blank space may be swapped with a component in one of the four directions ’Up’, ’Down’, ’Left’, ’Right’, one move at a time. The cost of moving from one configuration of the board to another is the same and equal to one. Thus, the total cost of path is equal to the number of moves made from the initial state to the goal state.      
   
![image](https://github.com/Ali-Mones/Intro-to-AI-Labs/assets/128807308/b768b730-6f9f-4378-8fc2-63dc0b805d30)   

### Features
 * Interactive GUI: Built with Pygame, allowing users to manually solve the puzzle or watch automated solutions.
 * Multiple Search Algorithms: Implements DFS, BFS, and A* Search to solve the puzzle.
 * For the A* (the informed search) we are going to use Manhattan heuristic and Euclidean
heuristic and compare between number of nodes expanded and output paths, and to report
which heuristic is more admissible.
 * Step-by-Step Visualization: Visual representation of the solving process for each algorithm.

### Installation
Prerequisites
* Python 3.x
* Pygame

### Steps
* Clone the repository:
```
https://github.com/Ali-Mones/Intro-to-AI-Labs/tree/main/Lab_1
```
```
cd '8 Game'
```
* Install the required packages:
```
pip install pygame
```
* Run the application:
```
python main.py
```
### Snippets   

![image](https://github.com/Ali-Mones/Intro-to-AI-Labs/assets/128807308/87a7eb2e-b091-4a2f-8cbb-0b86e80590fb)   
   
* Change the starting board as you like by dragging and dropping tiles.   
* When 'start' is clicked, you can choose what searching algorithm to do.   
* On the right, all the properties of the algorithm is displayed.
* Clicking 'next' or 'prev', will change between moves.
* Clicking 'show moves', will automatically play the moves towards the solution.

![image](https://github.com/Ali-Mones/Intro-to-AI-Labs/assets/128807308/8fcd11eb-1886-4afb-8df3-20890399efe8)

When there is no solution, it is simply stated.
      
![image](https://github.com/Ali-Mones/Intro-to-AI-Labs/assets/128807308/471ead6b-9a02-471a-82c1-f77c27a60c46)

## Lab 2   
### Overview
