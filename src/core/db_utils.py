import os

from neomodel import config, adb
from neomodel.exceptions import NeomodelException

import logging


async def setup_db(database_name: str = "neo4j", test_connection: bool = False, purge_db: bool = False) -> None:
    _configure_neomodel(database_name)
    if test_connection:
        await _test_db_connection()
    if purge_db:
        await _purge_db()


def _configure_neomodel(database: str = "neo4j") -> None:
    url: str = os.getenv("NEO4J_URI")
    username: str = os.getenv("NEO4J_USER")
    password: str = os.getenv("NEO4J_PASSWORD")

    if not url or not username or not password:
        raise ValueError("Database credentials not found in environment variables.")

    config.DATABASE_URL = f"bolt://{username}:{password}@{url}/{database}"
    config.AUTO_INSTALL_LABELS = True

    logging.info(f"Neomodel configured for database: {database}")


async def _test_db_connection():
    try:
        await adb.cypher_query("MATCH (n) RETURN n LIMIT 1")
        logging.info("Database connection successful")
    except NeomodelException as e:
        logging.error(f"Failed to connect to Neo4j database. Error: {str(e)}")


async def _purge_db():
    try:
        async with adb.transaction:
            await adb.cypher_query("MATCH (n) DETACH DELETE n")
            logging.info("Database Emptied.")
    except NeomodelException as e:
        logging.error(f"Failed to purge Neo4j database. Error: {str(e)}")
        raise
