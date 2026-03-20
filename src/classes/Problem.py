from abc import ABC, abstractmethod

class Problem(ABC):
    """
    Problem class it's a templated designated, for a structure of Linear Programming
    Problem class. Abstract methods are meant, to be used with the cooperation with gurobi
    solver engine.
    """
    
    @abstractmethod
    def __call__(self):
        """
        This method should be used, as a run optimization method. Within it, there
        should be implemented a way of collecting required data and build_criterion,
        build_constraints and optimization method should be called here.
        """
        pass
    
    @abstractmethod
    def initialize(self):
        """
        Initialize gurobi model and invokes build_variables method. It can be
        also used, for any preparation process, that may be needed.
        """
        pass
    
    @abstractmethod
    def build_variables(self):
        """
        This method should initialize all variables, that would be later optimized,
        by the gurobi solving engine.
        """
        pass
    
    @abstractmethod
    def build_criterion(self):
        """
        This method should implement the optimization method / the criterion, for
        the solving model.
        """
        pass
    
    @abstractmethod
    def build_constraints(self):
        """
        The problems constraints should be specified here.
        """
        pass