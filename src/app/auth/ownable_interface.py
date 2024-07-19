from abc import ABC, abstractmethod
from uuid import UUID


class IOwnable(ABC):
    @abstractmethod
    async def check_ownership(self, user_id: str, entity_id: str) -> bool:
        pass
