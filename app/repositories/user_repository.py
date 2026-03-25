from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def create_user(db: Session, first_name: str, last_name: str, email: str, password: str):
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user