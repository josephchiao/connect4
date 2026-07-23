# connect4

A terminal Connect Four game with an AI opponent that combines a **neural network** (trained by a **genetic algorithm**) with **alpha-beta minimax tree search**.

## What it does

- **Playable Connect Four** in the terminal — play against another human or against the AI.
- **Neural-network evaluation** — board positions are scored by a feed-forward network implemented from scratch in NumPy (`neural_network.py`).
- **Genetic-algorithm training** — instead of backpropagation, networks are evolved: they play against each other, and the strongest are selected, mutated, and reproduced over generations (`genetic_algorithm.py`, `mutation.py`, `reproduction.py`).
- **Alpha-beta tree search** — the network's evaluation is combined with minimax search and alpha-beta pruning to look ahead several moves (`tree_search.py`, `branch.py`).

## How to play

```bash
python interface.py
```

Enter a number from **1–7** to choose the column where you want to drop your token. `Y` = Yellow, `R` = Red, `-` = empty.

By default `interface.py` runs a player-vs-computer game. The file also contains `player_vs_player()` and self-play routines used during training — call whichever you want at the bottom of the file.

## Repository layout

| File | Purpose |
|------|---------|
| `interface.py` | Game loop and terminal UI (entry point) |
| `gameplay.py` | `Game` class — board state, move handling, win/draw detection |
| `setup.py` | Board generation and setup helpers |
| `neural_network.py` | From-scratch feed-forward network used to evaluate positions |
| `feedforward_prop.py` | Forward-propagation routines |
| `tree_search.py`, `branch.py` | Alpha-beta minimax search |
| `genetic_algorithm.py` | Evolutionary training loop |
| `mutation.py`, `reproduction.py` | Genetic operators |
| `theta_init.py` | Weight initialization |
| `genetic_parent_data/` | Saved network weights for evolved "parent" agents |
| `archive/` | Older versions kept for reference |

## Requirements

- Python 3.8+
- `numpy`, `matplotlib`

```bash
pip install numpy matplotlib
```

## Notes

Personal machine-learning project. Note that `genetic_algorithm.py` contains some hard-coded absolute file paths from the original development machine — update these before running training on your own setup.
Run the interface.py file to play. Input 1~7 to indicate the row you want to place your token. 
