from sqlalchemy import Column, Integer, String, BLOB
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import ForeignKey

DATABASE_URI = "sqlite:///./blog.db"

engine_ = create_engine(DATABASE_URI, connect_args={"check_same_thread": False})


Base = declarative_base()
db = Session(bind=engine_, autocommit=False, autoflush=False)


# class Blog(Base):
#     __tablename__ = "blogs"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     title = Column(String, nullable=False)
#     body = Column(String, nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     # user = relationship("User", backref="users")
#     user = relationship("User", back_populates="blogs")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    current_question = Column(Integer, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(BLOB, nullable=False)
    salt = Column(BLOB, nullable=False)

    responses = relationship("Response")


class Response(Base):
    __tablename__ = "response"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    option_num = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"))
    question_num = Column(Integer, nullable=False)
    user = relationship("User", back_populates="responses")


# class Response(Base): # relationship with
#     __tablename__ = "response"
#     id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
#     answer = Column(Integer, nullable=False)
#     user_id = Column(Integer, ForeignKey("user.id"))
#     question_id = Column(Integer, ForeignKey("question.id"))
#     user = relationship("User", back_populates="responses")
#     question = relationship("Question", back_populates="responses", uselist=False)


# class Question(Base):
#     __tablename__ = "question"
#     id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
#     response_id = Column(Integer, ForeignKey("response.id"))
#     response = relationship("Response", back_populates="question", uselist=False)


if __name__ == "__main__":
    Base.metadata.create_all(engine_)
