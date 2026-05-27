"""
Lab 9: Propositional Logic
Topics: Truth tables, model checking, resolution theorem proving
"""

from itertools import product


# ── Truth Table ──────────────────────────────────────────────────────────────

def truth_table(variables, formula_fn, formula_label):
    header = " | ".join(f"  {v}  " for v in variables) + f" | {formula_label}"
    divider = "-" * len(header)
    print(f"\nTruth Table: {formula_label}")
    print(divider)
    print(header)
    print(divider)
    for values in product([True, False], repeat=len(variables)):
        result = formula_fn(*values)
        row = " | ".join(f"  {'T' if v else 'F'}  " for v in values)
        print(f"{row} |   {'T' if result else 'F'}")
    print()


# ── Knowledge Base (CNF Resolution) ──────────────────────────────────────────

class KnowledgeBase:
    """Propositional KB using CNF clauses and resolution."""

    def __init__(self):
        self.clauses = []

    def tell(self, *literals):
        """Add a disjunction of literals as a clause. Prefix negated literals with '~'."""
        self.clauses.append(frozenset(literals))

    def _resolve(self, ci, cj):
        resolvents = []
        for lit in ci:
            neg = lit[1:] if lit.startswith("~") else f"~{lit}"
            if neg in cj:
                new_clause = (ci - {lit}) | (cj - {neg})
                resolvents.append(frozenset(new_clause))
        return resolvents

    def ask(self, *negated_query_literals):
        """
        Return True if the KB entails the query using refutation resolution.
        Pass the *negated* form of what you want to prove.
        """
        clauses = list(self.clauses) + [frozenset(negated_query_literals)]
        seen = set(clauses)

        while True:
            new = set()
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    for resolvent in self._resolve(clauses[i], clauses[j]):
                        if not resolvent:           # empty clause → proven
                            return True
                        new.add(resolvent)
            new -= seen
            if not new:
                return False
            seen.update(new)
            clauses.extend(new)


# ── Demos ─────────────────────────────────────────────────────────────────────

def demo_truth_tables():
    print("=" * 55)
    print("DEMO 1: Truth Tables")
    print("=" * 55)

    truth_table(["P", "Q"], lambda p, q: p and q,        "P AND Q")
    truth_table(["P", "Q"], lambda p, q: p or q,         "P OR Q")
    truth_table(["P", "Q"], lambda p, q: (not p) or q,   "P IMPLIES Q")
    truth_table(["P"],      lambda p: not p,              "NOT P")

    # De Morgan's law: NOT(P AND Q) ≡ (NOT P) OR (NOT Q)
    truth_table(
        ["P", "Q"],
        lambda p, q: (not (p and q)) == ((not p) or (not q)),
        "NOT(P AND Q) == (NOT P) OR (NOT Q)",
    )


def demo_model_checking():
    print("=" * 55)
    print("DEMO 2: Model Checking — Modus Ponens")
    print("=" * 55)
    print("KB: P => Q  AND  P is True")
    print("Query: Must Q be True?\n")

    # All combinations; find models where KB is satisfied
    for p, q in product([True, False], repeat=2):
        kb_satisfied = ((not p) or q) and p   # (P=>Q) AND P
        print(f"  P={int(p)}, Q={int(q)}: KB satisfied={kb_satisfied}"
              + (" ← valid model" if kb_satisfied else ""))


def demo_resolution():
    print("\n" + "=" * 55)
    print("DEMO 3: Resolution Theorem Proving")
    print("=" * 55)

    kb = KnowledgeBase()
    kb.tell("A")               # A is true
    kb.tell("~A", "C")        # A => C  (¬A ∨ C)
    kb.tell("~C", "D")        # C => D  (¬C ∨ D)

    # Prove C: negate query → add {¬C} and check for contradiction
    print("KB: A,  A=>C,  C=>D")
    print(f"  Entails C? {kb.ask('~C')}")
    print(f"  Entails D? {kb.ask('~D')}")
    print(f"  Entails B? {kb.ask('~B')}")   # B is not in KB


def demo_wumpus():
    print("\n" + "=" * 55)
    print("DEMO 4: Wumpus World — Simple Inference")
    print("=" * 55)

    # Sentences from the Wumpus world:
    #   R1: ¬P11
    #   R2: B11 <=> (P12 OR P21)
    #   Observation: ¬B11 (no breeze at [1,1])
    print("Given: No breeze at [1,1]")
    print("Rule:  Breeze at [1,1] iff Pit at [1,2] OR Pit at [2,1]")

    B11 = False
    if not B11:
        P12 = False
        P21 = False
        print(f"Inference: Pit at [1,2]? {P12}  →  Safe to move!")
        print(f"Inference: Pit at [2,1]? {P21}  →  Safe to move!")


if __name__ == "__main__":
    demo_truth_tables()
    demo_model_checking()
    demo_resolution()
    demo_wumpus()
