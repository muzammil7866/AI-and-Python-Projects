"""
Autonomous Delivery Robot
15x15 grid city simulation with Greedy Best-First Search and A* path planning.
The robot makes 5 sequential deliveries; each completed delivery becomes the new start.
"""

import heapq
import random
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap

# ── Constants ─────────────────────────────────────────────────────────────────
GRID   = 15
EMPTY  = 0
BLOCK  = 1   # building / house
ROAD   = 0   # roads are EMPTY
N_DELIVERIES = 5

random.seed(42)
np.random.seed(42)


# ── Environment ───────────────────────────────────────────────────────────────

def build_city(vehicle_seed=0):
    """
    Create a 15×15 grid with fixed building blocks and random vehicles on roads.
    Returns grid (list of lists) with 0 = passable, 1 = obstacle.
    """
    grid = [[0] * GRID for _ in range(GRID)]

    # Fixed buildings (3×3 clusters at fixed positions)
    for (br, bc) in [(2,2), (2,11), (7,6), (11,2), (11,11)]:
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                r, c = br + dr, bc + dc
                if 1 <= r < GRID - 1 and 1 <= c < GRID - 1:
                    grid[r][c] = 1

    # Dynamic vehicles — change position each delivery (dynamic environment)
    random.seed(vehicle_seed)
    passable = [(r, c) for r in range(GRID) for c in range(GRID)
                if grid[r][c] == 0 and r not in (0, GRID - 1) and c not in (0, GRID - 1)]
    for pos in random.sample(passable, min(18, len(passable))):
        grid[pos[0]][pos[1]] = 1

    return grid


def build_graph(grid):
    """
    Build a weighted graph from the grid.
    Edge cost is a random integer in [1, 20] (re-generated each call to simulate
    changing road conditions).
    """
    graph = {}
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(GRID):
        for c in range(GRID):
            if grid[r][c] == 1:
                continue
            neighbors = []
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < GRID and 0 <= nc < GRID and grid[nr][nc] == 0:
                    cost = random.randint(1, 20)
                    neighbors.append(((nr, nc), cost))
            graph[(r, c)] = neighbors
    return graph


