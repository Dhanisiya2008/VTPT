from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    weight = Column(Integer)
    goal = Column(String)
    intensity = Column(String)
    original_plan = Column(Text)
    updated_plan = Column(Text)

Base.metadata.create_all(bind=engine)

def save_user(session, user_data):
    user = User(**user_data)
    session.add(user)
    session.commit()
    return user

def save_plan(session, user_id, plan):
    user = session.query(User).filter(User.id == user_id).first()
    user.original_plan = plan
    session.commit()

def update_plan(session, user_id, updated_plan):
    user = session.query(User).filter(User.id == user_id).first()
    user.updated_plan = updated_plan
    session.commit()

def get_user(session, user_id):
    return session.query(User).filter(User.id == user_id).first()

def get_all_users(session):
    return session.query(User).all()
                    