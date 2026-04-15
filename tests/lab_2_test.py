from unittest import TestCase, main
import logging

from src.classes.WorkersProblem import WorkersProblem


class TestLabTwoTasks(TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.logger = logging.getLogger()
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s: %(message)s"
        )

    def test_workers_problem(self) -> None:
        """
        Test the workers problem, for whether the produced
        solution is being correct and the valid one.
        """

        workers = [1, 2, 3, 4, 5, 6]
        jobs = [10, 30, 12, 1, 3, 6, 4, 3]
        budget = 50

        problem = WorkersProblem(
            len(workers),
            len(jobs)
        )

        values = problem(jobs, budget)

        for v in values:
            self.assertIn(v.X, [0, 1])

        allocations = problem.job_allocations.X

        for i in range(len(allocations)):
            self.assertLessEqual(sum(allocations[i, :]), 1.0)

        for j in range(len(allocations[0])):
            self.assertLessEqual(sum(allocations[:, j]), 1.0)


if __name__ == "__main__":
    main()
