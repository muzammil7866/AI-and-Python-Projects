"""
Lab 11: First Order Logic — Backward Chaining
Topics: Goal-directed backward chaining, Prolog-style query resolution
"""


# ── Unification (shared utility) ──────────────────────────────────────────────

def is_var(x):
    return isinstance(x, str) and x[0].islower()


def subst(theta, x):
    if is_var(x) and x in theta:
        return subst(theta, theta[x])
    if isinstance(x, list):
        return [subst(theta, xi) for xi in x]
    return x


def unify(x, y, theta=None):
    """Returns MGU dict or None."""
    if theta is None:
        theta = {}
    x, y = subst(theta, x), subst(theta, y)
    if x == y:
        return theta
    if is_var(x):
        theta2 = dict(theta); theta2[x] = y; return theta2
    if is_var(y):
        theta2 = dict(theta); theta2[y] = x; return theta2
    if isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            return None
        for xi, yi in zip(x, y):
            theta = unify(xi, yi, theta)
            if theta is None:
                return None
        return theta
    return None


# ── Backward-Chaining Prover ──────────────────────────────────────────────────

class PrologKB:
    """
    Simple Prolog-style KB with backward chaining.
    Facts and rules are stored as Horn clauses.
    """

    def __init__(self):
        self._clauses = []   # list of (head, body)

    def fact(self, pred, *args):
        """Assert a ground fact: pred(arg1, arg2, ...)"""
        self._clauses.append(((pred, list(args)), []))

    def rule(self, head_pred, head_args, body):
        """
        Assert a rule.
        head_args: list of strings (lowercase = variable, Uppercase = constant)
        body: list of (pred, [args...])
        """
        self._clauses.append(((head_pred, list(head_args)), list(body)))

    def query(self, pred, *args):
        """Return a list of binding dicts that prove pred(args)."""
        return list(self._solve([(pred, list(args))], {}))

    def _solve(self, goals, theta):
        if not goals:
            yield dict(theta)
            return
        goal_pred, goal_args = goals[0]
        rest = goals[1:]
        for (h_pred, h_args), body in self._clauses:
            if h_pred != goal_pred or len(h_args) != len(goal_args):
                continue
            # Rename variables to avoid clashes
            renamed_head, renamed_body = self._rename(h_args, body)
            theta2 = unify(
                [subst(theta, a) for a in goal_args],
                renamed_head,
                dict(theta),
            )
            if theta2 is not None:
                new_goals = renamed_body + rest
                yield from self._solve(new_goals, theta2)

    _counter = [0]

    def _rename(self, head_args, body):
        """Alpha-rename all variables in a clause to fresh names."""
        self._counter[0] += 1
        n = self._counter[0]
        mapping = {}

        def rename_term(t):
            if is_var(t):
                if t not in mapping:
                    mapping[t] = f"{t}_{n}"
                return mapping[t]
            if isinstance(t, list):
                return [rename_term(x) for x in t]
            return t

        new_head = [rename_term(a) for a in head_args]
        new_body = [(p, [rename_term(a) for a in args]) for p, args in body]
        return new_head, new_body


# ── Helper ────────────────────────────────────────────────────────────────────

def yes_no(kb, pred, *args):
    results = kb.query(pred, *args)
    return "YES" if results else "NO"


# ── Demo 1: Genealogy ─────────────────────────────────────────────────────────

