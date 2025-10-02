# IA-Tetris

Autonomous Agent for Tetris – Artificial Intelligence Project 2021/2022

Developed by:

- Nuno Cunha (98124)
- Bernardo Kaluza (97521)
- Pedro Lima (97860)
- Diogo Gomes
- Luís Seabra Lopes

## Demo

Check out the demo video here: https://www.youtube.com/watch?v=2Kd3KGwfX5Y

## Project Overview

This project implements an autonomous agent capable of playing Tetris. It was developed as part of the Artificial Intelligence course (2021/2022).

The system is divided into three components:

- Server – runs the game logic.
- Viewer – visualizes the game in real-time.
- Client – controls the Tetris agent or allows human play.

The AI agent makes decisions by simulating possible moves, evaluating game states, and selecting the optimal sequence of actions.

## AI Agent Architecture
### Piece Detection

- Detects the current piece (state['piece']) using a dictionary that maps spawn positions to the corresponding shapes and rotations.
- Returns a Shape object and its rotation index.

### Simulation

- Calculates all possible positions for the current piece.
- Assigns a score to each possible move.
- Returns the move with the highest score.

### GenerateInputs

- Simulates placing a copy of the piece in a target position.
- Returns the required key sequence and final position.

### Move Class

- Calculates scores for all potential positions.
- Scoring is based on game state features (e.g., holes, height, completed lines).
- Weights were tuned via trial-and-error for performance across multiple seeds.

## Installation

Make sure you are running Python 3.7+.

    $ pip install -r requirements.txt


Tip: It’s recommended to use a virtual environment.

## How to Play

Open 3 terminals and run:

    $ python3 server.py
    $ python3 viewer.py
    $ python3 client.py


- If you want to play manually, use the arrow keys in the Pygame client window.
- If you let the AI agent run, it will automatically play the game.

## Controls

- Left / Right arrows → Move piece
- Up arrow → Rotate
- Down arrow → Soft drop

## Debugging

Check if pygame is correctly installed:

    $ python -m pygame.examples.aliens

## Tested On

macOS Big Sur 11.6
