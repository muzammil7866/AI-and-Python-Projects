# A* And Greedy BFS — Autonomous Delivery Robot

## Overview

An autonomous delivery robot navigates a **15×15 city grid** (buildings, houses, road vehicles) to complete 5 sequential deliveries. Each completed delivery becomes the new robot start position, simulating a real-world progressive delivery route.

Two informed search algorithms are implemented and compared:
- **Greedy Best-First Search (GBFS)** — fast but not guaranteed optimal
- **A\* Search** — optimal path cost, guaranteed by admissible Euclidean heuristic

## File

| File | Description |
|------|-------------|
| `A Star And Greedy BFS Path Planning.py` | Full simulation: grid, graph, GBFS, A\*, 5-delivery run, visualisation |

## How to Run

```bash
pip install numpy matplotlib
python "A Star And Greedy BFS Path Planning.py"
```

## Environment Design

| Element | Representation |
|---------|---------------|
| City area | 15×15 grid (225 cells) |
| Buildings/Houses | Fixed 3×3 obstacle blocks at 5 locations |
| Vehicles on roads | 18 random obstacle cells, repositioned between deliveries |
| Passable cells | Cost 0 (EMPTY) |
| Obstacle cells | Cost ∞ (BLOCK) |
| Edge weights | Random integer in \[1, 20\] — recalculated each delivery |

## Algorithm Details

### Greedy Best-First Search
```
f(n) = h(n) = Euclidean(n, goal)
```
- Prioritises cells closest to the goal
- Fast, uses a small frontier
- **Not optimal** — may find a longer total-cost path

### A* Search
```
f(n) = g(n) + h(n)
g(n) = actual cost from start to n (sum of edge weights 1–20)
h(n) = Euclidean distance to goal (admissible → never overestimates)
```
- Expands nodes in order of minimum estimated total cost
- **Optimal** — always finds the minimum-cost path
- Uses MRV tie-breaking on equal f-values

## Dynamic Environment Handling

Between each delivery:
1. Vehicle obstacles are randomly repositioned (new `vehicle_seed`)
2. The graph is fully rebuilt with new random edge costs
3. The previous delivery point becomes the new robot start

## Simulation Flow

```
Robot waits at depot (0,0)
   ↓
Assign Delivery 1 → run GBFS + A* → compare → robot follows A* path
   ↓
Previous goal becomes new start
   ↓
Assign Delivery 2 … (repeat 5 times)
   ↓
Report total A* cost
```

## Performance Comparison

| Property | Greedy Best-First | A\* Search |
|----------|------------------|------------|
| Evaluation fn | h(n) | g(n) + h(n) |
| Optimal | No | Yes |
| Complete | Yes (finite graph) | Yes |
| Nodes expanded | Fewer (greedy) | More (thorough) |
| Best use case | Speed priority | Cost optimality |

## Output

- Console comparison table per delivery (steps, nodes expanded, time, cost)
- matplotlib visualisation: side-by-side GBFS vs A\* grid for each delivery
- Aggregate comparison over 50 random instances

## Dependencies

```
numpy, matplotlib
```