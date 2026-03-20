import pytest
from src.classes.DistancesProblem import DistancesProblem
from gurobipy import GRB

def test_distances_problem():
    faculties_size = 5
    points_shape = (6, 2)
    
    budget = 10
    faculties_count = 3
    faculties_costs = [1, 2, 3, 4, 5]
    faculties_locations = [[2, 0], [0, 1], [1, 0], [0, 3], [0, 2]]
    points_locations = [[0, 0], [2, 2], [1, 1], [3, 0], [3, 3], [4, 4]]
    
    problem = DistancesProblem(faculties_size=faculties_size, points_shape=points_shape)
    
    solution = problem(
        budget=budget,
        faculties_count=faculties_count,
        faculties_costs=faculties_costs,
        faculties_locations=faculties_locations,
        points_locations=points_locations
    )
    
    assert problem.model.Status == GRB.OPTIMAL

    chosen_values = problem.choosen_faculties.X
    dist_values = problem.points_distribution.X
    
    assert sum(chosen_values) == pytest.approx(faculties_count)
    
    total_cost = sum(chosen_values[i] * faculties_costs[i] for i in range(faculties_size))
    assert total_cost <= budget
    
    for i in range(points_shape[0]):
        assert sum(dist_values[i, :]) == pytest.approx(1.0)
        
    for i in range(points_shape[0]):
        for j in range(faculties_size):
            if dist_values[i, j] > 0.5:
                assert chosen_values[j] > 0.5

    assert problem.model.ObjVal > 0