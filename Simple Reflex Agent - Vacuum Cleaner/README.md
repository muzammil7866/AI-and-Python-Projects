# Simple Reflex Agent — Vacuum Cleaner World

## Overview

Implements the classic **simple reflex agent** — the vacuum cleaner from Russell & Norvig's AIMA. The agent operates in a two-room environment, sensing dirt and deciding to clean or move accordingly.

## Concepts Covered

- Intelligent agent architecture (Sense → Decide → Actuate)
- Simple reflex agents (no memory / world model)
- Environment representation
- Percept-to-action mapping via a condition-action rule table

## Files

| File | Description |
|------|-------------|
| `Simple Reflex Agent Simulation.ipynb` | Full implementation with OOP design |
| `Report.docx` | Problem statement and report |

## How to Run

```bash
jupyter notebook "Simple Reflex Agent Simulation.ipynb"
```

## Agent Architecture

```
Environment (Room 1, Room 2)
        ↓ sense()
   VacuumCleaner
        ↓ decide()
   Action sequence
        ↓ actuate()
   Updated environment
```

## Classes

| Class | Responsibility |
|-------|---------------|
| `Room` | Holds the dirt state (`dirty` / `clean`) of a room |
| `VacuumCleaner` | Agent — implements `sense()`, `decide()`, `actuate()` |

## Possible Percept States

| Room 1 | Room 2 | Location | Action |
|--------|--------|----------|--------|
| Dirty | Dirty | 1 | Clean 1 → Move Right → Clean 2 |
| Dirty | Clean | 1 | Clean 1 |
| Clean | Dirty | 1 | Move Right → Clean 2 |
| Clean | Clean | * | Power Off |

## Sample Run

```
Initial state: Room 1 = DIRTY, Room 2 = DIRTY, Start = Room 1
CLEANED ROOM 1
MOVED TO RIGHT!
CLEANED ROOM 2
BOTH ROOMS ARE CLEAN SO VACUUM IS POWERING OFF!
```