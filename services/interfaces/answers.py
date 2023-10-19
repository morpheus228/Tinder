from abc import ABC, abstractmethod

from repositories.postgres.models import Form, Match


class Answers(ABC):  
    @abstractmethod
    async def get(self, user_id: int) -> tuple[Match, Form]:
        pass

    @abstractmethod
    async def create(self, user_id: int, match_id: Match, form_id: Form, value: bool) -> int|None:
        pass

    async def start(self, interval: int = 15 * 60):
        # while ``
        pass