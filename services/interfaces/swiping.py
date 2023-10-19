from abc import ABC, abstractmethod

from repositories.postgres.models import Form


class Swiping(ABC):
    @abstractmethod
    async def get_form(self, user_id: int, prev_form_id: int) -> int:
        pass
    
    @abstractmethod
    async def create_rate(self, user_id: int, form_id: int, value: bool):
        pass

    