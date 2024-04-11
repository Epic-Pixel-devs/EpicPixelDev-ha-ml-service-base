# -- code: utf-8 --
import json

from .base_model import BaseModel


class AgentsModel(BaseModel):
    """
    description:
        BaseModel - base class to keep out some methods and variables
    """

    def __init__(self, agents) -> None:
        super().__init__(agents)

        self.agents = json.loads(agents)
