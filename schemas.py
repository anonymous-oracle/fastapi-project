from pydantic import BaseModel


class BaseUser(BaseModel):
    class Config:
        orm_mode = True


class BaseQuestionResponse(BaseModel):
    class Config:
        orm_mode = True


class User(BaseUser):
    username: str
    password: str


class UserResponse(BaseUser):
    id: int
    username: str


class QuestionResponse(BaseQuestionResponse):
    id: int
    user_id: int
    answer_num: int = 0
    question_num: int