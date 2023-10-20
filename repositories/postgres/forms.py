from ..interfaces import Forms

from sqlalchemy.orm import Session
from .models import Form

from aiogram import types


class FormsPostgres(Forms):
    def __init__(self, engine):
        self.engine = engine

    # def get_by_id(self, user_id: int) -> User|None:
    #     with Session(self.engine) as session:
    #         return session.query(User).get(user_id)
    
    def create(self, form: Form) -> int:
        with Session(self.engine) as session:
            session.add(form)
            session.commit()
            return form.id
    
    def get_by_user_id(self, user_id: int) -> Form|None:
        with Session(self.engine) as session:
            return session.query(Form).filter_by(user_id=user_id).order_by(Form.created_at).first()
    
    def get_by_id(self, form_id: int) -> Form|None:
        with Session(self.engine) as session:
            return session.query(Form).get(form_id)
        
    def delete_by_user_id(self, user_id: int):
        with Session(self.engine) as session:
            session.query(Form).filter_by(user_id=user_id).delete()
            session.commit()
		