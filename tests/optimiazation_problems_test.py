import logging
from unittest import TestCase, main
from gurobipy import GRB

from src.classes.PartitionProblem import PartitionProblem
from src.classes.MakespanSchedulingProblem import MakespanSchedulingProblem
from src.classes.KnapsackProblem import KnapsackProblem
from src.classes.DistancesProblem import DistancesProblem


class TestOptimizationProblems(TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.logger = logging.getLogger()
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s: %(message)s"
        )

    def test_partition_problem(self) -> None:
        """
        Test PartitionProblem to ensure the solution contains only binary
        values and matches the input size.
        """
        data = [3, 9, 4, 7, 6, 5, 11]
        problem = PartitionProblem(input_size=len(data))

        solution = problem(data)

        self.assertIsNotNone(solution)
        self.assertEqual(len(solution), len(data))

        values = [var.X for var in solution]
        for v in values:
            self.assertIn(v, [0, 1])

    def test_makespan_scheduling_problem(self) -> None:
        """
        Test MakespanSchedulingProblem to verify task allocations and that
        each task is assigned to exactly one process.
        """
        tasks = [3, 9, 4, 7]
        processes_size = 2
        problem = MakespanSchedulingProblem(
            tasks_size=len(tasks),
            processes_size=processes_size
        )

        solution = problem(tasks)

        self.assertIsNotNone(solution)
        allocations_vars = solution[:len(tasks) * processes_size]

        self.assertEqual(
            len(allocations_vars),
            len(tasks) * processes_size
        )

        values = [var.X for var in allocations_vars]
        for v in values:
            self.assertIn(v, [0, 1])

        for i in range(len(tasks)):
            row_sum = sum(
                values[i*processes_size + j] for j in range(processes_size)
            )
            self.assertEqual(row_sum, 1)

    def test_knapsack_problem_basic(self) -> None:
        """
        Test KnapsackProblem for basic binary constraints and solution length.
        """
        prices = [1, 2, 3, 4, 5]
        weights = [1, 2, 3, 4, 5]
        capacity = 7

        problem = KnapsackProblem(
            prices_size=len(prices),
            weights_size=len(weights)
        )
        solution = problem(prices, weights, capacity)

        self.assertIsNotNone(solution)
        self.assertEqual(len(solution), len(prices))

        values = [var.X for var in solution]
        for v in values:
            self.assertIn(v, [0, 1])

    def test_knapsack_solution_with_full_capacity(self) -> None:
        """
        Test KnapsackProblem to ensure weight capacity is respected and at
        least one item is chosen.
        """
        prices = [10, 20, 30]
        weights = [5, 5, 5]
        capacity = 10

        problem = KnapsackProblem(
            prices_size=len(prices),
            weights_size=len(weights)
        )
        solution = problem(prices, weights, capacity)

        values = [var.X for var in solution]
        total_weight = sum(w * x for w, x in zip(weights, values))

        self.assertLessEqual(total_weight, capacity)
        self.assertTrue(any(values))

    def test_distances_problem(self) -> None:
        """
        Test DistancesProblem for budget constraints, faculty counts, and
        proper distribution of points to faculties.
        """
        faculties_size = 5
        points_shape = (6, 2)
        budget = 10
        faculties_count = 3
        faculties_costs = [1, 2, 3, 4, 5]
        faculties_locations = [[2, 0], [0, 1], [1, 0], [0, 3], [0, 2]]
        points_locations = [[0, 0], [2, 2], [1, 1], [3, 0], [3, 3], [4, 4]]

        problem = DistancesProblem(
            faculties_size=faculties_size,
            points_shape=points_shape
        )

        problem(
            budget=budget,
            faculties_count=faculties_count,
            faculties_costs=faculties_costs,
            faculties_locations=faculties_locations,
            points_locations=points_locations
        )

        self.assertEqual(problem.model.Status, GRB.OPTIMAL)

        chosen_values = problem.choosen_faculties.X
        dist_values = problem.points_distribution.X

        self.assertAlmostEqual(sum(chosen_values), faculties_count)

        total_cost = sum(
            chosen_values[i] * faculties_costs[i]
            for i in range(faculties_size)
        )
        self.assertLessEqual(total_cost, budget)

        for i in range(points_shape[0]):
            self.assertAlmostEqual(sum(dist_values[i, :]), 1.0)

        for i in range(points_shape[0]):
            for j in range(faculties_size):
                if dist_values[i, j] > 0.5:
                    self.assertGreater(chosen_values[j], 0.5)

        self.assertGreater(problem.model.ObjVal, 0)


if __name__ == "__main__":
    main()
