from gurobipy import Model, GRB, Var, quicksum

from src.const.general import PROBLEM_NAMES

class PartitionProblem:
    def __init__(self, input_size: int):
        self.input = []
        self.input_size = input_size
        self.input_mean = 0
        
        self.initialize()
        
    def __call__(self, input):
        self.input = input
        self.input_mean = sum(input) * 0.5
        
        self.build_criterion()
        self.build_constrains()
        
        self.model.optimize()
        
        return self.model.getVars()
    
    def initialize(self):
        self.model = Model(PROBLEM_NAMES["partition_problem"])
        self.build_variables()
    
    def build_variables(self):
        self.partitions = self.model.addMVar(self.input_size, vtype=GRB.BINARY)
        
    def build_criterion(self):
        self.model.setObjective(
            self.input_mean - quicksum(
                                self.input[i]*self.partitions[i] 
                                for i in range(self.input_size)
                            )
        )
        
    def build_constrains(self):
        self.model.addConstr(
            self.input_mean - quicksum(
                                self.input[i]*self.partitions[i] 
                                for i in range(self.input_size)
                            ) >= 0
        )