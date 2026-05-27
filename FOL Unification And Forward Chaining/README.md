# FOL — Unification And Forward Chaining

## Overview

Extends propositional logic to **First Order Logic (FOL)**, introducing variables, predicates, and quantifiers. Implements the **Unification** algorithm (the backbone of FOL inference) and a **Forward Chaining** knowledge base that derives new facts from rules.

## Concepts Covered

- FOL syntax: constants, variables, predicates, functions
- Substitution and the Most General Unifier (MGU)
- Robinson's Unification Algorithm
- Horn clauses and definite clauses
- Data-driven forward chaining (bottom-up reasoning)
- Knowledge base saturation

## Files

| File | Description |
|------|-------------|
| `Forward Chaining And Unification.py` | Unification + forward chaining KB implementation |
| `Report.docx` | Problem statement and report |

## How to Run

```bash
python "Forward Chaining And Unification.py"
```

## Demos Included

| Demo | Description |
|------|-------------|
| Unification | Tests MGU computation for various term pairs |
| Family Relationships | Derives `GrandParent`, `Father`, `Mother` from `Parent` facts |
| Animal Classification | Derives `Mammal`, `Bird`, `Carnivore` from observable properties |

## Unification Example

```
unify([Knows, John, x], [Knows, John, Jane])
→ MGU: {x: Jane}

unify([Knows, x, y], [Knows, John, Jane])
→ MGU: {x: John, y: Jane}
```

## Forward Chaining Rule Format

```python
# GrandParent(x, z) :- Parent(x, y) AND Parent(y, z)
kb.add_rule(
    body=[("Parent", ["x", "y"]), ("Parent", ["y", "z"])],
    head=("GrandParent", ["x", "z"])
)
```