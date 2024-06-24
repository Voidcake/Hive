import logging

from dotenv import load_dotenv

from core.db_utils import setup_db


async def configure_app():
    load_dotenv()
    configure_logger()
    await setup_db(test_connection=True)


def configure_logger(level=logging.INFO):
    logging.basicConfig(level=level, format='%(levelname)s - %(asctime)s  - %(message)s', datefmt='%H:%M:%S')
    logging.getLogger('passlib').setLevel(logging.ERROR)
