from abc import ABC, abstractmethod


class CRUDRepository(ABC):

    @abstractmethod
    async def create(self, entity):
        pass

    @abstractmethod
    async def get(self, uid: str):
        pass

    @abstractmethod
    async def update(self, uid: str, **kwargs):
        pass

    @abstractmethod
    async def delete(self, uid: str) -> str:
        pass
