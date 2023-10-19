from abc import ABC, abstractmethod
from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from .models import Form, Rate

from ..interfaces import Swiping


class SwipingPostgres(Swiping):
    def __init__(self, engine):
        self.engine = engine

    # получаем анкеты, которые еще не оценил пользователь 
    def get_forms_without_rate(self, user_id: int) -> list[Form]:
        with Session(self.engine) as session:
            subquery = session.query(Form.user_id, func.max(Form.created_at).label('created_at')).group_by(Form.user_id).subquery()
            
            query = session.query(Form).join(subquery, 
                            and_(Form.user_id == subquery.c.user_id, Form.created_at == subquery.c.created_at)).\
                            filter(Form.user_id != user_id).\
                            outerjoin(Rate, and_(Rate.user_id == user_id, Rate.form_id == Form.id)).\
                            filter(Rate.id.is_(None)).with_entities(Form.id)
            
            return [result[0] for result in query.all()]
        
    # получаем анкеты, которые пользователь оценил отприцательно
    def get_forms_with_negative_rate(self, user_id: int) -> list[Form]:
        with Session(self.engine) as session:
            subquery = session.query(Form.user_id, func.max(Form.created_at).label('created_at')).group_by(Form.user_id).subquery()
            
            query = session.query(Form).join(subquery, 
                            and_(Form.user_id == subquery.c.user_id, Form.created_at == subquery.c.created_at)).\
                            filter(Form.user_id != user_id).\
                            outerjoin(Rate, and_(Rate.user_id == user_id, Rate.form_id == Form.id)).\
                            filter(Rate.value == False).with_entities(Form.id)
            
            return [result[0] for result in query.all()]