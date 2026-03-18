import pytest
from src.classes.PartitionProblem import PartitionProblem


def test_partition_problem():
    data = [3, 9, 4, 7, 6, 5, 11]
    problem = PartitionProblem(input_size=len(data))
    
    solution = problem(data)
    
    assert solution is not None
    assert len(solution) == len(data)
    
    values = [var.X for var in solution]
    for v in values:
        assert v in [0, 1]
        
