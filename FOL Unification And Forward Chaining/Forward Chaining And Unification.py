"""
Lab 10: First Order Logic
Topics: Unification, forward chaining, knowledge base with rules and facts
"""


# ── Unification ───────────────────────────────────────────────────────────────

def is_var(x):
    """Lowercase strings are treated as FOL variables."""
    return isinstance(x, str) and x[0].islower()


def subst(theta, x):
    """Apply substitution theta to term x."""
    if is_var(x):
        return subst(theta, theta[x]) if x in theta else x
    if isinstance(x, (list, tuple)):
        return type(x)(subst(theta, xi) for xi in x)
    return x


def unify(x, y, theta=None):
    """
    Unification algorithm (Robinson, 1965).
    Returns the most general unifier (dict) or None on failure.
    """
    if theta is None:
        theta = {}
    x, y = subst(theta, x), subst(theta, y)
    if x == y:
        return theta
    if is_var(x):
        return _unify_var(x, y, theta)
    if is_var(y):
        return _unify_var(y, x, theta)
    if isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)):
        if len(x) != len(y):
            return None
        for xi, yi in zip(x, y):
            theta = unify(xi, yi, theta)
            if theta is None:
                return None
        return theta
    return None


def _unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    theta = dict(theta)
    theta[var] = x
    return theta


# ── Forward Chaining KB ───────────────────────────────────────────────────────

class FOLKnowledgeBase:
    """
    FOL KB supporting ground facts and universally quantified Horn-clause rules.
    Uses data-driven forward chaining (like Rete, simplified).
    """

    def __init__(self):
        self.facts = []    # list of (predicate, [args...])
        self.rules = []    # list of (body_list, head_tuple)

    def tell(self, predicate, *args):
        fact = (predicate, list(args))
        if fact not in self.facts:
            self.facts.append(fact)

    def add_rule(self, body, head):
        """
        body: list of (predicate, [args...])  — conditions (lowercase = variable)
        head: (predicate, [args...])           — conclusion
        """
        self.rules.append((body, head))

    def _match_body(self, body, facts, theta):
        if not body:
            yield theta
            return
        pred, args = body[0]
        for fp, fa in facts:
            if fp == pred:
                theta2 = unify(args, fa, dict(theta))
                if theta2 is not None:
                    args_sub = [subst(theta2, a) for a in args]
                    if args_sub == fa:
                        yield from self._match_body(body[1:], facts, theta2)

    def forward_chain(self):
        """Saturate the KB by applying all rules until nothing new is derived."""
        changed = True
        while changed:
            changed = False
            for body, (h_pred, h_args) in self.rules:
                for theta in self._match_body(body, list(self.facts), {}):
                    new_args = [subst(theta, a) for a in h_args]
                    new_fact = (h_pred, new_args)
                    if new_fact not in self.facts:
                        self.facts.append(new_fact)
                        changed = True

    def ask(self, predicate, *args):
        return (predicate, list(args)) in self.facts

    def display(self, filter_pred=None):
        for pred, args in self.facts:
            if filter_pred is None or pred == filter_pred:
                print(f"  {pred}({', '.join(str(a) for a in args)})")


# ── Demo 1: Unification ───────────────────────────────────────────────────────

def demo_unification():
    print("=" * 55)
    print("DEMO 1: Unification")
    print("=" * 55)

    tests = [
        # (x, y, expected outcome description)
        (["Knows", "John", "x"], ["Knows", "John", "Jane"],  "x/Jane"),
        (["Knows", "x", "y"],   ["Knows", "John", "Jane"],   "x/John, y/Jane"),
        (["Knows", "x", "x"],   ["Knows", "John", "John"],   "x/John"),
        (["Knows", "x", "x"],   ["Knows", "John", "Jane"],   "FAIL (x cannot be both)"),
        (["f", "x", "g", "y"],  ["f", "a", "g", "b"],        "x/a, y/b"),
    ]

    for x, y, desc in tests:
        mgu = unify(x, y)
        print(f"  unify({x}, {y})")
        print(f"  Expected: {desc}")
        print(f"  MGU:      {mgu}\n")


