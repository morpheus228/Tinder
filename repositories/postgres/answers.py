from abc import ABC, abstractmethod
from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from repositories.interfaces.matches import Matches

from .models import Form, Match, Rate

from ..interfaces import Answers


class AnswersPostgres(Answers):
    def __init__(self, engine):
        self.engine = engine

    def get_matches_without_answer_by_user_id(self, user_id: int) -> list[tuple[int, int]]:
        with Session(self.engine) as session:
            query = session.query(Match).\
                            join(Rate, Rate.id == Match.liker_rate_id).\
                            join(Form, Form.id == Rate.form_id).\
                            filter(Form.user_id == user_id, Match.result == None).\
                            with_entities(Match.id, Rate.user_id)
            result = query.all()
            return result
        
    def get_user_ids_with_likes(self) -> list[int]:
        with Session(self.engine) as session:
            query = session.query(Match).\
                            join(Rate, Rate.id == Match.liker_rate_id).\
                            join(Form, Form.id == Rate.form_id).\
                            filter(Match.result == None).\
                            with_entities(Form.user_id).distinct()

            return [result[0] for result in query.all()]