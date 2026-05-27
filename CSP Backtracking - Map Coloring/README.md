# Backtracking — Map Coloring CSP

## Overview

**Map Coloring** is a classic Constraint Satisfaction Problem (CSP): assign colors to regions of a map such that no two adjacent regions share the same color. Formulated and solved using CSP techniques including **backtracking search** and constraint propagation.

## Concepts Covered

- CSP formulation (variables, domains, constraints)
- Backtracking search for CSPs
- Constraint propagation (arc consistency / forward checking)
- Minimum Remaining Values (MRV) heuristic
- The 4-Color Theorem

## Files

| File | Description |
|------|-------------|
| `Backtracking CSP Map Coloring.ipynb` | Full CSP implementation |
| `Report.docx` | Problem statement and report |

## How to Run

```bash
jupyter notebook "Backtracking CSP Map Coloring.ipynb"
```

## CSP Formulation

- **Variables:** Regions of the map (e.g., WA, NT, SA, Q, NSW, V, T for Australia)
- **Domains:** {Red, Green, Blue} (3 colors are sufficient for most planar maps)
- **Constraints:** Adjacent regions must have different colors

## Algorithm — Backtracking

```
function backtrack(assignment, csp):
    if assignment is complete: return assignment
    var = select_unassigned_variable(csp)
    for value in order_domain_values(var, csp):
        if value consistent with assignment:
            assign(var, value)
            result = backtrack(assignment, csp)
            if result != failure: return result
            remove(var, value) from assignment
    return failure
```

## Example (Australia Map)

```
WA=Red, NT=Green, SA=Blue, Q=Red, NSW=Green, V=Red, T=Green
```