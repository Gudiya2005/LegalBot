from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Base class for all agents in LegalBot.
    Every agent must inherit from this class.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, context):
        """  
        Execute the agent's task.

        Parameters:
            context: Shared AgentContext object.

        Returns:
            Updated AgentContext.
        """
        pass