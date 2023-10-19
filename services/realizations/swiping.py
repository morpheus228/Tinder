import repositories
import random
from repositories.postgres.models import Form
from services.interfaces import NoFormsError, Swiping, Forms


class SwipingService(Swiping):
    def __init__(self, repository: repositories.Swiping, 
                 rates_repository: repositories.Rates,
                 matches_repository: repositories.Matches,
                 forms_service: Forms):
                 
        self.repository: repositories.Swiping = repository
        self.rates_repository: repositories.Rates = rates_repository
        self.matches_repository: repositories.Matches = matches_repository
        self.forms_service: Forms = forms_service

    async def get_form(self, user_id: int, prev_form_id: int) -> Form:
        forms = self.repository.get_forms_without_rate(user_id)
        print("without Rates")
        print(forms)

        if len(forms) > 0:
            random.shuffle(forms)
            return await self.forms_service.get_by_id(forms[0])
        
        forms = self.repository.get_forms_with_negative_rate(user_id)
        print("with negative Rates")
        print(forms)

        if len(forms) == 0:
            raise NoFormsError()

        if len(forms) == 1:
            if forms[0] == prev_form_id:
                raise NoFormsError()
            else:
                return await self.forms_service.get_by_id(forms[0])

        while True:
            random.shuffle(forms)
            if forms[0] != prev_form_id:
                return await self.forms_service.get_by_id(forms[0])

    async def create_rate(self, user_id: int, form_id: int, value: bool):
        rate_id = self.rates_repository.create(user_id, form_id, value)

        if value:
            self.matches_repository.create(rate_id)

    