# ── Demo 2: Family Relationships ──────────────────────────────────────────────

def demo_family():
    print("=" * 55)
    print("DEMO 2: Forward Chaining — Family Relationships")
    print("=" * 55)

    kb = FOLKnowledgeBase()

    # Ground facts
    for parent, child in [("Tom","Bob"),("Tom","Liz"),("Bob","Ann"),("Bob","Pat")]:
        kb.tell("Parent", parent, child)
    for m in ["Tom", "Bob"]:
        kb.tell("Male", m)
    for f in ["Liz", "Ann", "Pat"]:
        kb.tell("Female", f)

    # Rules (lowercase = variable)
    # GrandParent(x, z) :- Parent(x, y), Parent(y, z)
    kb.add_rule(
        [("Parent", ["x", "y"]), ("Parent", ["y", "z"])],
        ("GrandParent", ["x", "z"])
    )
    # Father(x, y) :- Parent(x, y), Male(x)
    kb.add_rule(
        [("Parent", ["x", "y"]), ("Male", ["x"])],
        ("Father", ["x", "y"])
    )
    # Mother(x, y) :- Parent(x, y), Female(x)
    kb.add_rule(
        [("Parent", ["x", "y"]), ("Female", ["x"])],
        ("Mother", ["x", "y"])
    )

    kb.forward_chain()

    print("Derived GrandParent facts:")
    kb.display("GrandParent")
    print("Derived Father facts:")
    kb.display("Father")
    print("Derived Mother facts:")
    kb.display("Mother")

    print(f"\nQuery: Is Tom a GrandParent of Ann? {kb.ask('GrandParent', 'Tom', 'Ann')}")
    print(f"Query: Is Bob a Father of Pat?       {kb.ask('Father', 'Bob', 'Pat')}")
    print(f"Query: Is Tom a Mother of Liz?       {kb.ask('Mother', 'Tom', 'Liz')}")


# ── Demo 3: Animal Classification ────────────────────────────────────────────

def demo_animals():
    print("\n" + "=" * 55)
    print("DEMO 3: Forward Chaining — Animal Classification")
    print("=" * 55)

    kb = FOLKnowledgeBase()

    # Observed properties of "Tweety"
    for prop in ["HasFeathers", "CanFly", "LaysEggs"]:
        kb.tell(prop, "Tweety")

    # Observed properties of "Rex"
    for prop in ["HasHair", "GivesMilk", "HasSharpTeeth", "HasClaws", "HasForwardEyes"]:
        kb.tell(prop, "Rex")

    # Rules
    kb.add_rule([("HasFeathers", ["x"])], ("Bird", ["x"]))
    kb.add_rule([("CanFly", ["x"]), ("LaysEggs", ["x"])], ("Bird", ["x"]))
    kb.add_rule([("HasHair", ["x"])], ("Mammal", ["x"]))
    kb.add_rule([("GivesMilk", ["x"])], ("Mammal", ["x"]))
    kb.add_rule(
        [("Mammal", ["x"]), ("HasSharpTeeth", ["x"]),
         ("HasClaws", ["x"]), ("HasForwardEyes", ["x"])],
        ("Carnivore", ["x"])
    )

    kb.forward_chain()

    print(f"Is Tweety a Bird?      {kb.ask('Bird', 'Tweety')}")
    print(f"Is Rex a Mammal?       {kb.ask('Mammal', 'Rex')}")
    print(f"Is Rex a Carnivore?    {kb.ask('Carnivore', 'Rex')}")
    print(f"Is Tweety a Carnivore? {kb.ask('Carnivore', 'Tweety')}")


if __name__ == "__main__":
    demo_unification()
    demo_family()
    demo_animals()
