from abc import ABC, abstractmethod


class Problem(ABC):
    """
    Problem class is a template for Linear Programming Problem classes.
    Abstract methods are intended to be used with the Gurobi solver engine.
    """

    @abstractmethod
    def __call__(self):
        """
        This method should be used as the run optimization method. It should
        collect required data, then call build_criterion, build_constraints,
        and execute the optimization.
        """
        pass

    @abstractmethod
    def initialize(self):
        """
        Initialize the Gurobi model and invoke build_variables. Can also
        prepare any other required setup.
        """
        pass

    @abstractmethod
    def build_variables(self):
        """
        Initialize all variables that will be optimized by Gurobi.
        """
        pass

    @abstractmethod
    def build_criterion(self):
        """
        Implement the optimization criterion for the model.
        """
        pass

    @abstractmethod
    def build_constraints(self):
        """
        Specify the problem's constraints here.
        """
        pass
