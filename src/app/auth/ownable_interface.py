from abc import ABC, abstractmethod


class IOwnable(ABC):
    @abstractmethod
    async def check_ownership(self, user_id: str, entity_id: str) -> bool:
        pass
