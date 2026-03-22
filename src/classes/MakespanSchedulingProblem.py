from gurobipy import Model, GRB, quicksum

from src.const.general import PROBLEM_NAMES
from src.classes.Problem import Problem


class MakespanSchedulingProblem(Problem):
    """
    Optimization problem: Allocation of tasks to processes in order
    to minimize makespan.

    Args:
        tasks_size (int): Number of tasks to assign.
        processes_size (int): Number of processes that can execute tasks.
    """
    def __init__(self, tasks_size: int, processes_size: int):
        self.tasks = []
        self.tasks_size = tasks_size
        self.processes_size = processes_size

        self.initialize()

    def __call__(self, tasks):
        """
        Returns the optimized variables described in build_variables.

        Args:
            tasks (int[tasks_size]): Processing time (duration) of each task.

        Returns:
            Var[]: Variables list representing the assignment of tasks
            to processes and the resulting makespan.
        """
        self.tasks = tasks

        self.build_criterion()
        self.build_constraints()

        self.model.optimize()

        return self.model.getVars()

    def initialize(self):
        self.model = Model(PROBLEM_NAMES["makespan_scheduling"])
        self.build_variables()

    def build_variables(self):
        """
        Variables:
        - allocations GRB.BINARY[tasks_size, processes_size]:
            Matrix representing assignment of tasks to processes
            (1 if task i is assigned to process j, 0 otherwise).
        - c GRB.CONTINUOUS: Variable representing the makespan
            (maximum load across all processes).
        """
        self.allocations = self.model.addMVar(
            (self.tasks_size, self.processes_size),
            vtype=GRB.BINARY,
        )
        self.c = self.model.addVar(lb=0, vtype=GRB.CONTINUOUS)

    def build_criterion(self):
        """
        Criterion: Minimize the makespan (maximum total processing time
        assigned to any process).
        """
        self.model.setObjective(self.c, GRB.MINIMIZE)

    def build_constraints(self):
        """
        Constraints:
        - Each task must be assigned to exactly one process.
        - The total processing time assigned to each process must not
          exceed makespan c.
        """
        for i in range(self.tasks_size):
            self.model.addConstr(
                quicksum(self.allocations[i, j]
                         for j in range(self.processes_size)) == 1
            )

        for j in range(self.processes_size):
            self.model.addConstr(
                quicksum(
                    self.tasks[i] * self.allocations[i, j]
                    for i in range(self.tasks_size)
                ) <= self.c
            )
