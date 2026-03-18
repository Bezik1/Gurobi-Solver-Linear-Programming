from gurobipy import Model, GRB, Var, quicksum

from src.const.general import PROBLEM_NAMES

class  MakespanScheduling:
    def __init__(self, tasks_size: int, processes_size: int):
        self.tasks = []
        self.tasks_size = tasks_size
        self.processes_size = processes_size
        
        self.initialize()
        
    def __call__(self, tasks):
        self.tasks = tasks
        
        self.build_criterion()
        self.build_constrains()
        
        self.model.optimize()
        
        return self.model.getVars()
    
    def initialize(self):
        self.model = Model(PROBLEM_NAMES["makespan_scheduling"])
        self.build_variables()
    
    def build_variables(self):
        self.allocations = self.model.addMVar(
            (self.tasks_size, self.processes_size),
            vtype=GRB.BINARY,
        )
        self.c = self.model.addVar(lb=0, vtype=GRB.CONTINUOUS)
        
    def build_criterion(self):
        self.model.setObjective(self.c, GRB.MINIMIZE)
        
    def build_constrains(self):
        for i in range(self.tasks_size):
            self.model.addConstr(
                quicksum(self.allocations[i,j] for j in range(self.processes_size)) == 1)

        for j in range(self.processes_size):
            self.model.addConstr(
                quicksum(self.tasks[i]*self.allocations[i,j] for i in range(self.tasks_size)) <= self.c)