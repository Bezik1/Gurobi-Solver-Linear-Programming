from gurobipy import Model, GRB, quicksum

from src.const.general import PROBLEM_NAMES
from src.classes.Problem import Problem


class KnapsackProblem(Problem):
    """
    Optimization problem: Select items with specific weights
    and prices to maximize value.

    Args:
        prices_size (int): Number of items available
            (based on price list).
        weights_size (int): Number of items available
            (based on weight list).
    """
    def __init__(self, prices_size: int, weights_size: int):
        self.prices = []
        self.prices_size = prices_size

        self.weights = []
        self.weights_size = weights_size

        self.initialize()

    def __call__(self, prices, weights, capacity):
        """
        Returns the optimized variables described in build_variables.

        Args:
            prices (int[prices_size]): The value/price of each item.
            weights (int[prices_size]): The weight of each item.
            capacity (int): The maximum total weight the knapsack can hold.

        Returns:
            Var[]: Variables representing which items were selected.
        """
        self.prices = prices
        self.weights = weights
        self.capacity = capacity

        self.build_criterion()
        self.build_constraints()

        self.model.optimize()

        return self.model.getVars()

    def initialize(self):
        self.model = Model(PROBLEM_NAMES["knapsack_problem"])
        self.build_variables()

    def build_variables(self):
        """
        Variables:
        - choosen_items GRB.BINARY[prices_size]:
            1 if item i is selected, 0 otherwise.
        """
        self.choosen_items = self.model.addMVar(
            self.prices_size,
            vtype=GRB.BINARY
        )

    def build_criterion(self):
        """
        Criterion: Maximize the total price (value) of the selected items.
        """
        self.model.setObjective(
            quicksum(
                self.choosen_items[i] * self.prices[i]
                for i in range(self.prices_size)
            ),
            GRB.MAXIMIZE
        )

    def build_constraints(self):
        """
        Constraints:
        - The total weight of selected items must not
          exceed the specified capacity.
        """
        self.model.addConstr(
            quicksum(
                self.choosen_items[i] * self.weights[i]
                for i in range(self.prices_size)
            ) <= self.capacity
        )
