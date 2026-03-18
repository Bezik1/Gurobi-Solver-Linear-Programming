import pytest
from src.classes.KnapsackProblem import KnapsackProblem

def test_knapsack_problem():
    prices = [1, 2, 3, 4, 5]
    weights = [1, 2, 3, 4, 5]
    capacity = 7
    
    problem = KnapsackProblem(prices_size=len(prices), weights_size=len(weights))
    
    solution = problem(prices, weights, capacity)
    
    assert solution is not None
    assert len(solution) == len(prices)
    
    values = [var.X for var in solution]
    for v in values:
        assert v in [0, 1]

def test_knapsack_solution_with_full_capacity():
    prices = [10, 20, 30]
    weights = [5, 5, 5]
    capacity = 10
    
    problem = KnapsackProblem(prices_size=len(prices), weights_size=len(weights))
    
    solution = problem(prices, weights, capacity)
    
    values = [var.X for var in solution]
    total_weight = sum(w * x for w, x in zip(weights, values))
    total_price = sum(p * x for p, x in zip(prices, values))
    
    assert total_weight <= capacity
    assert any(values)