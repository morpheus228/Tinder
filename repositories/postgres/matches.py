from sqlalchemy.orm import Session

from .models import Match

from ..interfaces import Matches


class MatchesPostgres(Matches):
    def __init__(self, engine):
        self.engine = engine

    def create(self, rate_id: int) -> int:
        with Session(self.engine) as session:
            match = Match(liker_rate_id=rate_id)
            session.add(match)
            session.commit()
            return match.id
        
    def get_by_id(self, match_id: int) -> Match:
        with Session(self.engine) as session:
            return session.query(Match).get(match_id)
        
    def update(self, match_id: int, **kwargs) -> Match:
        match = self.get_by_id(match_id)
            
        with Session(self.engine) as session:
            for attr, value in kwargs.items():
                match.__setattr__(attr, value)

            session.add(match)
            session.commit()
        
        return match


		