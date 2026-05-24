"""Hill-climbing and simulated annealing experiments for the 8-queens problem."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Callable, Sequence


Board = list[int]


def calculate_conflicts(board: Sequence[int]) -> int:
    """Return the number of attacking queen pairs on the board."""
    conflicts = 0
    for row_index in range(len(board)):
        for next_index in range(row_index + 1, len(board)):
            same_row = board[row_index] == board[next_index]
            same_diagonal = abs(board[row_index] - board[next_index]) == abs(row_index - next_index)
            if same_row or same_diagonal:
                conflicts += 1
    return conflicts


def generate_successor(board: Sequence[int]) -> Board:
    """Move one queen to a random row in its current column."""
    if not board:
        raise ValueError("Board cannot be empty.")

    successor = list(board)
    column = random.randrange(len(board))
    successor[column] = random.randrange(len(board))
    return successor


def hill_climbing(board: Sequence[int], max_steps: int = 500) -> Board:
    """Classic hill climbing using the best of several random neighbors."""
    current = list(board)
    current_conflicts = calculate_conflicts(current)

    for _ in range(max_steps):
        neighbors = [generate_successor(current) for _ in range(len(current))]
        best_neighbor = min(neighbors, key=calculate_conflicts)
        best_conflicts = calculate_conflicts(best_neighbor)
        if best_conflicts >= current_conflicts:
            return current
        current = best_neighbor
        current_conflicts = best_conflicts

    return current


def stochastic_hill_climbing(board: Sequence[int], max_steps: int = 500) -> Board:
    """Accept any improving neighbor and stop when progress stalls."""
    current = list(board)
    current_conflicts = calculate_conflicts(current)

    for _ in range(max_steps):
        neighbor = generate_successor(current)
        neighbor_conflicts = calculate_conflicts(neighbor)
        if neighbor_conflicts < current_conflicts:
            current = neighbor
            current_conflicts = neighbor_conflicts
        else:
            return current

    return current


def simulated_annealing(
    board: Sequence[int],
    temperature_schedule: Callable[[int], float],
    max_steps: int = 1000,
) -> Board:
    """Simulated annealing with a caller-provided temperature schedule."""
    current = list(board)
    current_conflicts = calculate_conflicts(current)

    for step in range(1, max_steps + 1):
        temperature = temperature_schedule(step)
        if temperature <= 0:
            break

        neighbor = generate_successor(current)
        neighbor_conflicts = calculate_conflicts(neighbor)
        delta = current_conflicts - neighbor_conflicts
        if delta > 0 or random.random() < math.exp(delta / temperature):
            current = neighbor
            current_conflicts = neighbor_conflicts

    return current


def exponential_decay(initial_temperature: float, decay_constant: float, step: int) -> float:
    return initial_temperature * math.exp(-decay_constant * step)


@dataclass(frozen=True)
class ExperimentResult:
    seed: int
    hill_climbing_conflicts: int
    stochastic_conflicts: int
    simulated_annealing_conflicts: int


def run_experiments(seed_count: int = 10, board_size: int = 8) -> list[ExperimentResult]:
    """Run all three search strategies against random initial boards."""
    results: list[ExperimentResult] = []

    for _ in range(seed_count):
        seed = random.randint(0, 10_000)
        random.seed(seed)
        initial_board = [random.randrange(board_size) for _ in range(board_size)]

        hill_board = hill_climbing(initial_board)
        stochastic_board = stochastic_hill_climbing(initial_board)
        annealed_board = simulated_annealing(
            initial_board,
            lambda step: exponential_decay(100.0, 0.01, step),
        )

        results.append(
            ExperimentResult(
                seed=seed,
                hill_climbing_conflicts=calculate_conflicts(hill_board),
                stochastic_conflicts=calculate_conflicts(stochastic_board),
                simulated_annealing_conflicts=calculate_conflicts(annealed_board),
            )
        )

    return results


def print_results(results: Sequence[ExperimentResult]) -> None:
    print("Seed\tHC Conflicts\tSHC Conflicts\tSA Conflicts")
    print("-" * 52)
    for result in results:
        print(
            f"{result.seed}\t{result.hill_climbing_conflicts}\t\t"
            f"{result.stochastic_conflicts}\t\t{result.simulated_annealing_conflicts}"
        )


def main() -> None:
    print_results(run_experiments())


if __name__ == "__main__":
    main()