from aiogram import Bot
from config import Config
from repositories import Repository

from .realizations import *
from .interfaces import *


class Service:
	def __init__(self, repository: Repository, bot: Bot):
		self.forms: Forms = FormsService(repository.forms, bot)
		self.swiping: Swiping = SwipingService(repository.swiping, repository.rates, repository.matches, repository.answers, self.forms, bot)
		self.answers: Answers = AnswersService(repository.answers, repository.forms, repository.rates, repository.matches, self.forms, bot)

