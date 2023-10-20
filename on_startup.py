import random
from repositories.postgres.models import Form, User
from repositories.repository import Repository
from repositories.postgres.models import Base
from services.service import Service


async def on_startup(repository: Repository, service: Service):
    Base.metadata.drop_all(repository.engine)
    Base.metadata.create_all(repository.engine)

    # users = await create_users(repository)
    # await create_forms(repository, users)

    # my_id = 587247376
    # form_id = await create_me(repository, my_id)
    # await create_likes_to_me(service, form_id)


async def create_users(repository: Repository, count: int = 5):
    users = []
    for i in range(count):
        users.append(User(id=i, username=f"test{i}"))
        repository.users.create(users[i])
    return users

gender_searches = [True, False, None]

async def create_forms(repository: Repository, users: list[User], n: int = 2):
    for i in range(len(users)):
        for j in range(1):
            id = i*n + j
            repository.forms.create(Form(
                user_id=users[i].id, 
                gender=random.choice([True, False]),
                gender_search=gender_searches[random.choice([0, 1, 2])],
                name=f"Имя_{id}",
                faculty=f"Факультет_{id}",
                course=f"Курс_{id}",
                about=f"О себе_{id}",
                request=f"Запрос_{id}",
                photo_1=f"photo_{id}.jpg"))
            
            
async def create_me(repository: Repository, id: int ):
    repository.users.create(User(id=id, username="me"))
    return repository.forms.create(Form(user_id=id, username='me', gender=True, gender_search=False, name='Кирилл', photo_1='photo_0.jpg'))


async def create_likes_to_me(service: Service, form_id: int):
    await service.swiping.create_rate(0, form_id, True)    
    await service.swiping.create_rate(1, form_id, True)    
    await service.swiping.create_rate(2, form_id, False)    