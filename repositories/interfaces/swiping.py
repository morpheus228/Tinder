from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from repositories.postgres.models import Form


class Swiping(ABC):
    @abstractmethod
    def get_forms_without_rate(self, user_id: int) -> list[Form]:
        pass

    @abstractmethod
    def get_forms_with_negative_rate(self, user_id: int) -> list[Form]:
        pass