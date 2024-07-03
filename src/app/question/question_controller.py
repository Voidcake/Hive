from typing import List

from strawberry import type, mutation, field, Info

from src.app.question.question_schema import QuestionType, QuestionIn, QuestionUpdateIn
from src.app.question.question_service import QuestionService, get_question_service

question_service: QuestionService = get_question_service()


@type
class QuestionQueries:
    all_questions: List[QuestionType] = field(resolver=question_service.get_all_questions)
    question_by_id: QuestionType | None = field(resolver=question_service.get_question_via_id)
    # all_claims: List[ClaimType] = field(resolver=question_service.get_all_claims) -> TODO


@type
class QuestionMutations:
    @mutation
    async def create_question(self, info: Info, new_question: QuestionIn) -> QuestionType:
        uid: str = await info.context.uid()
        return await question_service.create_question(author_id=uid, title=new_question.title,
                                                      description=new_question.description,
                                                      townsquare_id=new_question.townsquare_id)

    @mutation
    async def update_question(self, info: Info, question_id: str, updated_question: QuestionUpdateIn) -> QuestionType:
        uid: str = await info.context.uid()

        if await question_service.check_ownership(user_id=uid, question_id=question_id):
            return await question_service.update_question(question_id, **vars(updated_question))

    @mutation
    async def delete_question(self, info: Info, question_id: str, confirmation: bool = False) -> str:
        uid: str = await info.context.uid()

        if not confirmation:
            return "Deletion not confirmed"

        if await question_service.check_ownership(user_id=uid, question_id=question_id):
            return await question_service.delete_question(question_id)


@type
class Query:
    @field
    async def questions(self) -> QuestionQueries:
        return QuestionQueries()


@type
class Mutation:
    @field
    async def questions(self) -> QuestionMutations:
        return QuestionMutations()
