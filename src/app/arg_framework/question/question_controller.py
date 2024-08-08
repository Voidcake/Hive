from typing import List
from uuid import UUID

from strawberry import type, mutation, field, Info

from src.app.arg_framework.question.question import Question
from src.app.arg_framework.question.question_schema import QuestionType, QuestionIn, QuestionUpdateIn
from src.app.arg_framework.question.question_service import QuestionService, get_question_service

question_service: QuestionService = get_question_service()


@type
class QuestionQueries:
    @field
    async def all_questions(self) -> List[QuestionType]:
        question_nodes: List[Question] = await question_service.get_all_questions()
        return [QuestionType.from_node(question_node) for question_node in question_nodes]

    @field
    async def question_by_id(self, question_id: UUID) -> QuestionType:
        question_node: Question = await question_service.get_question(question_id)
        return QuestionType.from_node(question_node)


@type
class QuestionMutations:
    @mutation
    async def create_question(self, info: Info, new_question: QuestionIn) -> QuestionType:
        uid: UUID = await info.context.uid()
        question = await question_service.create_question(author_id=uid, question=new_question.question,
                                                          description=new_question.description,
                                                          townsquare_id=new_question.townsquare_id,
                                                          addressed_node_id=new_question.addressed_node_id)
        return QuestionType.from_node(question)

    @mutation
    async def update_question(self, info: Info, question_id: UUID, updated_question: QuestionUpdateIn) -> QuestionType:
        uid: UUID = await info.context.uid()

        if await question_service.check_ownership(user_id=uid, question_id=question_id):
            question = await question_service.update_question(question_id, **vars(updated_question))
            return QuestionType.from_node(question)

    @mutation
    async def delete_question(self, info: Info, question_id: UUID, confirmation: bool = False) -> str:
        if not confirmation:
            return "Confirmation required before deleting Question"

        uid: UUID = await info.context.uid()

        if await question_service.check_ownership(user_id=uid, question_id=question_id):
            return await question_service.delete_question(question_id)


@type
class Query:
    @field
    async def question(self) -> QuestionQueries:
        return QuestionQueries()


@type
class Mutation:
    @field
    async def question(self) -> QuestionMutations:
        return QuestionMutations()
