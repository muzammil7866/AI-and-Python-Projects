# Greedy Best-First Search And A* — Romania Map

## Overview

Implements two heuristically informed search algorithms to find a path between cities on the classic **Romania road map** from Russell & Norvig's AIMA. The goal city is **Bucharest**. Cities, distances, and heuristic values are loaded from external text files.

## Concepts Covered

- Heuristic functions (straight-line distance to Bucharest)
- Greedy Best-First Search (GBFS) — minimises `h(n)`
- A\* Search — minimises `f(n) = g(n) + h(n)`
- Priority queue (min-heap) for the open list
- Admissibility and optimality of A\*
- Route visualisation with matplotlib

## Files

| File | Description |
|------|-------------|
| `Greedy BFS And A Star.ipynb` | Jupyter notebook with visualisation output |
| `cities.txt` | City names with x/y coordinates |
| `citiesGraph.txt` | Road connections with distances |
| `heuristics.txt` | Straight-line distance of each city to Bucharest |

## How to Run

```bash
jupyter notebook "Greedy BFS And A Star.ipynb"
```

## Algorithm Comparison

| Property | GBFS | A\* |
|----------|------|-----|
| Evaluation fn | `h(n)` | `g(n) + h(n)` |
| Complete | No (may loop) | Yes |
| Optimal | No | Yes (admissible h) |
| Time | O(b^m) | O(b^d) |

## Data File Formats

**cities.txt** — `CityName x_coord y_coord`  
**citiesGraph.txt** — `City1 City2 distance`  
**heuristics.txt** — `CityName h_value`

## Visualisation

Running either algorithm produces a matplotlib map where:
- **Green path** = Greedy Best-First Search route
- **Blue path** = A\* route
- **Red dots** = all cities