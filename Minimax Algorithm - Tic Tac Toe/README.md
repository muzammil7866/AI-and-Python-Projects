# Minimax Algorithm — Tic Tac Toe

## Overview

A fully playable **Tic-Tac-Toe** game where the AI opponent uses the **Minimax algorithm** to play optimally. The AI explores the complete game tree and chooses the move that maximises its chances of winning (or minimises losses).

## Concepts Covered

- Adversarial (two-player, zero-sum) game representation
- Game tree search
- Minimax algorithm (MAX and MIN players)
- Terminal state detection (win / draw / lose)
- Optimal strategy — the Minimax agent never loses

## Files

| File | Description |
|------|-------------|
| `Minimax Tic Tac Toe.ipynb` | Full Minimax implementation and game loop |

## How to Run

```bash
jupyter notebook "Minimax Tic Tac Toe.ipynb"
```

## Minimax Algorithm

```
function minimax(state, isMaximising):
    if terminal(state): return utility(state)

    if isMaximising:
        best = -∞
        for each move in state:
            best = max(best, minimax(apply(move), False))
        return best
    else:
        best = +∞
        for each move in state:
            best = min(best, minimax(apply(move), True))
        return best
```

## Game Properties

| Property | Value |
|----------|-------|
| Players | 2 (X = human, O = AI) |
| Branching factor | ≤ 9 (shrinks as game progresses) |
| Max depth | 9 moves |
| State space | 9! = 362,880 (upper bound) |
| AI strategy | Optimal (never loses) |