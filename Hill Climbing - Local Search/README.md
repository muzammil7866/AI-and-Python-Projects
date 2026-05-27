# Hill Climbing — Local Search

## Overview

Implements the **Hill Climbing** local search algorithm, an iterative improvement technique that continuously moves toward better neighbouring states. Unlike systematic search, it requires no frontier or visited list — making it memory-efficient but susceptible to local optima.

## Concepts Covered

- Local search vs. systematic search
- State evaluation / objective function
- Hill Climbing (Steepest-Ascent variant)
- Problems: local maxima, plateaus, ridges
- Variants: Random-Restart Hill Climbing, Simulated Annealing (as improvement)

## Files

| File | Description |
|------|-------------|
| `Hill Climbing Local Search.ipynb` | Full implementation with problem demonstration |

## How to Run

```bash
jupyter notebook "Hill Climbing Local Search.ipynb"
```

## Algorithm

```
function hill_climbing(problem):
    current = initial_state(problem)
    loop:
        neighbour = highest_valued_successor(current)
        if value(neighbour) <= value(current):
            return current      # local maximum reached
        current = neighbour
```

## Comparison with Other Searches

| Property | Hill Climbing | BFS | A\* |
|----------|--------------|-----|-----|
| Memory | O(1) | O(b^d) | O(b^d) |
| Complete | No | Yes | Yes |
| Optimal | No | Yes (unit cost) | Yes |
| Good for | Large state spaces | Small spaces | Informed problems |