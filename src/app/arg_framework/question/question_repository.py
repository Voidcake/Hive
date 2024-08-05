import logging
from typing import List
from uuid import UUID

from neomodel import adb
from neomodel.exceptions import UniqueProperty, DoesNotExist

from src.app.arg_framework.question.question import Question
from src.app.townsquare.townsquare import Townsquare
from src.app.user.user import User
from src.infra.db.crud_repository_interface import ICRUDRepository
from src.infra.db.db_types import GraphDataTypes as types
from src.infra.db.graph_repository_interface import IGraphRepository


class QuestionRepository(IGraphRepository, ICRUDRepository):
    async def create(self, new_question: Question, author: User, townsquare: Townsquare | None) -> Question:
        try:
            await new_question.save()
            await new_question.author.connect(author)

            if townsquare:
                await new_question.townsquare.connect(townsquare)

            return new_question

        except UniqueProperty:
            raise ValueError(f"Question '{new_question.question}' already exists")

    async def get(self, question_id: UUID) -> Question:
        question: Question | None = await Question.nodes.get_or_none(uid=question_id)
        if not question:
            raise LookupError(f"The Question with ID '{question_id}' not found in the Database")
        return question

    async def get_all(self) -> List[Question]:
        return await Question.nodes.all()

    async def update(self, question_id: UUID, **kwargs) -> Question:
        try:
            question: Question = await self.get(question_id)
            for key, value in kwargs.items():
                if value is not None:
                    old_value = getattr(question, key)
                    setattr(question, key, value)
                    logging.info(f"Updating {key}: '{old_value}' --> '{value}'")
            async with adb.transaction:
                return await question.save()
        except DoesNotExist as e:
            logging.error(f"The Question with ID '{question_id}' not found in the Database: {str(e)}")
            raise LookupError(f"The Question with ID '{question_id}' not found in the Database") from e
        except UniqueProperty as e:
            logging.error(f"Question '{kwargs.get('title')}' already exists: {str(e)}")
            raise ValueError(f"Question '{kwargs.get('title')}' already exists: {str(e)}") from e
        except Exception as e:
            logging.error(f"Error updating Question with ID '{question_id}': {str(e)}")
            raise e

    async def delete(self, question_id: UUID) -> str:
        try:
            question: Question = await self.get(question_id)
            async with adb.transaction:
                await question.delete()
                return f"Question with ID '{question_id}' successfully deleted"
        except DoesNotExist:
            logging.error(f"The Question with ID '{question_id}' not found in the Database")
            raise LookupError(f"The Question with ID '{question_id}' not found in the Database")
        except Exception as e:
            logging.error(f"Error deleting Question with ID '{question_id}': {str(e)}")
            raise e

    async def add_database_constraints(self, label: str, constraints: dict = None):
        constraints: dict = {
            'node': {
                'uid':         ("unique", "required", types.STRING),
                'question': ("unique", "required", types.STRING),
                'description': ("unique", types.STRING)
            }
        }
        await super().add_database_constraints(label, constraints)


def get_question_repository():
    return QuestionRepository()
