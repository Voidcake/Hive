import logging
from typing import List

from neomodel import adb
from neomodel.exceptions import UniqueProperty, DoesNotExist

from src.app.townsquare.townsquare import Townsquare
from src.app.user.user import User
from src.infra.db.crud_repository_interface import ICRUDRepository
from src.infra.db.db_types import GraphDataTypes as types
from src.infra.db.graph_repository_interface import IGraphRepository


class UserRepository(ICRUDRepository, IGraphRepository):

    @staticmethod
    async def create(new_user: User) -> User:
        async with adb.transaction:
            try:
                return await new_user.save()
            except UniqueProperty:
                raise ValueError(f"Username '{new_user.username}' or Email '{new_user.email}' already exists")

    @staticmethod
    async def get(uid: str) -> User:
        user: User = await User.nodes.get_or_none(uid=uid)
        if not user:
            raise LookupError(f"The User with ID '{uid}' not found in the Database")
        return user

    @staticmethod
    async def get_via_username(username: str) -> User:
        user: User = await User.nodes.get_or_none(username=username)
        if not user:
            raise LookupError(f"The User with username '{username}' not found in the Database")
        return user

    @staticmethod
    async def get_all() -> List[User]:
        return await User.nodes.all()

    async def update(self, uid: str, **kwargs) -> User:
        try:
            user: User = await self.get(uid)
            for key, value in kwargs.items():
                if value is not None:
                    old_name = getattr(user, key)
                    setattr(user, key, value)
                    logging.info(f"Updating {key}: '{old_name}' --> '{value}'")

            async with adb.transaction:
                return await user.save()
        except DoesNotExist as e:
            logging.error(f"The User with ID '{uid}' not found in the Database: {str(e)}")
            raise LookupError(f"The User with ID '{uid}' not found in the Database") from e
        except UniqueProperty as e:
            logging.error(
                f"Username '{kwargs.get("username")}' or Email '{kwargs.get("email")}' already exists: {str(e)}")
            raise ValueError(
                f"Username '{kwargs.get("username")}' or Email '{kwargs.get("email")}' already exists: {str(e)}") from e
        except Exception as e:
            logging.error(f"Error updating User with ID '{uid}': {str(e)}")
            raise e

    async def delete(self, uid: str) -> str:
        try:
            user: User = await self.get(uid)
            async with adb.transaction:
                await user.delete()

            logging.info(f"User with ID '{uid}' deleted")
            return f"User with username '{user.username}' deleted"
        except DoesNotExist as e:
            logging.error(f"The User with ID '{uid}' not found in the Database: {str(e)}")
            raise LookupError(f"The User with ID '{uid}' not found in the Database") from e
        except Exception as e:
            logging.error(f"Error deleting User with ID '{uid}': {str(e)}")
            raise e

    # Townsquare Memberships
    async def get_all_townsquare_memberships(self, user_uid: str) -> List[Townsquare]:
        try:
            user: User = await self.get(user_uid)
            return await user.communities.all()
        except Exception as e:
            logging.error(f"Error getting all Townsquare Memberships of User with ID '{user_uid}': {str(e)}")
            raise e

    async def join_townsquare(self, user_uid: str, townsquare_id: str) -> User:
        try:
            user: User = await self.get(user_uid)
            townsquare: Townsquare = await Townsquare.nodes.get_or_none(uid=townsquare_id)
            if not townsquare:
                raise LookupError(f"The Townsquare with ID '{townsquare_id}' not found in the Database")
            async with adb.transaction:
                await user.townsquare_memberships.connect(townsquare)
                return await user.save()
        except DoesNotExist as e:
            logging.error(f"The User with ID '{user_uid}' not found in the Database: {str(e)}")
            raise LookupError(f"The User with ID '{user_uid}' not found in the Database") from e
        except Exception as e:
            logging.error(f"Error joining User with ID '{user_uid}' to Townsquare: {str(e)}")
            raise e

    async def leave_townsquare(self, user_uid: str, townsquare_id: str) -> User:
        try:
            user: User = await self.get(user_uid)
            townsquare: Townsquare = await Townsquare.nodes.get_or_none(uid=townsquare_id)
            if not townsquare:
                raise LookupError(f"The Townsquare with ID '{townsquare_id}' not found in the Database")
            async with adb.transaction:
                await user.townsquare_memberships.disconnect(townsquare)
                return await user.save()
        except DoesNotExist as e:
            logging.error(f"The User with ID '{user_uid}' not found in the Database: {str(e)}")
            raise LookupError(f"The User with ID '{user_uid}' not found in the Database") from e
        except Exception as e:
            logging.error(f"Error leaving User with ID '{user_uid}' from Townsquare: {str(e)}")
            raise e

    # Graph Constraints

    async def add_database_constraints(self, label: str, constraints=None):
        constraints: dict = {
            "node": {
                "uid":             ("unique", "required", types.STRING),
                "username":        ("unique", "required", types.STRING),
                "email":           ("unique", "required", types.STRING),
                "password":        ("required", types.STRING),
                "first_name":      ("required", types.STRING)
            }
        }
        await super().add_database_constraints(label, constraints)

    @staticmethod
    def get_repository() -> 'UserRepository':
        return UserRepository()