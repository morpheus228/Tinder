from sqlalchemy.orm import Session

from ..interfaces import Rates

from .models import Rate


class RatesPostgres(Rates):
    def __init__(self, engine):
        self.engine = engine

    def create(self, user_id: int, form_id: int, value: bool):
        with Session(self.engine) as session:
            session.add(Rate(user_id=user_id, form_id=form_id, value=value))
            session.commit()
#     def create(self, user_id: int, form_id: int, value: bool):
#         with Session(self.engine) as session:
#             subquery = session.query(Form.user_id, func.max(Form.created_at).label('max_created_at')).group_by(Form.user_id).subquery()

#             # # Запрос для получения форм, у которых время создания равно подзапросу
#             # query = session.query(Form).join(subquery, and_(Form.user_id == subquery.c.user_id,
#             #                                                 Form.created_at == subquery.c.max_created_at)).\
#             #         filter(Form.user_id == user_id).\
#             #         with_entities(Form.id)

# form_ids = [result[0] for result in query.all()]