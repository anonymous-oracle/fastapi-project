from models import db, User, Response
from hashing import gen_salt, hash_pwd
from pickle import dumps


async def read_user(**kwargs):
    id_ = kwargs.get("id")
    if id_ != None:
        return db.query(User).filter(User.id == id_).first()
    username = kwargs.get("username")
    if username != None:
        return db.query(User).filter(User.username == username).first()


async def create_user(**kwargs):
    salt = gen_salt()
    password = kwargs.get("password")
    password = hash_pwd(password=password, salt=salt)
    kwargs["password"] = dumps(password)
    new_user = User(salt=dumps(salt), **kwargs)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_user(**kwargs):
    db.query(User).update(kwargs)
    db.commit()
    return True


async def create_response(**kwargs):
    new_response = Response(**kwargs)
    db.add(new_response)
    db.commit()
    db.refresh(new_response)
    return new_response


async def read_response(user_id: int, question_num: int):
    try:
        return (
            db.query(Response)
            .filter(Response.user_id)
            .filter(Response.question_num)
            .first()
        )
    except Exception as e:
        print(e)
        return None
