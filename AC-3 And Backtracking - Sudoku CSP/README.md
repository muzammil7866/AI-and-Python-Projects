# AC-3 And Backtracking — Sudoku CSP Solver

## Overview

Solves Sudoku puzzles by formulating them as a **Constraint Satisfaction Problem (CSP)** and applying two algorithms:
- **AC-3** (Arc Consistency 3) — pure constraint propagation
- **Backtracking Search** with AC-3 as inference (MAC — Maintaining Arc Consistency)

A **Tkinter GUI** allows selecting difficulty, puzzle, and algorithm, then shows the solution with timing information.

## File

| File | Description |
|------|-------------|
| `AC-3 And Backtracking CSP Solver.py` | AC-3, Backtracking, Tkinter GUI, embedded 12-puzzle dataset |

## How to Run

```bash
# GUI mode (default)
python "AC-3 And Backtracking CSP Solver.py"

# CLI demo mode (no display needed)
python "AC-3 And Backtracking CSP Solver.py" --cli
```

## CSP Formulation

| CSP Component | Sudoku Mapping |
|---------------|---------------|
| Variables X | Each of 81 cells (row, col) |
| Domain D | {1, 2, 3, 4, 5, 6, 7, 8, 9} per empty cell |
| Constraints C | No two cells in the same row, column, or 3×3 box share a value |

Filled cells have a singleton domain `{given_value}`.

## Algorithm 1 — AC-3

```
function AC-3(csp):
    queue ← all arcs (Xi, Xj) in csp
    while queue not empty:
        (Xi, Xj) ← pop(queue)
        if REVISE(Xi, Xj):
            if |Di| == 0: return false   ← domain wipe-out
            for Xk in neighbors(Xi) - {Xj}:
                add (Xk, Xi) to queue
    return true

function REVISE(Xi, Xj):
    for each x in Di:
        if no y in Dj satisfies Xi ≠ Xj:
            remove x from Di
```

- AC-3 alone solves **Easy** and most **Medium** puzzles
- **Hard** puzzles require backtracking — AC-3 alone returns a partially reduced board

## Algorithm 2 — Backtracking + AC-3 (MAC)

```
function BACKTRACK(assignment, csp):
    if complete: return assignment
    var ← SELECT-UNASSIGNED (MRV heuristic)
    for value in domain(var):
        if consistent with assignment:
            assign var = value
            run AC-3 as inference
            if AC-3 succeeds:
                result ← BACKTRACK(assignment, csp)
                if result ≠ failure: return result
            undo assignment and inference
    return failure
```

- MRV (Minimum Remaining Values) selects the most constrained variable first
- AC-3 after each assignment prunes domains early → far fewer backtracks
- Always finds a solution if one exists

## GUI Features

| Control | Options |
|---------|---------|
| Difficulty | Easy / Medium / Hard |
| Puzzle # | 1 / 2 / 3 / 4 |
| Algorithm | AC-3 Only / A\* Backtracking / Compare Both |
| Buttons | Solve, Reset |
| Status bar | Algorithm used, solve time (ms), nodes expanded |

## Dataset (Embedded)

12 puzzles across 3 difficulty levels (4 per level):

| Level | Given cells | Solving method |
|-------|-------------|----------------|
| Easy | 36–45 | AC-3 alone usually sufficient |
| Medium | 27–35 | AC-3 + some backtracking |
| Hard | < 27 | Full backtracking required |

## Performance Comparison

| Property | AC-3 Only | Backtracking + AC-3 |
|----------|-----------|---------------------|
| Completeness | No (may not fully solve) | Yes — always solves |
| Time (Easy) | < 1 ms | < 5 ms |
| Time (Hard) | < 1 ms (partial) | 10–500 ms |
| Nodes expanded | 0 (propagation only) | Tracked and displayed |

## Dependencies

```
tkinter (built-in Python standard library)
```