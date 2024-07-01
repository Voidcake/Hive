from typing import List

from src.app.townsquare.townsquare import Townsquare
from src.app.townsquare.townsquare_repository import TownsquareRepository
from src.app.user.user import User


class TownsquareService:
    def __init__(self, townsquare_repository: TownsquareRepository):
        self.townsquare_repository = townsquare_repository

    async def create_townsquare(self, name: str, description: str | None = None) -> Townsquare:
        if not description:
            description = f"Welcome to {name}!"

        new_townsquare: Townsquare = Townsquare(name=name, description=description)
        return await self.townsquare_repository.create(new_townsquare)

    async def get_townsquare_via_id(self, uid: str) -> Townsquare:
        return await self.townsquare_repository.get(uid)

    async def get_all_townsquares(self) -> List[Townsquare]:
        return await self.townsquare_repository.get_all()

    async def update_townsquare(self, uid: str, **kwargs) -> Townsquare:
        return await self.townsquare_repository.update(uid, **kwargs)

    async def delete_townsquare(self, uid: str) -> str:
        return await self.townsquare_repository.delete(uid)

    async def get_all_members(self, townsquare_id: str) -> List[User]:
        return await self.townsquare_repository.get_all_members(townsquare_id)


def get_townsquare_service() -> TownsquareService:
    return TownsquareService(TownsquareRepository())
