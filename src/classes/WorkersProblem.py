from gurobipy import Model, GRB, quicksum

from src.const.general import PROBLEM_NAMES
from src.classes.Problem import Problem


class WorkersProblem(Problem):
    """
    Optimization Problem: Maximize the number of allocated tasks.
    """
    def __init__(self, workers_size, jobs_size):
        """
        Args:
            workers_size (int): _description_
            jobs_size (int): _description_
        """
        self.workers_size = workers_size
        self.job_size = jobs_size

        self.initialize()

    def __call__(self, jobs, budget):
        """
        Calculate the tasks allocations for each worker.

        Args:
            jobs (list[int]): Costs of each job.
            budget (int): Genral budget for all the tasks.

        Returns:
            Var[]: Allocations of tasks for each worker as
            GRB.BINARY[workers_size, job_size].
        """
        self.jobs = jobs
        self.budget = budget

        self.build_criterion()
        self.build_constraints()

        self.model.optimize()

        return self.model.getVars()

    def initialize(self):
        self.model = Model(PROBLEM_NAMES["workers_problem"])
        self.build_variables()

    def build_variables(self):
        """
        Variables:
        - job_allocations: GRB.BINARY[workers_size, job_size] -
        allocations of tasks for each worker.
        """
        self.job_allocations = self.model.addMVar(
            (self.workers_size, self.job_size),
            vtype=GRB.BINARY
        )

    def build_constraints(self):
        """
        Constraints:
        - Accumulated allocated task costs should not exceed budget.
        - Each worker can work only on up to 1 task.
        """

        self.model.addConstr(
            quicksum(self.job_allocations[i, j] * self.jobs[i]
                     for i in range(self.workers_size)
                     for j in range(self.job_size)) <= self.budget
        )

        for j in range(self.job_size):
            self.model.addConstr(
                self.job_allocations[:, j].sum() <= 1
            )

        for i in range(self.workers_size):
            self.model.addConstr(
                self.job_allocations[i, :].sum() <= 1
            )

    def build_criterion(self):
        """
        Criterion: Maximize the number of tasks allocated, between workers.
        """
        self.model.setObjective(
            quicksum(self.job_allocations[i, j]
                     for i in range(self.workers_size)
                     for j in range(self.job_size)),
            GRB.MAXIMIZE
        )
