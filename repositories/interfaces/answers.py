from abc import ABC, abstractmethod
from sqlalchemy.orm import Session


class Answers(ABC):
    @abstractmethod
    def get_matches_without_answer_by_user_id(self, user_id: int) -> list[tuple[int, int]]:
        pass

    @abstractmethod
    def get_user_ids_with_likes(self) -> list[int]:
        pass