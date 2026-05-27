# Breadth-First Search — 8 Puzzle

## Overview

The **8-Puzzle** is a sliding tile puzzle on a 3×3 grid with 8 numbered tiles and one blank. The task is to reach a goal configuration from an initial scrambled state. Solved using **Breadth-First Search (BFS)**, guaranteeing the shortest solution path.

## Concepts Covered

- Problem formulation (state, actions, transition model, goal test)
- Uninformed (blind) search strategies
- Breadth-First Search — completeness and optimality
- State representation as a 2D matrix or flat list
- Frontier management using a queue (FIFO)
- Visited-state tracking to avoid cycles

## Files

| File | Description |
|------|-------------|
| `Breadth First Search 8 Puzzle.ipynb` | BFS implementation and solution trace |

## How to Run

```bash
jupyter notebook "Breadth First Search 8 Puzzle.ipynb"
```

## Problem Formulation

- **State:** 3×3 grid configuration, e.g. `[[1,2,3],[4,0,5],[7,8,6]]` (0 = blank)
- **Actions:** Slide blank Left / Right / Up / Down
- **Goal state:** `[[1,2,3],[4,5,6],[7,8,0]]`
- **Cost:** Each move costs 1 (BFS gives optimal solution)

## Algorithm — BFS

```
frontier = Queue([initial_state])
visited  = {initial_state}

while frontier not empty:
    node = frontier.dequeue()
    if node == goal: return path
    for each successor of node:
        if successor not in visited:
            visited.add(successor)
            frontier.enqueue(successor)
```

## Complexity

| Property | Value |
|----------|-------|
| Time | O(b^d) |
| Space | O(b^d) |
| Complete | Yes |
| Optimal | Yes (unit costs) |

where *b* = branching factor ≈ 3, *d* = solution depth.