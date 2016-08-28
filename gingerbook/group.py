import uuid


class Group(object):
    __tablename__ = 'groups'

    def __init__(self, name, id=None, member_ids=None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.member_ids = member_ids or []

    def __repr__(self):
        return "<Group '%s'>" % self.name

    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'member_ids': self.member_ids
        }
