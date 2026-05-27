# Propositional Logic — Resolution And Truth Tables

## Overview

Covers the fundamentals of **Propositional Logic** as a knowledge representation language. Implements truth table generation, model checking, and resolution-based theorem proving — the foundations of logic-based AI agents.

## Concepts Covered

- Propositional symbols, connectives (AND, OR, NOT, IMPLIES, IFF)
- Truth tables and model enumeration
- Validity, satisfiability, and entailment
- Model checking (truth-table method)
- Conjunctive Normal Form (CNF)
- Resolution theorem proving (refutation)

## Files

| File | Description |
|------|-------------|
| `Resolution Theorem Proving.py` | Python implementation: truth tables, model checking, resolution KB |
| `Report.docx` | Problem statement and report |

## How to Run

```bash
python "Resolution Theorem Proving.py"
```

## Demos Included

| Demo | Description |
|------|-------------|
| Truth Tables | Generates truth tables for AND, OR, IMPLIES, De Morgan's law |
| Model Checking | Verifies Modus Ponens (`P→Q`, `P` ⊢ `Q`) |
| Resolution | Proves entailment using PL-Resolution (refutation) |
| Wumpus World | Applies propositional inference to a toy AI scenario |

## Key Concepts

**Entailment:** KB ⊨ α means every model satisfying KB also satisfies α.

**Resolution rule:**  
`(P ∨ Q)` and `(¬P ∨ R)` resolves to `(Q ∨ R)`

**Refutation proof:** To prove α, add `¬α` to KB and derive the empty clause (contradiction).