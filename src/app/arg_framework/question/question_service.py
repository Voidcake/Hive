from datetime import datetime
from typing import List
from uuid import UUID

from neomodel import AsyncStructuredNode, adb

from src.app.arg_framework.IAddressable import IAddressable
from src.app.arg_framework.IOwnable import IOwnable
from src.app.arg_framework.question.question import Question
from src.app.arg_framework.question.question_repository import QuestionRepository
from src.app.townsquare.townsquare import Townsquare
from src.app.townsquare.townsquare_repository import TownsquareRepository
from src.app.user.user import User
from src.app.user.user_repository import UserRepository


class QuestionService(IOwnable, IAddressable):

    def __init__(self, question_repository: QuestionRepository, user_repository: UserRepository,
                 townsquare_repository: TownsquareRepository):
        self.question_repository: QuestionRepository = question_repository
        self.user_repository: UserRepository = user_repository
        self.townsquare_repository: TownsquareRepository = townsquare_repository

    async def create_question(self, author_id: UUID, question: str, description: str, townsquare_id: UUID | None,
                              addressed_node_id: UUID | None) -> Question:

        if not addressed_node_id and not townsquare_id:
            raise ValueError(f"A question needs address a node or a townsquare")

        new_question: Question = Question(created_at=datetime.now(), question=question,
                                          description=description)

        async with adb.transaction:
            try:
                author: User = await self.user_repository.get(author_id)

                if townsquare_id:
                    townsquare: Townsquare = await self.townsquare_repository.get(townsquare_id)
                    return await self.question_repository.create(new_question=new_question,
                                                                 author=author,
                                                                 townsquare=townsquare)
                else:
                    new_question: Question = await self.question_repository.create(new_question=new_question,
                                                                                   author=author, townsquare=None)
                    return await self.address_node(new_question, addressed_node_id)

            except LookupError as e:
                raise ValueError(f"Node not found") from e
            except ValueError as e:
                raise e

    async def get_question(self, question_id: UUID) -> Question:
        return await self.question_repository.get(question_id)

    async def get_all_questions(self) -> List[Question]:
        return await self.question_repository.get_all()

    async def check_ownership(self, user_id: UUID, question_id: UUID) -> bool:
        question: Question | None = await self.get_question(question_id)
        if not question:
            raise LookupError(f"The Question with ID '{question_id}' not found in the Database")

        author: User | None = await question.author.single()
        if not author:
            raise ValueError(f"Author of the Question with ID '{question_id}' not found")

        if author.uid != user_id:
            raise PermissionError("You are not the author of this question")

        return True

    async def update_question(self, question_id: UUID, **kwargs) -> Question:
        return await self.question_repository.update(question_id, **kwargs)

    async def delete_question(self, question_id: UUID) -> str:
        return await self.question_repository.delete(question_id)

    async def address_node(self, source_node: Question, target_node_id: UUID) -> Question:
        question: Question = source_node
        target_node: AsyncStructuredNode = await self.question_repository.query_nodes(target_node_id)

        await question.questions.connect(target_node)
        return question

    async def disconnect_node(self, source_node: UUID, target_node_id: UUID) -> Question:
        question: Question = await self.get_question(source_node)
        target_node: AsyncStructuredNode = await self.question_repository.query_nodes(target_node_id)

        await question.questions.disconnect(target_node)
        return question


def get_question_service() -> QuestionService:
    return QuestionService(QuestionRepository(), UserRepository(), TownsquareRepository())
