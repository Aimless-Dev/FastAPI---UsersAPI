from fastapi import APIRouter, HTTPException
from schemas.user import User, UserUpdate
from models.user import users
from config.db import conn
from sqlalchemy import func, select
from passlib.hash import sha256_crypt

user = APIRouter()

@user.get('/users')
def get_users():
    return conn.execute(users.select()).fetchall()

@user.get('/users/count')
def get_users_count():
    result = conn.execute(select([func.count()]).select_from(users))
    return {'total': tuple(result)[0][0]}

@user.get('/users/{user_id}')
def get_user(user_id: str):
    result = conn.execute(users.select().where(users.c.id == user_id)).first()
    if not (result == None):
        return result
    raise HTTPException(status_code=404, detail='User not found')


@user.post('/users')
def create_user(user: User):
    user.password = sha256_crypt.encrypt(str(user.dict()['password']))
    result = conn.execute(users.insert().values(user.dict()))
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()

@user.put('/users/{user_id}')
def update_user(user_id: str, newData: UserUpdate):
    result = conn.execute(users.select().where(users.c.id == user_id)).first()
    if not (result == None):
        conn.execute(users.update().values(name=newData.name, email=newData.email, password=sha256_crypt.encrypt(str(newData.password))).where(users.c.id == user_id))
        return {'message': 'User has been uploated successfully'}
    raise HTTPException(status_code=404, detail='User not found')

@user.delete('/users/{user_id}')
def delete_user(user_id: str):
    result = conn.execute(users.select().where(users.c.id == user_id)).first()
    if not (result == None):
        conn.execute(users.delete().where(users.c.id == user_id))
        return {'message': 'User has been deleted successfully'}
    raise HTTPException(status_code=404, detail='User not found')