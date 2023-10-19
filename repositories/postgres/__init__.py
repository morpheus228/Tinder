from sqlalchemy import create_engine

from config import PostgresConfig

from .users import UsersPostgres
from .forms import FormsPostgres
from .matches import MatchesPostgres
from .rates import RatesPostgres
from .swiping import SwipingPostgres
from .answers import AnswersPostgres

from .models import Base


def get_engine(config: PostgresConfig):
	engine_str = f"postgresql+psycopg2://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}"
	engine = create_engine(engine_str)
	return engine
