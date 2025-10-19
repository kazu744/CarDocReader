from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime,ForeignKey
from app.db.base import Base
from app.db.base import SessionLocal

class Ocr(Base):
    __tablename__ = "ocrs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    new_owner_name = Column(String(100))
    new_owner_address_main = Column(String(100))
    new_owner_address_street = Column(String(50))
    new_owner_address_number = Column(String(50))
    raw_text = Column(Text)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at  = Column(DateTime)
    deleted_at = Column(DateTime, nullable=True)

    @classmethod
    def create(cls, **kwargs):
        ocr_record = cls(**kwargs)
        with SessionLocal() as session:
            try:
                session.add(ocr_record)
                session.commit()
                session.refresh(ocr_record)
                return ocr_record
            except Exception as e:
                print(f"エラーが発生しました。{e}")
                return None
            
    @classmethod
    def get_by_user_id(cls, user_id):
        with SessionLocal() as session:
            return session.query(cls).filter(cls.user_id == user_id, cls.deleted_at.is_(None)).all()
        
    @classmethod
    def get_by_id(cls, ocr_id):
        with SessionLocal() as session:
            return session.query(cls).filter(cls.id == ocr_id).first()
        
    @classmethod
    def update(cls, ocr_id: int, **kwargs):
        with SessionLocal() as session:
            try:
                edit_ocr = session.get(cls, ocr_id)
                if edit_ocr is None:
                    return None
                for key, value in kwargs.items():
                    setattr(edit_ocr, key, value)
                session.commit()
                session.refresh(edit_ocr)
                return edit_ocr
            except Exception as err:
                session.rollback()
                print(f"エラー発生しました。{err}")
                return False