from datetime import datetime
from typing import List
from uuid import UUID

from src.app.townsquare.townsquare import Townsquare
from src.app.townsquare.townsquare_repository import TownsquareRepository
from src.app.user.user import User
from src.app.user.user_repository import UserRepository
from src.app.user.user_service import get_user_service


class TownsquareService:
    def __init__(self, townsquare_repository: TownsquareRepository, user_repository: UserRepository):
        self.townsquare_repository = townsquare_repository
        self.user_repository = user_repository
        self.user_service = get_user_service()

    async def create_townsquare(self, creator_id: UUID, name: str, description: str | None = None) -> Townsquare:
        if not description:
            description = f"Welcome to {name}!"

        new_townsquare: Townsquare = Townsquare(created_at=datetime.now(), name=name, description=description)
        new_townsquare = await self.townsquare_repository.create(new_townsquare)

        await self.user_service.join_townsquare(user_id=creator_id, townsquare_id=new_townsquare.uid)

        return new_townsquare

    async def get_townsquare(self, townsquare_id: UUID) -> Townsquare:
        return await self.townsquare_repository.get(townsquare_id)

    async def get_all_townsquares(self) -> List[Townsquare]:
        return await self.townsquare_repository.get_all()

    async def update_townsquare(self, townsquare_id: UUID, **kwargs) -> Townsquare:
        return await self.townsquare_repository.update(townsquare_id, **kwargs)

    async def delete_townsquare(self, townsquare_id: UUID) -> str:
        return await self.townsquare_repository.delete(townsquare_id)

    async def get_all_members(self, townsquare_id: UUID) -> List[User]:
        return await self.townsquare_repository.get_all_members(townsquare_id)


def get_townsquare_service() -> TownsquareService:
    return TownsquareService(TownsquareRepository(), UserRepository())
