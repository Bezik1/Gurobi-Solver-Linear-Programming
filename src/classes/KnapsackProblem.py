from gurobipy import Model, GRB, Var, quicksum

from src.const.general import PROBLEM_NAMES

class KnapsackProblem:
    def __init__(self, prices_size: int, weights_size: int):
        self.prices = []
        self.prices_size = prices_size
        
        self.weights = []
        self.weights_size = weights_size
        
        self.initialize()
        
    def __call__(self, prices, weights, capacity):
        self.prices = prices
        self.weights = weights
        self.capacity = capacity
        
        self.build_criterion()
        self.build_constrains()
        
        self.model.optimize()
        
        return self.model.getVars()
    
    def initialize(self):
        self.model = Model(PROBLEM_NAMES["knapsack_problem"])
        self.build_variables()
    
    def build_variables(self):
        self.choosen_items = self.model.addMVar(self.prices_size, vtype=GRB.BINARY)
        
    def build_criterion(self):
        self.model.setObjective(quicksum(
            self.choosen_items[i]*self.prices[i] for i in range(self.prices_size)
        ), GRB.MAXIMIZE)
        
    def build_constrains(self):
        self.model.addConstr(quicksum(
            self.choosen_items[i]*self.weights[i] for i in range(self.prices_size)
        ) <= self.capacity)