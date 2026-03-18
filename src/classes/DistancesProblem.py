from gurobipy import Model, GRB, quicksum
from src.const.general import PROBLEM_NAMES
import math

class DistancesProblem:
    """
    Optimization problem: choose faculties to minimize cost + distance to points.
    faculties = [...]
    points = [[0, 0], ...] (points_len, points_dim)
    """
    def __init__(self, faculties_size, points_shape):
        pass
        
    def __call__(self, faculties_costs, points, faculties_count):
        pass
    
    def initalize(self):
        pass
        
    def build_variables(self):
        pass
        
    def distance(self, point, faculty_index):
        pass
        
    def build_criterion(self):
        pass
        
    def build_constraints(self):
        pass