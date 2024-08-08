import logging
from typing import List
from uuid import UUID

from neomodel import adb
from neomodel.exceptions import UniqueProperty, DoesNotExist

from src.app.arg_framework.evidence.evidence import Evidence
from src.app.user.user import User
from src.infra.db.crud_repository_interface import ICRUDRepository
from src.infra.db.db_types import GraphDataTypes as types
from src.infra.db.graph_repository_interface import IGraphRepository


class EvidenceRepository(IGraphRepository, ICRUDRepository):
    async def create(self, new_evidence: Evidence, author: User) -> Evidence:
        try:
            new_evidence = await new_evidence.save()
            await new_evidence.author.connect(author)
            return new_evidence

        except UniqueProperty:
            raise ValueError(f"Evidence '{new_evidence}' already exists")

    async def get(self, evidence_id: UUID) -> Evidence:
        if evidence_id is UUID:
            evidence_id = evidence_id.hex

        evidence: Evidence | None = await Evidence.nodes.get_or_none(uid=evidence_id)
        if not evidence:
            raise LookupError(f"The Evidence with ID '{evidence_id}' not found in the Database")
        return evidence

    async def get_all(self) -> List[Evidence]:
        return await Evidence.nodes.all()

    async def update(self, evidence_id: UUID, **kwargs) -> Evidence:
        try:
            evidence: Evidence = await self.get(evidence_id)

            for key, value in kwargs.items():
                if value is not None:
                    old_value = getattr(evidence, key)
                    setattr(evidence, key, value)
                    logging.info(f"Updating {key}: '{old_value}' --> '{value}'")

            async with adb.transaction:
                return await evidence.save()

        except DoesNotExist as e:
            logging.error(f"The Evidence with ID '{evidence_id}' not found in the Database: {str(e)}")
            raise LookupError(f"The Evidence with ID '{evidence_id}' not found in the Database") from e
        except UniqueProperty as e:
            logging.error(f"Evidence '{kwargs.get('content')}' already exists: {str(e)}")
            raise ValueError(f"Evidence '{kwargs.get('content')}' already exists: {str(e)}") from e
        except Exception as e:
            logging.error(f"Error updating Evidence with ID '{evidence_id}': {str(e)}")
            raise e

    async def delete(self, evidence_id: UUID) -> str:
        try:
            evidence: Evidence = await self.get(evidence_id)
            async with adb.transaction:
                await evidence.delete()
                return f"Evidence with ID '{evidence_id}' successfully deleted"
        except DoesNotExist as e:
            logging.error(f"The Evidence with ID '{evidence_id}' not found in the Database: {str(e)}")
            raise LookupError(f"The Evidence with ID '{evidence_id}' not found in the Database") from e

    async def add_database_constraints(self, label: str, constraints: dict = None):
        constraints: dict = {
            "node": {
                "uid":     ("unique", "required", types.STRING),
                "content": ("unique", "required", types.STRING),
            }
        }
        await super().add_database_constraints(label, constraints)


def get_evidence_repository() -> EvidenceRepository:
    return EvidenceRepository()
