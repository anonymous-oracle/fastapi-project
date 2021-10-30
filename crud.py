from sqlalchemy.sql.expression import update
from models import db, User, Response
from hashing import gen_salt, hash_pwd


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
    kwargs["password"] = password
    new_user = User(salt=salt, **kwargs)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_user(
    id: int, current_question: int, username: str, password: str, salt: str
):
    try:
        db.query(User).filter(User.id == id).update(
            {
                User.current_question: current_question,
                User.username: username,
                User.password: password,
                User.salt: salt,
            }
        )

        db.commit()
        return True
    except Exception as e:
        print(e)
        return False


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
            .filter(Response.user_id == user_id)
            .filter(Response.question_num == question_num)
            .first()
        )
    except Exception as e:
        print(e)
        return None


async def update_response(id: int, option_num: int, question_num: int, user_id: int):
    try:
        # db.query(Response).update(kwargs)
        db.query(Response).filter(User.id == id).update(
            {
                Response.option_num: option_num,
                Response.question_num: question_num,
                Response.user_id: user_id,
            }
        )

        db.commit()
        return True
    except Exception as e:
        print(e)
        return False
