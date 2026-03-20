import pytest
from src.classes.MakespanSchedulingProblem import MakespanSchedulingProblem

def test_makespan_scheduling_problem():
    tasks = [3, 9, 4, 7]
    processes_size = 2
    problem = MakespanSchedulingProblem(tasks_size=len(tasks), processes_size=processes_size)
    
    solution = problem(tasks)
    
    assert solution is not None
    allocations_vars = solution[:len(tasks) * processes_size]
    
    assert len(allocations_vars) == len(tasks) * processes_size
    
    values = [var.X for var in allocations_vars]
    for v in values:
        assert v in [0, 1]
    
    for i in range(len(tasks)):
        row_sum = sum(values[i*processes_size + j] for j in range(processes_size))
        assert row_sum == 1