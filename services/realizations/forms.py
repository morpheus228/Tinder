from aiogram import Bot
from aiogram.types import FSInputFile

import repositories
from repositories.postgres.models import Form
from utils.files import save_document
from ..interfaces import Forms



class FormsService(Forms):
	def __init__(self, repository: repositories.Forms, bot: Bot):
		self.repository: repositories.Forms = repository
		self.bot: Bot = bot

	async def create(self, user_id: int, data: dict) -> int:
		photo_1 = max(data['photo_1'], key=lambda x: x.file_size)
		photo_1_path = await save_document(self.bot, user_id, photo_1)

		return self.repository.create(Form(
			user_id = user_id,
			name = data['name'],
			about = data['about'],
			request = data['request'],
			photo_1 = photo_1_path
		))
	
	async def get(self, user_id: int) -> Form:
		form = self.repository.get_by_user_id(user_id)
		
		if form is not None:
			form.photo_1 = FSInputFile("files/" + form.photo_1)
			
		return form
	