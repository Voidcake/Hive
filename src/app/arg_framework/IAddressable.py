from abc import ABC, abstractmethod
from uuid import UUID

from neomodel import AsyncStructuredNode


class IAddressable(ABC):
    @abstractmethod
    async def address_node(self, source_node_id: UUID, target_node_id: UUID) -> AsyncStructuredNode:
        """
        :param source_node_id
        :param target_node_id
        :raises ValueError
        :raises LookupError
        :return: AsyncStructuredNode
        """
        pass

    @abstractmethod
    async def disconnect_node(self, source_node_id: UUID, target_node_id: UUID) -> None:
        """
        :param source_node_id
        :param target_node_id
        :raises ValueError
        :raises LookupError
        :return: None
        """

        pass
