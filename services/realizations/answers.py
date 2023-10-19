import random
from aiogram import Bot
from anyio import sleep
import repositories
from repositories.postgres.models import Form, Match
from repositories.repository import Repository
from services.interfaces import Answers, NoFormsError
from services.interfaces.forms import Forms
from utils.message_template import MessageTemplate


class AnswersService(Answers):  
    def __init__(self, repository: repositories.Answers, forms_repository: repositories.Forms, rates_repository: repositories.Rates, matches_repository: repositories.Matches, forms_service: Forms, bot: Bot):
        self.bot: Bot = bot
        self.repository: repositories.Answers = repository
        self.forms_repository: repositories.Forms = forms_repository
        self.rates_repository: repositories.Rates = rates_repository
        self.matches_repository: repositories.Matches = matches_repository
        self.forms_service: Forms = forms_service

    async def get(self, user_id: int) -> tuple[Match, Form]:
        matches = self.repository.get_matches_without_answer_by_user_id(user_id)

        if len(matches) == 0:
            raise NoFormsError()
    
        random.shuffle(matches)

        match_id, user_id = matches[0]
        form = await self.forms_service.get_by_user_id(user_id)
        match = self.matches_repository.get_by_id(match_id)

        return match, form

    async def create(self, user_id: int, match_id: int, form_id: int, value: bool) -> int|None:
        getter_rate_id = self.rates_repository.create(user_id, form_id, value)
        match = self.matches_repository.update(match_id, getter_rate_id=getter_rate_id, result=value)

        # if value is True:
        #     liker_rate = self.rates_repository.get_by_id(match.liker_rate_id)
            # await self.send_match_message(getter_rate.user_id, liker_rate.form_id)
            # await self.send_match_message(liker_rate.user_id, liker_rate.form_id)
        
    async def start(self, interval: int = 10):
        while True:
            a = False
            for user_id in self.repository.get_user_ids_with_likes():
                count = len(self.repository.get_matches_without_answer_by_user_id(user_id))
                text, reply_markup = MessageTemplate.from_json('answers/start').render(count=count)
                await self.bot.send_message(user_id, text=text, reply_markup=reply_markup)
            
            await sleep(interval)
    
    async def send_match_message(self, user_id: int, form_id: int):
        form = self.forms_repository.get_by_id(form_id)
        text, reply_markup = MessageTemplate.from_json('answers/match').render(form=form)
        self.bot.send_message(user_id, text=text, reply_markup=reply_markup)
                
