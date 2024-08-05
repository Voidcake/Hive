import logging
from typing import List
from uuid import UUID

from neomodel import adb
from neomodel.exceptions import UniqueProperty, DoesNotExist

from src.app.arg_framework.claim.claim import Claim
from src.app.user.user import User
from src.infra.db.crud_repository_interface import ICRUDRepository
from src.infra.db.db_types import GraphDataTypes as types
from src.infra.db.graph_repository_interface import IGraphRepository


class ClaimRepository(IGraphRepository, ICRUDRepository):
    async def create(self, new_claim: Claim, author: User) -> Claim:
        try:
            new_claim = await new_claim.save()
            await new_claim.author.connect(author)
            return new_claim

        except UniqueProperty:
            raise ValueError(f"Claim '{new_claim}' already exists")

    async def get(self, claim_id: UUID) -> Claim:
        if type(claim_id) is UUID:
            claim_id = claim_id.hex

        claim: Claim | None = await Claim.nodes.get_or_none(uid=claim_id)
        if not claim:
            raise LookupError(f"The Claim with ID '{claim_id}' not found in the Database")
        return claim

    async def get_all(self) -> List[Claim]:
        return await Claim.nodes.all()

    async def update(self, claim_id: UUID, **kwargs) -> Claim:
        try:
            claim: Claim = await self.get(claim_id)

            for key, value in kwargs.items():
                if value is not None:
                    old_value = getattr(claim, key)
                    setattr(claim, key, value)
                    logging.info(f"Updating {key}: '{old_value}' --> '{value}'")

            async with adb.transaction:
                return await claim.save()

        except DoesNotExist as e:
            logging.error(f"The Claim with ID '{claim_id}' not found in the Database: {str(e)}")
            raise LookupError(f"The Claim with ID '{claim_id}' not found in the Database") from e
        except UniqueProperty as e:
            logging.error(f"Claim '{kwargs.get('content')}' already exists: {str(e)}")
            raise ValueError(f"Claim '{kwargs.get('content')}' already exists: {str(e)}") from e
        except Exception as e:
            logging.error(f"Error updating Claim with ID '{claim_id}': {str(e)}")
            raise e

    async def delete(self, claim_id: UUID) -> str:
        try:
            claim: Claim = await self.get(claim_id)
            async with adb.transaction:
                await claim.delete()
                return f"Claim with ID '{claim_id}' successfully deleted"

        except DoesNotExist:
            logging.error(f"The Claim with ID '{claim_id}' not found in the Database")
            raise LookupError(f"The Claim with ID '{claim_id}' not found in the Database")

    async def add_database_constraints(self, label: str, constraints: dict = None):
        constraints: dict = {
            "node": {
                "uid":     ("unique", "required", types.STRING),
                "content": ("unique", "required", types.STRING)
            }
        }
        await super().add_database_constraints(label, constraints)


def get_claim_repository() -> ClaimRepository:
    return ClaimRepository()
