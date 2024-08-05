from abc import ABC, abstractmethod
from uuid import UUID


class IOwnable(ABC):
    @abstractmethod
    async def check_ownership(self, user_id: UUID, entity_id: UUID) -> bool:
        # TODO: consolidate logic from services that implement IOwnable here for a generic type of node entity!
        pass
