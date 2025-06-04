from fastapi import APIRouter, status, Body, HTTPException, Depends

from schemas.base_schemas import UserCreate, UserOutputSchemas, UpdateUser, User
from services.base_services import UserService

router = APIRouter(prefix="/v1", tags=["Пользователи"])



from pydantic import BaseModel, ValidationError


@router.get("/users", status_code= status.HTTP_200_OK, summary="Список пользоавтелей", description="Метод отдет список пользователей")
async def get_users(service: UserService = Depends()):
    return await service.get_users_all()

@router.post("/users-create", status_code=status.HTTP_201_CREATED, summary="Метод добаления пользователя", description="Метод создает нового пользователя")
async def create_user(user: UserCreate,
                      service: UserService = Depends()):
    return await service.create_user(user)

@router.put("/user/{user_id}", status_code=status.HTTP_200_OK, summary="Метод обновления пользователя", description="Метод изменяет пользователя")
async def update_user(user_id: int, user: UpdateUser, service: UserService = Depends()):
    return await service.update_user(user_id, user)


@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Метод удаления пользователя", description="Метод удаляет пользователя")
async def delete_user(user_id: int, service: UserService = Depends()):
    await service.delete_user(user_id)