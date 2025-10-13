from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Text, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from app.db.base import Base, SessionLocal

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    vision_api = Column(Text)
    openai_api = Column(Text)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def signup(cls, password, **kwargs):
        new_user = cls(**kwargs)
        new_user.set_password(password)
        with SessionLocal() as session:
            try:
                session.add(new_user)
                session.commit()
                return new_user
            except Exception as e:
                session.rollback()
                print(f"エラーが発生しました。{e}")
                return None
        
    @classmethod
    def profile_edit(cls, user_id, password, **kwargs):
        with SessionLocal() as session:
            try:
                edit_user = session.get(cls, user_id)
                if password:
                    edit_user.set_password(password)
                for key, value in kwargs.items():
                    setattr(edit_user, key, value)
                session.commit()
                session.refresh(edit_user)
                return edit_user
            except Exception as e:
                session.rollback()
                print(f"エラーが発生しました。{e}")
                return None
        
    @classmethod
    def get_by_email(cls, email):
        with SessionLocal() as session:
            return session.query(cls).filter(cls.email == email).first()
        
    @classmethod
    def get_by_id(cls, id):
        with SessionLocal() as session:
            return session.query(cls).filter(cls.id == id).first()
        
    