from gurobipy import Model, GRB, quicksum

from src.const.general import PROBLEM_NAMES
from src.classes.Problem import Problem

class DistancesProblem(Problem):
    """
    Optimization problem: Choose faculties to minimize cost + distance to points.
    
    Args:
        faculties_size (int): Number of all faculties.
        points_shape (tuple[int]): Shape of the points composed of number of 
        all points and dimensions of the point.
    """
    def __init__(self, faculties_size, points_shape):
        self.faculties_size = faculties_size
        self.points_size, self.points_dim = points_shape
        
        self.initialize()
    
    def __call__(self, budget, faculties_count, faculties_costs, faculties_locations, points_locations):
        """
        Returns the optimized variables described in build_variables.
        
        Args:
            budget (int): Budget for faculties.
            faculties_count (int): Count of faculties
            faculties_costs (int[faculties_count]): List of costs of faculties.
            faculties_locations (int[faculties_count][point_dim]): Location of the faculties.
            points_locations (int[points_count][points_dim]): Location of the points.
        Returns:
            Var[]: Variables list, representing the choice of faculties and their assigned points.
        """
        self.budget = budget
        self.faculties_count = faculties_count
        self.faculties_costs = faculties_costs
        self.faculties_locations = faculties_locations
        self.points_locations = points_locations
        
        self.build_criterion()
        self.build_constraints()
        
        self.model.optimize()
        
        return self.model.getVars()
    
    def initialize(self):
        self.model = Model(PROBLEM_NAMES["distances_problem"])
        self.build_variables()
        
    def build_variables(self):
        """
        Variables:
        - choosen_faculties GRB.BINARY[faculties_size]: List of choosen faculties.
        - points_distribution GRB.BINARY[points_size, faculties_size]: Matrix of 
        assigments of points to specific faculty.
        """
        self.choosen_faculties = self.model.addMVar(self.faculties_size, vtype=GRB.BINARY)
        self.points_distribution = self.model.addMVar(
            (self.points_size, self.faculties_size), vtype=GRB.BINARY)
        
    def distance(self, point_index, faculty_index):
        """ Distance function implemented, as a squared euclidian distance.

        Args:
            point_index (int): Index of the choosen point.
            faculty_index (int): Index of the coresponding faculty.

        Returns:
            int: squared euclidian distance 
        """
        point = self.points_locations[point_index]
        faculty = self.faculties_locations[faculty_index]
        
        return sum(
            (point[dim] - faculty[dim]) ** 2
            for dim in range(self.points_dim)
        )
        
    def build_criterion(self):
        """
        Criterion: We minimize the sum of partial distances, from choosen faculties to their specified points.
        """
        self.model.setObjective(
            quicksum(
                self.distance(i, j) * self.points_distribution[i, j]
                for i in range(self.points_size)
                for j in range(self.faculties_size)
            ),
            GRB.MINIMIZE
        )
        
    def build_constraints(self):
        """
        Constrains:
        - Each point is assigned only once.
        - Count of choosen faculties must be equal to the faculties_count variable.
        - Cost of choosen faculties, must not exceed budget variable.
        - Points should be only assigned to choosen faculty.
        """
        for i in range(self.points_size):
            self.model.addConstr(
                self.points_distribution[i, :].sum() == 1
            )
            
            for j in range(self.faculties_size):
                self.model.addConstr(
                    self.points_distribution[i, j] <= self.choosen_faculties[j]
                )
        
        self.model.addConstr(
            self.choosen_faculties.sum() == self.faculties_count
        )
        
        self.model.addConstr(
            quicksum(self.choosen_faculties[i] * self.faculties_costs[i] 
                     for i in range(self.faculties_size)) <= self.budget
        )