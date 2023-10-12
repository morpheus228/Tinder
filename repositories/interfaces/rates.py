from abc import ABC, abstractmethod
from sqlalchemy.orm import Session


class Rates(ABC):
    @abstractmethod
    def create(self, user_id: int, form_id: int, value: bool):
        pass