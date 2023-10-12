from .postgres import *
from .interfaces import *


class Repository:
	def __init__(self, engine):
		self.engine = engine
		
		self.users: Users = UsersPostgres(engine)
		self.forms: Forms = FormsPostgres(engine)
		self.rates: Rates = RatesPostgres(engine)
		self.matches: Matches = MatchesPostgres(engine)
		self.swiping: Swiping = SwipingPostgres(engine)
