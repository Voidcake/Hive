import logging
from typing import List
from uuid import UUID

from neomodel import adb
from neomodel.exceptions import UniqueProperty, DoesNotExist

from src.app.townsquare.townsquare import Townsquare
from src.infra.db.crud_repository_interface import ICRUDRepository
from src.infra.db.db_types import GraphDataTypes as types
from src.infra.db.graph_repository_interface import IGraphRepository


class TownsquareRepository(ICRUDRepository, IGraphRepository):
    async def create(self, new_townsquare: Townsquare) -> Townsquare:
        async with adb.transaction:
            try:
                return await new_townsquare.save()
            except UniqueProperty:
                raise ValueError(f"Townsquare '{new_townsquare.name}' already exists")

    async def get(self, townsquare_id: UUID) -> Townsquare:
        townsquare: Townsquare | None = await Townsquare.nodes.get_or_none(uid=townsquare_id.hex)
        if not townsquare:
            raise LookupError(f"The Townsquare with ID '{townsquare_id}' not found in the Database")
        return townsquare

    async def get_all(self) -> List[Townsquare]:
        return await Townsquare.nodes.all()

    async def update(self, townsquare_id: UUID, **kwargs) -> Townsquare:
        try:
            townsquare: Townsquare = await self.get(townsquare_id)
            for key, value in kwargs.items():
                if value is not None:
                    old_value = getattr(townsquare, key)
                    setattr(townsquare, key, value)
                    logging.info(f"Updating {key}: '{old_value}' --> '{value}'")
            async with adb.transaction:
                return await townsquare.save()
        except DoesNotExist as e:
            logging.error(f"The Townsquare with ID '{townsquare_id}' not found in the Database: {str(e)}")
            raise LookupError(f"The Townsquare with ID '{townsquare_id}' not found in the Database") from e
        except UniqueProperty as e:
            logging.error(f"Townsquare '{kwargs.get('name')}' already exists: {str(e)}")
            raise ValueError(f"Townsquare '{kwargs.get('name')}' already exists: {str(e)}") from e
        except Exception as e:
            logging.error(f"Error updating Townsquare with ID '{townsquare_id}': {str(e)}")
            raise e

    async def delete(self, townsquare_id: UUID) -> str:
        try:
            townsquare: Townsquare = await self.get(townsquare_id)
            async with adb.transaction:
                await townsquare.delete()
                return f"Townsquare with ID '{townsquare_id}' successfully deleted"
        except DoesNotExist:
            logging.error(f"The Townsquare with ID '{townsquare_id}' not found in the Database")
            raise LookupError(f"The Townsquare with ID '{townsquare_id}' not found in the Database")
        except Exception as e:
            logging.error(f"Error deleting Townsquare with ID '{townsquare_id}': {str(e)}")
            raise e

    # Graph Constraints
    async def add_database_constraints(self, label: str, constraints=None):
        constraints: dict = {
            "node": {
                "uid":  ("unique", "required", types.STRING),
                "name": ("unique", "required", types.STRING),
                # "description": ("", "", types.STRING),
            }
        }
        await super().add_database_constraints(label, constraints)

    @staticmethod
    def get_repository() -> 'TownsquareRepository':
        return TownsquareRepository()
