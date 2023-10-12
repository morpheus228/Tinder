import repositories
import random
from repositories.postgres.models import Form
from services.interfaces import Swiping


class SwipingService(Swiping):
    def __init__(self, repository: repositories.Swiping):
        self.repository: repositories.Swiping = repository

    async def get_form(self, user_id: int) -> Form:
        forms = self.repository.get_forms_without_rate(user_id)

        if len(forms) > 0:
            random.shuffle(forms)
            return forms[0]

    async def get_forms(self, user_id: int) -> Form:
        forms = self.repository.get_forms_without_rate( )
        # получаем анкеты, которые еще не оценил пользователь
        # перешиваем их в случайном порядке

        # получаем анкеты, которые пользователь оценил отприцательно
        # перешиваем их в случайном порядке

        # merge двух этих списков в один
        # return список

        pass

    async def create_rate(self, user_id: int, form_id: int, value: bool):
        # создаем объект Rate

        if value:
            # создаем объект Match
            pass

    