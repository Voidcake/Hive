from neomodel import AsyncStructuredNode, StringProperty, EmailProperty, UniqueIdProperty


class User(AsyncStructuredNode):
    uid = UniqueIdProperty()
    username = StringProperty(required=True, unique_index=True)
    email = EmailProperty(required=True, unique_index=True)
    password = StringProperty(required=True)
    first_name = StringProperty(required=True)
