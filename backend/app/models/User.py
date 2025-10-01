from sqlalchemy import Column, Integer, String, Text, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from app.db.base import Base, SessionLocal

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    vision_api = Column(Text)
    openai_api = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def signup(cls, **kwargs):
        new_user = cls(**kwargs)
        try:
            with SessionLocal() as session:
                session.add(new_user)
                session.commit()
            return new_user
        except Exception as e:
            session.rollback()
            print(f"エラーが発生しました。{e}")
            return None