import os

from .person import Person
from .group import Group
from .query import Query
from .utils import (
    read_data,
    write_data,
    check_group_ids_exist,
    update_group_member_ids_relationship
)


class GingerBook(object):
    entities = (Person, Group)

    def __init__(self, datastore):
        self.datastore = datastore

        if os.path.isfile(self.datastore):
            with open(self.datastore, 'r') as f:
                data = f.read(1)  # 1 byte is enough to see if the datastore is empty
            if not data:
                self._initialize_datastore()
        else:
            self._initialize_datastore()

    def __repr__(self):
        return "<GingerBook '%s>'" % self.datastore

    def add(self, *entities):
        data = read_data(datastore=self.datastore)
        for entity in entities:
            if isinstance(entity, Person) and entity.group_ids:
                check_group_ids_exist(data, entity.group_ids)
                update_group_member_ids_relationship(data, entity.id, *entity.group_ids)

            data[entity.__tablename__].append(entity.data)
        write_data(datastore=self.datastore, data=data)

    def find(self, entity_class):
        return Query(entity_class=entity_class, datastore=self.datastore)

    def _initialize_datastore(self):
        initial_data = {entity.__tablename__: [] for entity in self.entities}
        write_data(datastore=self.datastore, data=initial_data)
