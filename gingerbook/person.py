import uuid


class Person(object):
    __tablename__ = 'people'

    def __init__(self, first_name, last_name, email_addresses, street_addresses, phone_numbers,
                 group_ids, id=None):
        self.id = id or str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email_addresses = email_addresses
        self.street_addresses = street_addresses
        self.phone_numbers = phone_numbers
        self.group_ids = group_ids

    def __repr__(self):
        return "<Person '%s %s'>" % (self.first_name, self.last_name)

    @property
    def data(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email_addresses': self.email_addresses,
            'street_addresses': self.street_addresses,
            'phone_numbers': self.phone_numbers,
            'group_ids': self.group_ids
        }