def demo_genealogy():
    print("=" * 55)
    print("DEMO 1: Backward Chaining — Genealogy")
    print("=" * 55)

    kb = PrologKB()

    # Facts
    for p, c in [("Tom","Bob"),("Tom","Liz"),("Bob","Ann"),("Bob","Pat")]:
        kb.fact("parent", p, c)
    for m in ["Tom", "Bob"]:
        kb.fact("male", m)
    for f in ["Liz", "Ann", "Pat"]:
        kb.fact("female", f)

    # Rules
    kb.rule("grandparent", ["x","z"],
            [("parent",["x","y"]), ("parent",["y","z"])])

    kb.rule("ancestor", ["x","z"], [("parent",["x","z"])])
    kb.rule("ancestor", ["x","z"],
            [("parent",["x","y"]), ("ancestor",["y","z"])])

    kb.rule("sibling", ["x","y"],
            [("parent",["z","x"]), ("parent",["z","y"])])

    kb.rule("uncle", ["x","z"],
            [("sibling",["x","y"]), ("parent",["y","z"])])

    queries = [
        ("grandparent", "Tom", "Ann"),
        ("grandparent", "Tom", "Liz"),
        ("ancestor",    "Tom", "Pat"),
        ("ancestor",    "Bob", "Liz"),
        ("sibling",     "Ann", "Pat"),
        ("uncle",       "Tom", "Ann"),
    ]

    for pred, *args in queries:
        print(f"  {pred}({', '.join(args)})? => {yes_no(kb, pred, *args)}")


# ── Demo 2: Knowledge-Based System — Disease Diagnosis ───────────────────────

def demo_diagnosis():
    print("\n" + "=" * 55)
    print("DEMO 2: Backward Chaining — Simple Diagnosis")
    print("=" * 55)

    kb = PrologKB()

    # Observed symptoms for a patient
    for symptom in ["fever", "cough", "sore_throat", "runny_nose"]:
        kb.fact("has_symptom", "patient1", symptom)

    # Rules: disease diagnosis
    kb.rule("has_cold", ["x"], [
        ("has_symptom", ["x", "runny_nose"]),
        ("has_symptom", ["x", "sore_throat"]),
    ])
    kb.rule("has_flu", ["x"], [
        ("has_symptom", ["x", "fever"]),
        ("has_symptom", ["x", "cough"]),
        ("has_symptom", ["x", "sore_throat"]),
    ])
    kb.rule("needs_rest", ["x"], [("has_flu",  ["x"])])
    kb.rule("needs_rest", ["x"], [("has_cold", ["x"])])

    queries = [
        ("has_cold",    "patient1"),
        ("has_flu",     "patient1"),
        ("needs_rest",  "patient1"),
        ("has_flu",     "patient2"),
    ]

    for pred, *args in queries:
        print(f"  {pred}({', '.join(args)})? => {yes_no(kb, pred, *args)}")


# ── Demo 3: Type Hierarchy ────────────────────────────────────────────────────

def demo_type_hierarchy():
    print("\n" + "=" * 55)
    print("DEMO 3: Backward Chaining — Type Hierarchy (subtype)")
    print("=" * 55)

    kb = PrologKB()

    # isa hierarchy
    for sub, sup in [("Dog","Mammal"), ("Cat","Mammal"),
                     ("Mammal","Animal"), ("Bird","Animal"),
                     ("Penguin","Bird")]:
        kb.fact("isa", sub, sup)

    # Instances
    for inst, typ in [("Rex","Dog"), ("Tweety","Bird"), ("Pingu","Penguin")]:
        kb.fact("instance_of", inst, typ)

    # Rules
    kb.rule("subtype_of", ["x","z"], [("isa",["x","z"])])
    kb.rule("subtype_of", ["x","z"],
            [("isa",["x","y"]), ("subtype_of",["y","z"])])

    kb.rule("is_a", ["x","z"],
            [("instance_of",["x","y"]), ("subtype_of",["y","z"])])
    kb.rule("is_a", ["x","z"], [("instance_of",["x","z"])])

    queries = [
        ("subtype_of", "Dog",    "Animal"),
        ("subtype_of", "Penguin","Animal"),
        ("is_a",       "Rex",    "Animal"),
        ("is_a",       "Tweety", "Mammal"),
        ("is_a",       "Pingu",  "Animal"),
    ]

    for pred, *args in queries:
        print(f"  {pred}({', '.join(args)})? => {yes_no(kb, pred, *args)}")


if __name__ == "__main__":
    demo_genealogy()
    demo_diagnosis()
    demo_type_hierarchy()
