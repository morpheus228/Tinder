from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from repositories.postgres.models import Rate


class Rates(ABC):
    @abstractmethod
    def create(self, user_id: int, form_id: int, value: bool) -> int:
        pass

    @abstractmethod
    def get_by_id(self, rate_id: int) -> Rate:
        pass