from fastapi import FastAPI, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from crud import (
    create_response,
    create_user,
    read_response,
    read_user,
    update_response,
    update_user,
)
from auth import get_current_user, get_token, authenticate_user, HTTPException
import models, schemas

app = FastAPI()


@app.post("/login")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(
        username=form_data.username, password=form_data.password
    )
    if user == False:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    user_obj = {"username": user.username, "password": user.password, "id": user.id}
    return get_token(user_obj)


@app.post("/users", response_model=schemas.UserResponse)
async def post_user(user: schemas.User):
    return await create_user(
        username=user.username, password=user.password, current_question=0
    )


@app.get("/users/me", response_model=schemas.UserResponse)
async def get_user_me(user: models.User = Depends(get_current_user)):
    return user


@app.post("/start", response_model=schemas.QuestionResponse)
async def start_exam(user: models.User = Depends(get_current_user)):
    user = await read_user(id=user.id)
    user.current_question = 1
    await update_user(
        id=user.id,
        current_question=user.current_question,
        username=user.username,
        password=user.password,
        salt=user.salt,
    )
    response = await create_response(
        id=user.id, question_num=user.current_question, user=user, option_num=0
    )

    
    return response


@app.post("/submit/{option}", response_model=schemas.QuestionResponse)
async def submit_answer(option: int, user: models.User = Depends(get_current_user)):
    response = await read_response(user_id=user.id, question_num=user.current_question)
    response.option_num = option
    await update_response(
        id=response.id,
        option_num=response.option_num,
        question_num=response.question_num,
        user_id=response.user_id,
    )

    return response


@app.get("/next", response_model=schemas.QuestionResponse)
async def next_question(user: models.User = Depends(get_current_user)):
    user.current_question += 1
    await update_user(
        id=user.id,
        current_question=user.current_question,
        username=user.username,
        password=user.password,
        salt=user.salt,
    )
    response = await read_response(user_id=user.id, question_num=user.current_question)
    if response == None:
        response = await create_response(
            user_id=user.id, question_num=user.current_question, user=user, option_num=0
        )
    
    return response


@app.get("/previous", response_model=schemas.QuestionResponse)
async def previous_question(user: models.User = Depends(get_current_user)):
    user.current_question -= 1
    await update_user(
        id=user.id,
        current_question=user.current_question,
        username=user.username,
        password=user.password,
        salt=user.salt,
    )
    response = await read_response(user_id=user.id, question_num=user.current_question)
    # if response == None:
    #     response = await create_response(
    #         user_id=user.id, question_num=user.current_question, user=user
    #     )
    return response


@app.get("/users/{username}", response_model=schemas.UserResponse)
async def get_user(username: str):
    return await read_user(username=username)
