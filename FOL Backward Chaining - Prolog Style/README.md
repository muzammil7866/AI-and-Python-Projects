# FOL — Backward Chaining (Prolog Style)

## Overview

Implements **Backward Chaining** for First Order Logic — a goal-directed inference strategy inspired by Prolog. Starting from a query, the engine works backwards through rules to find supporting facts, yielding all variable bindings (substitutions) that prove the goal.

## Concepts Covered

- Goal-directed (top-down) reasoning vs. forward chaining
- Prolog-style resolution
- Variable renaming (alpha-renaming) to avoid name clashes
- Recursive rule application
- Generating all proofs via a generator (yield-based search)

## Files

| File | Description |
|------|-------------|
| `Backward Chaining Prolog Style.py` | Prolog-style backward chaining engine |
| `Report.docx` | Problem statement and report |

## How to Run

```bash
python "Backward Chaining Prolog Style.py"
```

## Demos Included

| Demo | Description |
|------|-------------|
| Genealogy | Proves `grandparent`, `ancestor`, `sibling`, `uncle` relationships |
| Disease Diagnosis | Goal-driven symptom → diagnosis reasoning |
| Type Hierarchy | `isA` / `subtype_of` hierarchy traversal |

## Backward Chaining vs. Forward Chaining

| Property | Forward Chaining | Backward Chaining |
|----------|-----------------|-------------------|
| Direction | Data → Conclusions | Goal → Supporting facts |
| Driven by | New facts | User query |
| Good for | Monitoring, alert systems | Query answering (Prolog) |
| Risk | Derives irrelevant facts | May loop on recursive rules |

## Example Query

```python
kb = PrologKB()
kb.fact("parent", "Tom", "Bob")
kb.rule("grandparent", ["x","z"],
        [("parent",["x","y"]), ("parent",["y","z"])])

results = kb.query("grandparent", "Tom", "Ann")
# → YES if Tom is grandparent of Ann
```