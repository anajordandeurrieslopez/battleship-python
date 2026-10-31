# Battleship in Python

A terminal-based Battleship game built with Python as a university programming project.

## Features

- Single-player mode against an automated opponent.
- Two-player mode on the same computer.
- Ship placement on a 10 × 10 board.
- Turn-based shooting with hit and sunk indicators.
- Save and load functionality using a text file.

## Requirements

Python 3.9 or later. No external dependencies are required.

## How to play

Download the project and keep all Python files in the same folder.

From that folder, run:

```bash
python main.py
```

The interface is in Spanish. At the first prompt, enter:

- `empezar una nueva` to start a new game.
- `continuar una partida` to load an existing saved game.

For a new game, choose one or two players and follow the prompts to place your ships and take turns firing.

Loading a game requires a previously created `partida_guardada.txt` file in the working folder.

## Project structure

- `main.py`: game entry point and turn management.
- `barcos.py`: ship placement and automated fleet generation.
- `disparo.py`: shooting logic and victory checks.
- `tablero.py`: board creation.
- `guardar.py`: saving and loading games.
- `excepciones.py`: custom exceptions.
- `test.py`: basic checks for victory detection and ship placement boundaries.

## Basic checks

Run the included checks with:

```bash
python test.py
```

These checks cover selected functions rather than the full gameplay.

## Academic context

This project demonstrates modular programming, game logic, input handling, and persistence with text files.
