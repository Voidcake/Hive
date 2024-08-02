from enum import Enum, auto

from strawberry import enum


class AddressRelationship(Enum):
    ATTACKS = auto()
    SUPPORTS = auto()
    ANSWERS = auto()


AddressRelationshipSchema = enum(AddressRelationship)
