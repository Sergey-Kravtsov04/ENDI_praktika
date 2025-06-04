from pydantic import ValidationError, EmailStr
from sqlalchemy import select, update

from database import AsyncSession, get_session
from schemas.base_schemas import UserCreate, User, UserOutputSchemas, UpdateUser
from fastapi import Depends, HTTPException
from models.users import User as UserModel


class UserService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self._session = session

    async def email_validate_checker(self, email: EmailStr, exclude_user_id: int | None = None):
        query = select(UserModel).where(UserModel.email == email)
        if exclude_user_id: # Если передан exclude_user_id, добавляем условие исключения этого пользователя
            query = query.where(UserModel.id != exclude_user_id)
        result = await self._session.execute(query)

        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="Пользователь с таким email уже существует"
            )

    async def get_users_all(self):
        users = (await self._session.execute(
            select(UserModel).where(UserModel.is_active == True)
        )).scalars().all()

        if not users:
            raise HTTPException(status_code=404, detail="В базе данных нет пользователей")

        return users

    async def create_user(self, user: UserCreate)->UserOutputSchemas:
        await self.email_validate_checker(user.email)

        new_user = UserModel(**user.dict())
        self._session.add(new_user)
        await self._session.commit()
        await self._session.refresh(new_user)

        return UserOutputSchemas(message=f"Пользователь с id = {new_user.id}", user=User.model_validate(new_user))

    async def update_user(self, user_id: int, user: UpdateUser )->UserOutputSchemas:
        users = await self._session.execute(select(UserModel).where(UserModel.id == user_id))
        existing_user = users.scalar_one_or_none()

        if existing_user is None:
            raise HTTPException(status_code=404, detail=f"В базе данных пользователь с id = {user_id} не найден")

        await self._session.execute(update(UserModel)
                                    .where(UserModel.id == user_id)
                                    .values(**user.dict()))
        await self._session.commit()

        return UserOutputSchemas(message=f"Пользователь с id = {user_id} обновлен",user=User.model_validate(existing_user))

    async def delete_user(self, user_id: int)->UserOutputSchemas:
        users = await self._session.execute(select(UserModel).where(UserModel.id == user_id))
        existing_user = users.scalar_one_or_none()

        if existing_user is None:
            raise HTTPException(status_code=404, detail=f"В базе данных пользователь с id = {user_id} не найден")

        await self._session.execute(
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(is_active=False)
        )
        await self._session.commit()

