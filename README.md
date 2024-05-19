# Intro-to-AI-Labs
## Lab 1   
### 8 Game application with AI Agent
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
* Play the game yourself or use an agent.
* On the right, all the properties of the algorithm is displayed.
* Clicking 'next' or 'prev', will change between moves.
* Clicking 'show moves', will automatically play the moves towards the solution.

![image](https://github.com/Ali-Mones/Intro-to-AI-Labs/assets/128807308/8fcd11eb-1886-4afb-8df3-20890399efe8)

When there is no solution, it is simply stated.
      
![image](https://github.com/Ali-Mones/Intro-to-AI-Labs/assets/128807308/471ead6b-9a02-471a-82c1-f77c27a60c46)

## Lab 2   
### Connect 4 Game Application with AI Agent
### Overview
This application is a graphical implementation of the Connect 4 game, developed using Pygame. It includes an AI agent that can play against a human player. The AI uses various search algorithms such as Minimax and Alpha-Beta Pruning.   
*The score is the total number of 4 consecutive dots.*
### Features
* Interactive GUI: Built with Pygame, allowing a human player to play against the AI.
* Multiple AI Algorithms: Implements Minimax and Alpha-Beta Pruning.

### Installation
Prerequisites
* Python 3.x
* Pygame
### Steps
* Clone the repository:
```
https://github.com/Ali-Mones/Intro-to-AI-Labs/tree/main/Lab_2
```
### Install the required packages:
```
pip install pygame
```
### Run the application:
```
python main.py
```
### AI Algorithms
#### Minimax
* Description: A decision-making algorithm used for minimizing the possible loss while maximizing the potential gain.
* Characteristics: Considers all possible moves, but can be slow for deep searches.
#### Alpha-Beta Pruning
Description: An optimization of the Minimax algorithm that eliminates branches in the search tree which don't need to be explored.
Characteristics: More efficient than Minimax, allowing deeper searches in less time.
Project Structure
### Snippets   
![image](https://github.com/Ali-Mones/Intro-to-AI-Labs/assets/128807308/589375d5-0204-464e-a731-48bb9c370411)
* Choose the depth
![image](https://github.com/Ali-Mones/Intro-to-AI-Labs/assets/128807308/162f54ac-6f6d-44aa-b39f-4b518ec392f1)
* Note that you can traverse the search tree by clicking on the nodes.
![image](https://github.com/Ali-Mones/Intro-to-AI-Labs/assets/128807308/7d1f93ec-ae6d-4869-8da3-8870d065afe4)
* The fina score is displayed on the top right
![image](https://github.com/Ali-Mones/Intro-to-AI-Labs/assets/128807308/3e6d69ed-b19e-4288-a308-937565cd8951)


## Lab2
## Markov Decision Processes   
![image](https://github.com/Ali-Mones/Intro-to-AI-Labs/assets/128807308/363d316b-75c5-4c65-b253-21f9bedb11c0)   
The agent has four actions Up, Down, Right and Left.
The transition model is: 80% of the time the agent goes in the direction it selects; the rest of
the time it moves at right angles to the intended direction. A collision with a wall results in no
movement.   
   
![image](https://github.com/Ali-Mones/Intro-to-AI-Labs/assets/128807308/76d5b476-af86-4190-99c0-c7077bc773df)   
   
1. .Implemented value iteration for this world for each value of r below:   
• r = 100   
• r = 3   
• r = 0   
• r = -3   
2. Used discounted rewards with a discount factor of 0.99
3. Showed the policy obtained in each case.
4. Explained intuitively why the value of r leads to each policy.

