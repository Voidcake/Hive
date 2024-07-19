from datetime import datetime
from typing import List
from uuid import UUID

from src.app.arg_framework.question.question import Question
from src.app.arg_framework.question.question_repository import QuestionRepository
from src.app.auth.ownable_interface import IOwnable
from src.app.townsquare.townsquare import Townsquare
from src.app.townsquare.townsquare_repository import TownsquareRepository
from src.app.user.user import User
from src.app.user.user_repository import UserRepository


class QuestionService(IOwnable):

    def __init__(self, question_repository: QuestionRepository, user_repository: UserRepository,
                 townsquare_repository: TownsquareRepository):
        self.question_repository = question_repository
        self.user_repository = user_repository
        self.townsquare_repository = townsquare_repository

    async def create_question(self, author_id: str, townsquare_id: str, title: str, description: str) -> Question:
        new_question: Question = Question(title=title, description=description)

        author: User = await self.user_repository.get(author_id)
        townsquare: Townsquare = await self.townsquare_repository.get(townsquare_id)

        return await self.question_repository.create(new_question=new_question, author=author, townsquare=townsquare)

    async def get_question_via_id(self, question_id: str) -> Question:
        return await self.question_repository.get(question_id)

    async def get_all_questions(self) -> List[Question]:
        return await self.question_repository.get_all()

    async def check_ownership(self, user_id: str, question_id: str) -> bool:
        question: Question = await self.get_question_via_id(question_id)
        author: User = await question.author.single()
        if author.uid != user_id:
            raise PermissionError("You are not the author of this question")
        return True

    async def update_question(self, question_id: UUID, **kwargs) -> Question:
        return await self.question_repository.update(question_id, **kwargs)

    async def delete_question(self, question_id: UUID) -> str:
        return await self.question_repository.delete(question_id)

    async def get_all_claims(self, question_id: str):  # -> List[Claim]:
        raise NotImplementedError("Method not implemented yet")  # TODO


def get_question_service() -> QuestionService:
    return QuestionService(QuestionRepository(), UserRepository(), TownsquareRepository())