def euclidean(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


# ── Algorithms ────────────────────────────────────────────────────────────────

def gbfs(graph, start, goal):
    """
    Greedy Best-First Search.
    Uses only h(n) = Euclidean distance to goal.
    Complete on finite graphs; NOT guaranteed optimal.
    """
    t0 = time.perf_counter()
    heap = [(euclidean(start, goal), start)]
    came_from = {start: None}
    visited = set()
    expanded = 0

    while heap:
        _, cur = heapq.heappop(heap)
        if cur in visited:
            continue
        visited.add(cur)
        expanded += 1
        if cur == goal:
            break
        for nb, _ in graph.get(cur, []):
            if nb not in visited and nb not in came_from:
                came_from[nb] = cur
                heapq.heappush(heap, (euclidean(nb, goal), nb))

    elapsed = (time.perf_counter() - t0) * 1000
    path = _trace(came_from, start, goal)
    return path, expanded, elapsed


def astar(graph, start, goal):
    """
    A* Search.
    Uses f(n) = g(n) + h(n); h = Euclidean distance.
    Admissible heuristic → guaranteed optimal path cost.
    """
    t0 = time.perf_counter()
    heap = [(euclidean(start, goal), 0.0, start)]
    came_from = {start: None}
    g = {start: 0.0}
    visited = set()
    expanded = 0

    while heap:
        _, gn, cur = heapq.heappop(heap)
        if cur in visited:
            continue
        visited.add(cur)
        expanded += 1
        if cur == goal:
            break
        for nb, cost in graph.get(cur, []):
            ng = g[cur] + cost
            if nb not in g or ng < g[nb]:
                g[nb] = ng
                came_from[nb] = cur
                heapq.heappush(heap, (ng + euclidean(nb, goal), ng, nb))

    elapsed = (time.perf_counter() - t0) * 1000
    path = _trace(came_from, start, goal)
    cost = g.get(goal, float("inf"))
    return path, expanded, elapsed, cost


def _trace(came_from, start, goal):
    if goal not in came_from:
        return None
    path, node = [], goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path if path[0] == start else None


# ── Visualisation ─────────────────────────────────────────────────────────────

_CMAP = ListedColormap(["#F5F5F5", "#2C3E50", "#F39C12", "#3498DB", "#E74C3C", "#95A5A6"])
# 0=empty  1=obstacle  2=path  3=robot  4=current-goal  5=future-goal

def _grid_display(grid, path, robot, goals, current_idx):
    d = np.array(grid, dtype=float)
    if path:
        for r, c in path[1:-1]:
            d[r][c] = 2
    for i, (r, c) in enumerate(goals):
        d[r][c] = 4 if i == current_idx else 5
    d[robot[0]][robot[1]] = 3
    return d


def visualise(grid, gbfs_path, astar_path, robot, goals, delivery_idx):
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    title = (f"Delivery {delivery_idx + 1} / {N_DELIVERIES}: "
             f"{robot} → {goals[delivery_idx]}")
    fig.suptitle(title, fontsize=13, fontweight="bold")

    for ax, path, algo in zip(axes, [gbfs_path, astar_path],
                               ["Greedy Best-First Search", "A* Search"]):
        d = _grid_display(grid, path, robot, goals, delivery_idx)
        ax.imshow(d, cmap=_CMAP, vmin=0, vmax=5, interpolation="nearest")
        steps = len(path) - 1 if path else "—"
        ax.set_title(f"{algo}\nSteps: {steps}", fontsize=11)
        ax.set_xticks(np.arange(-0.5, GRID, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, GRID, 1), minor=True)
        ax.grid(which="minor", color="#AAAAAA", linewidth=0.3)
        ax.tick_params(which="both", bottom=False, left=False,
                       labelbottom=False, labelleft=False)

        # Labels on cells
        ax.text(robot[1], robot[0], "R", ha="center", va="center",
                fontsize=8, color="white", fontweight="bold")
        gr, gc = goals[delivery_idx]
        ax.text(gc, gr, str(delivery_idx + 1), ha="center", va="center",
                fontsize=8, color="white", fontweight="bold")
        for i, (r, c) in enumerate(goals):
            if i != delivery_idx:
                ax.text(c, r, str(i + 1), ha="center", va="center",
                        fontsize=7, color="white")

    legend = [
        mpatches.Patch(facecolor="#F5F5F5", edgecolor="gray", label="Empty road"),
        mpatches.Patch(facecolor="#2C3E50", label="Obstacle"),
        mpatches.Patch(facecolor="#F39C12", label="Path taken"),
        mpatches.Patch(facecolor="#3498DB", label="Robot (start)"),
        mpatches.Patch(facecolor="#E74C3C", label="Current delivery"),
        mpatches.Patch(facecolor="#95A5A6", label="Future delivery"),
    ]
    fig.legend(handles=legend, loc="lower center", ncol=6,
               fontsize=9, bbox_to_anchor=(0.5, -0.01))
    plt.tight_layout()
    plt.show()


def print_comparison(n, start, goal, g_res, a_res):
    g_path, g_exp, g_ms         = g_res
    a_path, a_exp, a_ms, a_cost = a_res

    print(f"\n  Delivery {n}:  {start} → {goal}")
    print(f"  {'Algorithm':<24} {'Steps':>6}  {'Nodes exp.':>10}  {'Time (ms)':>10}  {'Path cost':>10}")
    print(f"  {'─'*64}")
    gs = len(g_path) - 1 if g_path else "N/A"
    as_ = len(a_path) - 1 if a_path else "N/A"
    print(f"  {'Greedy Best-First':<24} {str(gs):>6}  {g_exp:>10}  {g_ms:>10.3f}  {'N/A (not opt)':>10}")
    print(f"  {'A* Search':<24} {str(as_):>6}  {a_exp:>10}  {a_ms:>10.3f}  {a_cost:>10.1f}")

    if g_path and a_path:
        if len(a_path) < len(g_path):
            print(f"  ✓ A* is shorter by {len(g_path) - len(a_path)} step(s) — optimal guarantee holds.")
        elif len(a_path) == len(g_path):
            print(f"  Both paths have equal length. A* cost ({a_cost:.1f}) is still optimal.")
        else:
            print(f"  GBFS found fewer steps but A* route has lower total cost ({a_cost:.1f}).")


# ── Simulation ────────────────────────────────────────────────────────────────

def random_free_cell(grid, exclude):
    free = [(r, c) for r in range(GRID) for c in range(GRID)
            if grid[r][c] == 0 and (r, c) not in exclude]
    return random.choice(free)


def simulate():
    print("=" * 65)
    print("         AUTONOMOUS DELIVERY ROBOT — SIMULATION")
    print("=" * 65)

    # Robot waits at the depot (top-left corner)
    robot_start = (0, 0)

    # Build base grid (buildings don't move)
    base_grid = build_city(vehicle_seed=0)
    base_grid[0][0] = 0  # always keep start clear

    # Generate 5 random delivery locations
    taken = {robot_start}
    delivery_points = []
    for _ in range(N_DELIVERIES):
        pt = random_free_cell(base_grid, taken)
        delivery_points.append(pt)
        taken.add(pt)

    print(f"\n  Robot depot   : {robot_start}")
    print(f"  Deliveries    : {delivery_points}")
    print(f"  Grid size     : {GRID} × {GRID}")

    current_pos = robot_start
    total_astar_cost = 0.0

    for i, goal in enumerate(delivery_points):
        # Dynamic environment: vehicles reposition between deliveries
        grid  = build_city(vehicle_seed=i + 1)
        grid[current_pos[0]][current_pos[1]] = 0
        grid[goal[0]][goal[1]] = 0

        graph = build_graph(grid)

        g_path, g_exp, g_ms         = gbfs(graph, current_pos, goal)
        a_path, a_exp, a_ms, a_cost = astar(graph, current_pos, goal)

        print_comparison(i + 1, current_pos, goal,
                         (g_path, g_exp, g_ms),
                         (a_path, a_exp, a_ms, a_cost))

        visualise(grid, g_path, a_path, current_pos, delivery_points, i)

        if a_path:
            total_astar_cost += a_cost
            print(f"  → Robot reached {goal}. Next start: {goal}")
        else:
            print(f"  ⚠ No path found! Goal unreachable from {current_pos}.")

        current_pos = goal   # previous delivery = new start

    print(f"\n{'='*65}")
    print(f"  ALL {N_DELIVERIES} DELIVERIES COMPLETE")
    print(f"  Total A* path cost across all deliveries : {total_astar_cost:.1f}")
    print(f"{'='*65}")


# ── Algorithm Comparison Summary ──────────────────────────────────────────────

def algorithm_comparison_summary():
    """
    Run both algorithms on 50 random problems and print aggregate statistics.
    """
    print("\n" + "=" * 65)
    print("  ALGORITHM COMPARISON — 50 RANDOM INSTANCES")
    print("=" * 65)

    gbfs_steps_list, astar_steps_list = [], []
    gbfs_ms_list,    astar_ms_list    = [], []
    gbfs_nodes_list, astar_nodes_list = [], []
    a_better, g_better, tie = 0, 0, 0

    grid  = build_city(0)
    graph = build_graph(grid)
    free  = [k for k in graph if grid[k[0]][k[1]] == 0]

    for _ in range(50):
        s, g = random.sample(free, 2)
        gp, gn, gm        = gbfs(graph, s, g)
        ap, an, am, _     = astar(graph, s, g)
        if gp and ap:
            gbfs_steps_list.append(len(gp) - 1)
            astar_steps_list.append(len(ap) - 1)
            gbfs_ms_list.append(gm)
            astar_ms_list.append(am)
            gbfs_nodes_list.append(gn)
            astar_nodes_list.append(an)
            if len(ap) < len(gp): a_better += 1
            elif len(gp) < len(ap): g_better += 1
            else: tie += 1

    print(f"\n  {'Metric':<28} {'GBFS':>10}  {'A*':>10}")
    print(f"  {'─'*52}")
    print(f"  {'Avg steps':<28} {np.mean(gbfs_steps_list):>10.1f}  {np.mean(astar_steps_list):>10.1f}")
    print(f"  {'Avg nodes expanded':<28} {np.mean(gbfs_nodes_list):>10.1f}  {np.mean(astar_nodes_list):>10.1f}")
    print(f"  {'Avg time (ms)':<28} {np.mean(gbfs_ms_list):>10.3f}  {np.mean(astar_ms_list):>10.3f}")
    print(f"\n  A* found shorter/equal path : {a_better + tie} / 50")
    print(f"  GBFS found shorter path     : {g_better} / 50")
    print(f"\n  Conclusion: A* is optimal (lower cost path) but explores more")
    print(f"  nodes. GBFS is faster but may miss the optimal route.")


if __name__ == "__main__":
    simulate()
    algorithm_comparison_summary()