import logging
from abc import ABC, abstractmethod

from neomodel import adb

from infra.db.db_types import GraphDataTypes


class IGraphRepository(ABC):

    @abstractmethod
    async def add_database_constraints(self, label: str, constraints: dict = None):
        """
        Add constraints to the graph database for a given node and its relationships
        https://neo4j.com/docs/cypher-manual/current/constraints/

        Constraints are defined as a dictionary with the following structure:
        example_constraints: dict = {
            "node":          {
                "username": ("unique", "required", GraphDataTypes.String),
                "uid":      ("key", GraphDataTypes.Integer | GraphDataTypes.String),
                "email":    ("unique", "required", GraphDataTypes.String),
                "name":     ("required", GraphDataTypes.String),
            },
            "relationships": {
                "relationship_name": {
                    "property1": ("key", "String | Integer"),
                    "property2": ("key", "String"),
                    "property3": ("unique", "required", "String"),
                },
            },
        }
        """

        responses: list[str] = []
        try:
            if "node" in constraints.keys():
                responses.extend(await self._create_db_entity_constraints(constraints["node"], label))
            if "relationships" in constraints.keys():
                for relationship, relationship_constraints in constraints["relationships"].items():
                    responses.append(
                        await self._create_db_entity_constraints(relationship_constraints, label=relationship,
                                                                 relationship=True))

            logging.info(
                f"Constraints for node '{label.capitalize()}' and its associated relationships successfully created")
            return responses

        except Exception as e:
            logging.error(
                f"Error creating constraints for node {label} and its associated relationships: {str(e)}")
            raise

    async def _create_db_entity_constraints(self, constraints: dict, label: str, relationship: bool = False):
        queries: list[str] = []

        for entity_property, property_constraints in constraints.items():
            keys: list[str] = []

            for constraint in property_constraints:
                if not isinstance(constraint, str):
                    constraint = str(constraint.name).lower()

                if relationship:
                    query = f"CREATE CONSTRAINT relationship_{label.lower()}_{entity_property}_is_{constraint} IF NOT EXISTS FOR ()-[e:{label}]-()"
                else:
                    query = f"CREATE CONSTRAINT node_{label.lower()}_{entity_property}_is_{constraint} IF NOT EXISTS FOR (e:{label})"

                constraint = constraint.upper()
                if constraint == "KEY":
                    keys.append(entity_property)
                elif constraint == "UNIQUE":
                    query += f"REQUIRE e.{entity_property} IS UNIQUE "
                elif constraint == "REQUIRED":
                    query += f"REQUIRE e.{entity_property} IS NOT NULL "
                # Type Constraints    
                elif constraint in GraphDataTypes.__members__:
                    query += f"REQUIRE e.{entity_property} IS TYPED {GraphDataTypes[constraint].name} "
                elif "|" in constraint:
                    first_type, second_type = constraint.split("|")
                    query += f"REQUIRE e.{entity_property} IS TYPED {GraphDataTypes[first_type].name} | {GraphDataTypes[second_type].value} "

                queries.append(query)

            if keys:
                if relationship:
                    query = f"CREATE CONSTRAINT {label}_keys IF NOT EXISTS FOR ()-[e:{label}]-()) "
                    query += f"REQUIRE (e.{", e.".join(keys)}) IS RELATIONSHIP KEY"
                else:
                    query = f"CREATE CONSTRAINT {label}_keys IF NOT EXISTS FOR (e:{label}) "
                    query += f"REQUIRE (e.{", e.".join(keys)}) IS NODE KEY"
                queries.append(query)

        try:
            async with adb.transaction:
                for query in queries:
                    response = await adb.cypher_query(query)
                logging.info(
                    f"Constraints for '{label.capitalize()}' successfully created: \n {self.__format_constraints(constraints)}")
                return response

        except Exception as e:
            logging.error(f"Error creating constraints for {label}: {str(e)}")
            raise

    @staticmethod
    def __format_constraints(constraints: dict) -> str:
        formatted_constraints = []
        for property_name, property_constraints in constraints.items():
            formatted_property_constraints = [
                str(constraint.name).lower() if type(constraint) is not str else str(constraint) for constraint in
                property_constraints]
            formatted_constraints.append(f"{property_name}: {formatted_property_constraints}")
        return "\n ".join(formatted_constraints)
