# State Space Search — Water Jug Problem

## Overview

The **Water Jug Problem** is a classic search problem. Given two jugs of capacity *m* and *n* litres (with no markings), the goal is to measure exactly *d* litres using a series of pour operations. The problem is modelled as a **state space** and explored using search algorithms.

## Concepts Covered

- State space representation
- State transitions (fill, empty, pour)
- Uninformed search in a state space graph
- Detecting goal states and avoiding revisited states

## Files

| File | Description |
|------|-------------|
| `State Space Search Water Jug.ipynb` | Full implementation and trace |
| `Report.pdf` | Reference material |

## How to Run

```bash
jupyter notebook "State Space Search Water Jug.ipynb"
```

## State Space

- **State:** `(x, y)` where `x` = litres in jug 1, `y` = litres in jug 2
- **Initial state:** `(0, 0)`
- **Goal state:** any state where `x == d` or `y == d`

## Possible Operations

| Operation | Description |
|-----------|-------------|
| Fill Jug 1 | `(x, y) → (m, y)` |
| Fill Jug 2 | `(x, y) → (x, n)` |
| Empty Jug 1 | `(x, y) → (0, y)` |
| Empty Jug 2 | `(x, y) → (x, 0)` |
| Pour 1→2 | `(x, y) → (x - d, y + d)` |
| Pour 2→1 | `(x, y) → (x + d, y - d)` |