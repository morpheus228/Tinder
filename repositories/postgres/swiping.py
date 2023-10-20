from abc import ABC, abstractmethod
from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from .models import Form, Rate

from ..interfaces import Swiping


class SwipingPostgres(Swiping):
    def __init__(self, engine):
        self.engine = engine

    # получаем анкеты, которые еще не оценил пользователь 
    def get_forms_without_rate(self, user_id: int, user_form: Form) -> list[int]:
        with Session(self.engine) as session:
            subquery = session.query(Form.user_id, func.max(Form.created_at).label('created_at')).group_by(Form.user_id).subquery()
            
            forms = session.query(Form).join(subquery, 
                            and_(Form.user_id == subquery.c.user_id, Form.created_at == subquery.c.created_at)).\
                            filter(Form.user_id != user_id).\
                            outerjoin(Rate, and_(Rate.user_id == user_id, Rate.form_id == Form.id)).\
                            filter(Rate.id.is_(None)).all()
            
            print(f"Изначально: {[form.id for form in forms]}")
            
            return [form.id for form in forms if self.gender_filter(user_form, form)]
        
    # получаем анкеты, которые пользователь оценил отприцательно
    def get_forms_with_negative_rate(self, user_id: int, user_form: Form) -> list[int]:
        with Session(self.engine) as session:
            subquery = session.query(Form.user_id, func.max(Form.created_at).label('created_at')).group_by(Form.user_id).subquery()
            
            forms = session.query(Form).join(subquery, 
                            and_(Form.user_id == subquery.c.user_id, Form.created_at == subquery.c.created_at)).\
                            filter(Form.user_id != user_id).\
                            outerjoin(Rate, and_(Rate.user_id == user_id, Rate.form_id == Form.id)).\
                            filter(Rate.value == False).all()
            
            print(f"Изначально: {[form.id for form in forms]}")
            
            forms = [form.id for form in forms if self.gender_filter(user_form, form)]
            positive_forms = self.get_forms_with_positive_rate(user_id, user_form)
            return list(set(forms) - set(positive_forms))
    
    def get_forms_with_positive_rate(self, user_id: int, user_form: Form) -> list[Form]:
        with Session(self.engine) as session:
            subquery = session.query(Form.user_id, func.max(Form.created_at).label('created_at')).group_by(Form.user_id).subquery()
            
            forms = session.query(Form).join(subquery, 
                            and_(Form.user_id == subquery.c.user_id, Form.created_at == subquery.c.created_at)).\
                            filter(Form.user_id != user_id).\
                            outerjoin(Rate, and_(Rate.user_id == user_id, Rate.form_id == Form.id)).\
                            filter(Rate.value == True).all()
            
            return [form.id for form in forms if self.gender_filter(user_form, form)]
        
    def gender_filter(self, user_form: Form, form: Form):
        return self.check_forms_convergence(user_form, form) and self.check_forms_convergence(form, user_form)
        
    @staticmethod
    def check_forms_convergence(form_1: Form, form_2: Form):
        if form_1.gender_search is not None:
            return form_1.gender_search == form_2.gender
        return True