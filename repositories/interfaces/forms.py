from abc import ABC, abstractmethod
from aiogram import types

from ..postgres.models import Form, User


class Forms(ABC):
	@abstractmethod
	def create(self, form: Form) -> int:
		pass

	@abstractmethod
	def get_by_user_id(self, user_id: int) -> Form|None:
		pass
	
	@abstractmethod
	def get_by_id(self, form_id: int) -> Form|None:
		pass