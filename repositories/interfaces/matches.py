from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from repositories.postgres.models import Match


class Matches(ABC):
    @abstractmethod
    def create(self, rate_id: int) -> int:
        pass

    @abstractmethod
    def update(self, match_id: int, **kwargs):
        pass

    @abstractmethod
    def get_by_id(self, match_id: int) -> Match:
        pass

