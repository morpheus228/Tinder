from sqlalchemy.orm import Session

from ..interfaces import Rates

from .models import Rate


class RatesPostgres(Rates):
    def __init__(self, engine):
        self.engine = engine

    def create(self, user_id: int, form_id: int, value: bool) -> int:
        with Session(self.engine) as session:
            rate = Rate(user_id=user_id, form_id=form_id, value=value)
            session.add(rate)
            session.commit()
            return rate.id
        
    def get_by_id(self, rate_id: int):
        with Session(self.engine) as session:
            return session.query(Rate).get(rate_id)        