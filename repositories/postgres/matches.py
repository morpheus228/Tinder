from sqlalchemy.orm import Session

from ..interfaces import Matches


class MatchesPostgres(Matches):
    def __init__(self, engine):
        self.engine = engine

		