from gurobipy import Model, GRB, Var, quicksum
from src.const.general import PROBLEM_NAMES
from src.classes.Problem import Problem

class PartitionProblem(Problem):
    """
    Optimization problem: Partition a set of numbers into two subsets with nearly equal sums.
    
    Args:
        input_size (int): Number of elements in the input set.
    """
    def __init__(self, input_size: int):
        self.input = []
        self.input_size = input_size
        self.input_mean = 0
        
        self.initialize()
        
    def __call__(self, input):
        """
        Returns the optimized variables described in build_variables.

        Args:
            input (int[input_size]): List of numerical values to be partitioned.

        Returns:
            Var[]: Variables representing the selection of items for the first subset.
        """
        self.input = input
        self.input_mean = sum(input) * 0.5
        
        self.build_criterion()
        self.build_constraints()
        
        self.model.optimize()
        
        return self.model.getVars()
    
    def initialize(self):
        self.model = Model(PROBLEM_NAMES["partition_problem"])
        self.build_variables()
    
    def build_variables(self):
        """
        Variables:
        - partitions GRB.BINARY[input_size]: 1 if item i is in the first subset, 0 otherwise.
        """
        self.partitions = self.model.addMVar(self.input_size, vtype=GRB.BINARY)
        
    def build_criterion(self):
        """
        Criterion: Minimize the difference between the target mean and the subset sum.
        """
        self.model.setObjective(
            self.input_mean - quicksum(
                                self.input[i] * self.partitions[i] 
                                for i in range(self.input_size)
                            ),
            GRB.MINIMIZE
        )
        
    def build_constraints(self):
        """
        Constraints:
        - The sum of the chosen subset must not exceed the target mean (half of total sum).
        """
        self.model.addConstr(
            self.input_mean - quicksum(
                                self.input[i] * self.partitions[i] 
                                for i in range(self.input_size)
                            ) >= 0
        )