from typing import List
from uuid import UUID

from neomodel import adb
from neomodel.exceptions import UniqueProperty, DoesNotExist

from src.app.arg_framework.premise.premise import Premise
from src.app.user.user import User
from src.infra.db.crud_repository_interface import ICRUDRepository
from src.infra.db.db_types import GraphDataTypes as types
from src.infra.db.graph_repository_interface import IGraphRepository


class PremiseRepository(ICRUDRepository, IGraphRepository):
    async def create(self, new_premise: Premise, author: User) -> Premise:
        try:
            new_premise = await new_premise.save()
            await new_premise.author.connect(author)
            return new_premise

        except UniqueProperty:
            raise ValueError(f"Premise '{new_premise}' already exists")

    async def get(self, premise_id: UUID) -> Premise:
        if type(premise_id) is UUID:
            premise_id = premise_id.hex

        premise: Premise | None = await Premise.nodes.get_or_none(uid=premise_id)
        if not premise:
            raise LookupError(f"The Premise with ID '{premise_id}' not found in the Database")
        return premise

    async def get_all(self) -> List[Premise]:
        return await Premise.nodes.all()

    async def update(self, premise_id: UUID, **kwargs) -> Premise:
        try:
            premise: Premise = await self.get(premise_id)

            for key, value in kwargs.items():
                if value is not None:
                    old_value = getattr(premise, key)
                    setattr(premise, key, value)
                    logging.info(f"Updating {key}: '{old_value}' --> '{value}'")

            async with adb.transaction:
                return await premise.save()

        except DoesNotExist as e:
            logging.error(f"The Premise with ID '{premise_id}' not found in the Database: {str(e)}")
            raise LookupError(f"The Premise with ID '{premise_id}' not found in the Database") from e
        except UniqueProperty as e:
            logging.error(f"Premise '{kwargs.get('content')}' already exists: {str(e)}")
            raise ValueError(f"Premise '{kwargs.get('content')}' already exists: {str(e)}") from e
        except Exception as e:
            logging.error(f"Error updating Premise with ID '{premise_id}': {str(e)}")
            raise e

    async def delete(self, premise_id: UUID) -> str:
        try:
            premise: Premise = await self.get(premise_id)
            async with adb.transaction:
                await premise.delete()
                return f"Premise '{premise_id}' deleted"

        except DoesNotExist as e:
            logging.error(f"The Premise with ID '{premise_id}' not found in the Database: {str(e)}")
            raise LookupError(f"The Premise with ID '{premise_id}' not found in the Database") from e

    async def add_database_constraints(self, label: str, constraints: dict = None):
        constraints: dict = {
            "node": {
                "uid":     ("unique", "required", types.STRING),
                "content": ("unique", "required", types.STRING),
            }
        }
        return await super().add_database_constraints(label, constraints)


def get_premise_repository() -> PremiseRepository:
    return PremiseRepository()
