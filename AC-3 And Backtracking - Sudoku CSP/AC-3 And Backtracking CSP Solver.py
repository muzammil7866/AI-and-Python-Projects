"""
Sudoku CSP Solver
Implements AC-3 (Arc Consistency 3) and Backtracking Search to solve Sudoku puzzles.
Tkinter GUI with difficulty selector, puzzle selector, algorithm selector, and timer.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import copy


# ── Puzzle Dataset ─────────────────────────────────────────────────────────────
# 0 = empty cell.  Format: 9×9 list of lists.

PUZZLES = {
    "Easy": [
        # Easy #1
        [[5,3,0,0,7,0,0,0,0],
         [6,0,0,1,9,5,0,0,0],
         [0,9,8,0,0,0,0,6,0],
         [8,0,0,0,6,0,0,0,3],
         [4,0,0,8,0,3,0,0,1],
         [7,0,0,0,2,0,0,0,6],
         [0,6,0,0,0,0,2,8,0],
         [0,0,0,4,1,9,0,0,5],
         [0,0,0,0,8,0,0,7,9]],
        # Easy #2
        [[0,0,3,0,2,0,6,0,0],
         [9,0,0,3,0,5,0,0,1],
         [0,0,1,8,0,6,4,0,0],
         [0,0,8,1,0,2,9,0,0],
         [7,0,0,0,0,0,0,0,8],
         [0,0,6,7,0,8,2,0,0],
         [0,0,2,6,0,9,5,0,0],
         [8,0,0,2,0,3,0,0,9],
         [0,0,5,0,1,0,3,0,0]],
        # Easy #3
        [[1,0,0,4,8,9,0,0,6],
         [7,3,0,0,0,0,0,4,0],
         [0,0,0,0,0,1,2,9,5],
         [0,0,7,1,2,0,6,0,0],
         [5,0,0,7,0,3,0,0,8],
         [0,0,6,0,9,5,7,0,0],
         [9,1,4,6,0,0,0,0,0],
         [0,2,0,0,0,0,0,3,7],
         [8,0,0,5,1,2,0,0,4]],
        # Easy #4
        [[0,2,0,6,0,8,0,0,0],
         [5,8,0,0,0,9,7,0,0],
         [0,0,0,0,4,0,0,0,0],
         [3,7,0,0,0,0,5,0,0],
         [6,0,0,0,0,0,0,0,4],
         [0,0,8,0,0,0,0,1,3],
         [0,0,0,0,2,0,0,0,0],
         [0,0,9,8,0,0,0,3,6],
         [0,0,0,3,0,6,0,9,0]],
    ],
    "Medium": [
        # Medium #1
        [[0,0,0,2,6,0,7,0,1],
         [6,8,0,0,7,0,0,9,0],
         [1,9,0,0,0,4,5,0,0],
         [8,2,0,1,0,0,0,4,0],
         [0,0,4,6,0,2,9,0,0],
         [0,5,0,0,0,3,0,2,8],
         [0,0,9,3,0,0,0,7,4],
         [0,4,0,0,5,0,0,3,6],
         [7,0,3,0,1,8,0,0,0]],
        # Medium #2
        [[0,0,0,6,0,0,4,0,0],
         [7,0,0,0,0,3,6,0,0],
         [0,0,0,0,9,1,0,8,0],
         [0,0,0,0,0,0,0,0,0],
         [0,5,0,1,8,0,0,0,3],
         [0,0,0,3,0,6,0,4,5],
         [0,4,0,2,0,0,0,6,0],
         [9,0,3,0,0,0,0,0,0],
         [0,2,0,0,0,0,1,0,0]],
        # Medium #3
        [[2,0,0,0,0,0,0,0,0],
         [0,0,0,6,0,0,0,0,3],
         [0,7,4,0,8,0,0,0,0],
         [0,0,0,0,0,3,0,0,2],
         [0,8,0,0,4,0,0,1,0],
         [6,0,0,5,0,0,0,0,0],
         [0,0,0,0,1,0,7,8,0],
         [5,0,0,0,0,9,0,0,0],
         [0,0,0,0,0,0,0,4,0]],
        # Medium #4
        [[0,0,5,3,0,0,0,0,0],
         [8,0,0,0,0,0,0,2,0],
         [0,7,0,0,1,0,5,0,0],
         [4,0,0,0,0,5,3,0,0],
         [0,1,0,0,7,0,0,0,6],
         [0,0,3,2,0,0,0,8,0],
         [0,6,0,5,0,0,0,0,9],
         [0,0,4,0,0,0,0,3,0],
         [0,0,0,0,0,9,7,0,0]],
    ],
    "Hard": [
        # Hard #1
        [[8,0,0,0,0,0,0,0,0],
         [0,0,3,6,0,0,0,0,0],
         [0,7,0,0,9,0,2,0,0],
         [0,5,0,0,0,7,0,0,0],
         [0,0,0,0,4,5,7,0,0],
         [0,0,0,1,0,0,0,3,0],
         [0,0,1,0,0,0,0,6,8],
         [0,0,8,5,0,0,0,1,0],
         [0,9,0,0,0,0,4,0,0]],
        # Hard #2
        [[0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,3,0,8,5],
         [0,0,1,0,2,0,0,0,0],
         [0,0,0,5,0,7,0,0,0],
         [0,0,4,0,0,0,1,0,0],
         [0,9,0,0,0,0,0,0,0],
         [5,0,0,0,0,0,0,7,3],
         [0,0,2,0,1,0,0,0,0],
         [0,0,0,0,4,0,0,0,9]],
        # Hard #3
        [[0,0,0,0,0,0,0,1,2],
         [0,0,0,0,3,5,0,0,0],
         [0,0,0,6,0,0,0,7,0],
         [7,0,0,0,0,0,3,0,0],
         [0,0,0,4,0,0,8,0,0],
         [1,0,0,0,0,0,0,0,0],
         [0,0,0,1,2,0,0,0,0],
         [0,8,0,0,0,0,0,4,0],
         [0,5,0,0,0,0,6,0,0]],
        # Hard #4
        [[1,0,0,0,0,7,0,9,0],
         [0,3,0,0,2,0,0,0,8],
         [0,0,9,6,0,0,5,0,0],
         [0,0,5,3,0,0,9,0,0],
         [0,1,0,0,8,0,0,0,2],
         [6,0,0,0,0,4,0,0,0],
         [3,0,0,0,0,0,0,1,0],
         [0,4,0,0,0,0,0,0,7],
         [0,0,7,0,0,0,3,0,0]],
    ],
}


# ── CSP Representation ────────────────────────────────────────────────────────

def grid_to_csp(grid):
    """
    Returns:
        variables : list of (row, col) for all empty cells
        domains   : dict (r,c) -> set of possible values
        neighbors : dict (r,c) -> set of peer cells (same row/col/box)
    """
    domains   = {}
    neighbors = {}

    for r in range(9):
        for c in range(9):
            val = grid[r][c]
            domains[(r, c)] = {val} if val != 0 else set(range(1, 10))

    for r in range(9):
        for c in range(9):
            peers = set()
            for cc in range(9):      # same row
                if cc != c: peers.add((r, cc))
            for rr in range(9):      # same column
                if rr != r: peers.add((rr, c))
            br, bc = (r // 3) * 3, (c // 3) * 3   # same 3×3 box
            for dr in range(3):
                for dc in range(3):
                    rr, cc = br + dr, bc + dc
                    if (rr, cc) != (r, c): peers.add((rr, cc))
            neighbors[(r, c)] = peers

    variables = [(r, c) for r in range(9) for c in range(9) if grid[r][c] == 0]
    return variables, domains, neighbors


# ── AC-3 ─────────────────────────────────────────────────────────────────────

def revise(domains, xi, xj):
    """Remove values from domains[xi] with no support in domains[xj]."""
    revised = False
    for x in set(domains[xi]):
        # For Sudoku: constraint is xi ≠ xj.
        # x has no support if every y in domains[xj] equals x.
        if all(x == y for y in domains[xj]):
            domains[xi].discard(x)
            revised = True
    return revised


def ac3(domains, neighbors):
    """
    AC-3 algorithm.
    Returns True if arc-consistent (no domain wiped out), False otherwise.
    Modifies domains in place.
    """
    queue = {(xi, xj) for xi in domains for xj in neighbors[xi]}
    queue = list(queue)

    while queue:
        xi, xj = queue.pop()
        if revise(domains, xi, xj):
            if not domains[xi]:
                return False          # domain wipe-out → inconsistency
            for xk in neighbors[xi] - {xj}:
                queue.append((xk, xi))
    return True


def solve_ac3_only(grid):
    """
    Attempt to solve purely with AC-3 constraint propagation.
    Works well on easy puzzles; may not fully solve harder ones.
    Returns solved grid (or partially solved) and whether fully solved.
    """
    _, domains, neighbors = grid_to_csp(grid)
    t0 = time.perf_counter()

    success = ac3(domains, neighbors)
    elapsed = (time.perf_counter() - t0) * 1000

    result = [row[:] for row in grid]
    for (r, c), vals in domains.items():
        if len(vals) == 1:
            result[r][c] = next(iter(vals))

    fully_solved = all(result[r][c] != 0 for r in range(9) for c in range(9))
    return result, fully_solved, elapsed


# ── Backtracking ──────────────────────────────────────────────────────────────

_bt_nodes = [0]   # mutable counter for tracking nodes expanded


def select_mrv(variables, domains):
    """Minimum Remaining Values heuristic: pick variable with smallest domain."""
    return min(variables, key=lambda v: len(domains[v]))


def backtrack(assignment, variables, domains, neighbors):
    """
    Backtracking search with AC-3 inference (MAC — Maintaining Arc Consistency).
    assignment: dict (r,c) -> value for already assigned cells.
    """
    _bt_nodes[0] += 1

    unassigned = [v for v in variables if v not in assignment]
    if not unassigned:
        return assignment

    var = select_mrv(unassigned, domains)

    for value in sorted(domains[var]):
        # Check consistency with current assignment
        if all(assignment.get(nb) != value for nb in neighbors[var]):
            assignment[var] = value

            # Save domains and try AC-3 (forward checking with propagation)
            saved  = {v: set(d) for v, d in domains.items()}
            domains[var] = {value}

            if ac3(domains, neighbors):
                result = backtrack(assignment, variables, domains, neighbors)
                if result is not None:
                    return result

            # Restore domains on failure
            for v in domains:
                domains[v] = saved[v]
            del assignment[var]

    return None


def solve_backtracking(grid):
    """
    Solve using Backtracking + AC-3 inference (MAC).
    Always finds a solution if one exists.
    """
    variables, domains, neighbors = grid_to_csp(grid)
    _bt_nodes[0] = 0
    t0 = time.perf_counter()

    # Pre-fill assignment with given cells
    assignment = {(r, c): grid[r][c]
                  for r in range(9) for c in range(9) if grid[r][c] != 0}

    result_assignment = backtrack(assignment, variables, domains, neighbors)
    elapsed = (time.perf_counter() - t0) * 1000

    if result_assignment is None:
        return None, False, elapsed, _bt_nodes[0]

    result = [[0] * 9 for _ in range(9)]
    for (r, c), v in result_assignment.items():
        result[r][c] = v

    return result, True, elapsed, _bt_nodes[0]


# ── Tkinter GUI ───────────────────────────────────────────────────────────────

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku CSP Solver")
        self.root.resizable(False, False)

        self.cells  = {}          # (r,c) -> tk.Entry
        self.puzzle_grid = None   # current puzzle (list of lists)

        self._build_ui()
        self._load_puzzle()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Controls (top bar) ──────────────────────────────────────────────
        ctrl = tk.Frame(self.root, bg="#2C3E50", pady=6)
        ctrl.pack(fill="x")

        tk.Label(ctrl, text="Difficulty:", bg="#2C3E50", fg="white",
                 font=("Helvetica", 10)).pack(side="left", padx=(10, 2))
        self.diff_var = tk.StringVar(value="Easy")
        diff_cb = ttk.Combobox(ctrl, textvariable=self.diff_var,
                               values=["Easy", "Medium", "Hard"],
                               width=8, state="readonly")
        diff_cb.pack(side="left", padx=2)
        diff_cb.bind("<<ComboboxSelected>>", lambda _: self._load_puzzle())

        tk.Label(ctrl, text="Puzzle #:", bg="#2C3E50", fg="white",
                 font=("Helvetica", 10)).pack(side="left", padx=(10, 2))
        self.puzzle_var = tk.StringVar(value="1")
        puz_cb = ttk.Combobox(ctrl, textvariable=self.puzzle_var,
                               values=["1", "2", "3", "4"],
                               width=4, state="readonly")
        puz_cb.pack(side="left", padx=2)
        puz_cb.bind("<<ComboboxSelected>>", lambda _: self._load_puzzle())

        tk.Label(ctrl, text="Algorithm:", bg="#2C3E50", fg="white",
                 font=("Helvetica", 10)).pack(side="left", padx=(10, 2))
        self.algo_var = tk.StringVar(value="A* Backtracking")
        algo_cb = ttk.Combobox(ctrl, textvariable=self.algo_var,
                                values=["AC-3 Only", "A* Backtracking", "Compare Both"],
                                width=16, state="readonly")
        algo_cb.pack(side="left", padx=2)

        tk.Button(ctrl, text="Solve", bg="#27AE60", fg="white",
                  font=("Helvetica", 10, "bold"),
                  relief="flat", padx=10,
                  command=self._solve).pack(side="left", padx=(15, 2))

        tk.Button(ctrl, text="Reset", bg="#E74C3C", fg="white",
                  font=("Helvetica", 10, "bold"),
                  relief="flat", padx=10,
                  command=self._load_puzzle).pack(side="left", padx=2)

        # ── Grid ────────────────────────────────────────────────────────────
        board_frame = tk.Frame(self.root, bg="#2C3E50", padx=12, pady=12)
        board_frame.pack()

        for r in range(9):
            for c in range(9):
                pad_top    = 4 if r in (3, 6) else 1
                pad_left   = 4 if c in (3, 6) else 1
                pad_bottom = 1
                pad_right  = 1

                e = tk.Entry(board_frame, width=2, font=("Helvetica", 18, "bold"),
                             justify="center", relief="solid", bd=1,
                             bg="#FDFEFE", fg="#2C3E50")
                e.grid(row=r, column=c,
                       padx=(pad_left, pad_right),
                       pady=(pad_top, pad_bottom),
                       ipady=4)
                self.cells[(r, c)] = e

        # ── Status bar ──────────────────────────────────────────────────────
        self.status = tk.StringVar(value="Select a puzzle and press Solve.")
        tk.Label(self.root, textvariable=self.status,
                 font=("Helvetica", 10), bg="#ECF0F1", pady=6
                 ).pack(fill="x")

    # ── Load / Reset ──────────────────────────────────────────────────────────

    def _load_puzzle(self):
        diff  = self.diff_var.get()
        idx   = int(self.puzzle_var.get()) - 1
        grid  = PUZZLES[diff][idx]
        self.puzzle_grid = copy.deepcopy(grid)

        for r in range(9):
            for c in range(9):
                e = self.cells[(r, c)]
                e.config(state="normal", bg="#FDFEFE", fg="#2C3E50")
                e.delete(0, "end")
                if grid[r][c] != 0:
                    e.insert(0, str(grid[r][c]))
                    e.config(state="disabled", bg="#D5D8DC", fg="#1A252F",
                             disabledforeground="#1A252F")

        self.status.set(f"Loaded: {diff} Puzzle #{idx + 1} — press Solve.")

    # ── Solve ────────────────────────────────────────────────────────────────

    def _solve(self):
        if self.puzzle_grid is None:
            return
        algo = self.algo_var.get()

        if algo == "AC-3 Only":
            sol, ok, ms = solve_ac3_only(self.puzzle_grid)[:3]
            nodes_info = ""
            if ok:
                self._display(sol, "#D5F5E3")
                self.status.set(f"AC-3 Only — solved in {ms:.2f} ms")
            else:
                self._display(sol, "#FDEBD0")
                self.status.set(
                    f"AC-3 Only — partially reduced in {ms:.2f} ms  "
                    f"(use Backtracking for full solution)")

        elif algo == "A* Backtracking":
            sol, ok, ms, nodes = solve_backtracking(self.puzzle_grid)
            if ok:
                self._display(sol, "#D5F5E3")
                self.status.set(
                    f"Backtracking+AC-3 — solved in {ms:.2f} ms  |  "
                    f"nodes expanded: {nodes}")
            else:
                self.status.set("No solution found — puzzle may be invalid.")

        elif algo == "Compare Both":
            ac3_sol, ac3_ok, ac3_ms = solve_ac3_only(self.puzzle_grid)[:3]
            bt_sol,  bt_ok,  bt_ms, bt_nodes = solve_backtracking(self.puzzle_grid)

            sol = bt_sol if bt_ok else ac3_sol
            self._display(sol, "#D5F5E3" if bt_ok else "#FDEBD0")

            msg = (f"AC-3: {ac3_ms:.2f} ms ({'solved' if ac3_ok else 'partial'})  |  "
                   f"Backtracking: {bt_ms:.2f} ms, {bt_nodes} nodes  |  "
                   f"Winner: {'AC-3' if (ac3_ok and ac3_ms < bt_ms) else 'Backtracking'}")
            self.status.set(msg)

    # ── Display ───────────────────────────────────────────────────────────────

    def _display(self, grid, solved_bg):
        orig = self.puzzle_grid
        for r in range(9):
            for c in range(9):
                e = self.cells[(r, c)]
                if orig[r][c] == 0 and grid and grid[r][c] != 0:
                    e.config(state="normal")
                    e.delete(0, "end")
                    e.insert(0, str(grid[r][c]))
                    e.config(bg=solved_bg, fg="#1A5276")


# ── CLI fallback (no display) ─────────────────────────────────────────────────

def cli_demo():
    print("=" * 55)
    print("  SUDOKU CSP SOLVER — CLI Demo")
    print("=" * 55)

    for diff in ["Easy", "Medium", "Hard"]:
        for i, puzzle in enumerate(PUZZLES[diff]):
            ac3_sol, ac3_ok, ac3_ms  = solve_ac3_only(puzzle)[:3]
            bt_sol,  bt_ok,  bt_ms, nodes = solve_backtracking(puzzle)

            status_ac3 = "SOLVED" if ac3_ok else "partial"
            status_bt  = "SOLVED" if bt_ok  else "FAILED"

            print(f"\n  {diff} Puzzle #{i+1}")
            print(f"    AC-3 only  : {status_ac3:8s} | {ac3_ms:.3f} ms")
            print(f"    Backtrack  : {status_bt:8s} | {bt_ms:.3f} ms | {nodes} nodes")


if __name__ == "__main__":
    import sys
    if "--cli" in sys.argv:
        cli_demo()
    else:
        root = tk.Tk()
        app = SudokuGUI(root)
        root.mainloop()