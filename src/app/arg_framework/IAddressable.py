from abc import ABC, abstractmethod
from enum import Enum
from uuid import UUID

from neomodel import AsyncStructuredNode


class IAddressable(ABC):
    @abstractmethod
    async def address_node(self, source_node: UUID | AsyncStructuredNode, target_node_id: UUID,
                           relationship_type: Enum | None = None) -> AsyncStructuredNode:
        """
        :param source_node:
        :param target_node_id
        :param relationship_type
        :raises ValueError
        :raises LookupError
        :return: AsyncStructuredNode
        """
        pass

    @abstractmethod
    async def disconnect_node(self, source_node: UUID | AsyncStructuredNode,
                              target_node_id: UUID) -> AsyncStructuredNode:
        """
        :param source_node
        :param target_node_id
        :raises ValueError
        :raises LookupError
        :return: None
        """

        pass
