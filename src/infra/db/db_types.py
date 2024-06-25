from enum import Enum, auto


class GraphDataTypes(Enum):
    """
    Types Docs: https://neo4j.com/docs/cypher-manual/current/constraints/examples/#constraints-examples-node-property-type)
    """
    BOOLEAN = auto()
    STRING = auto()
    INTEGER = auto()
    FLOAT = auto()
    DATE = auto()
    LOCAL_TIME = "LOCAL TIME"
    ZONED_TIME = "ZONED TIME"
    LOCAL_DATETIME = "LOCAL DATETIME"
    ZONED_DATETIME = "ZONED DATETIME"
    DURATION = auto()
    POINT = auto()
    LIST_BOOLEAN = "LIST<BOOLEAN NOT NULL>"
    LIST_STRING = "LIST<STRING NOT NULL>"
    LIST_INTEGER = "LIST<INTEGER NOT NULL>"
    LIST_FLOAT = "LIST<FLOAT NOT NULL>"
    LIST_DATE = "LIST<FLOAT NOT NULL>"
    LIST_LOCAL_TIME = "LIST<LOCAL TIME NOT NULL>"
    LIST_ZONED_TIME = "LIST<ZONED TIME NOT NULL>"
    LIST_LOCAL_DATETIME = "LIST<LOCAL DATETIME NOT NULL>"
    LIST_ZONED_DATETIME = "LIST<ZONED DATETIME NOT NULL>"
    LIST_DURATION = "LIST<DURATION NOT NULL>"
    LIST_POINT = "LIST<POINT NOT NULL>"
