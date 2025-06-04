from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column

from models import Base


class User(Base):
    __tablename__ = 'users'
    id = mapped_column(Integer, primary_key=True, comment="идентификатор пользователя")
    name = mapped_column(String(100), nullable=False,comment="имя пользователя")
    is_active = mapped_column(Boolean, default=True, comment="Статус пользователя")
    email = mapped_column(String(100), nullable=False,comment="email пользователя")
