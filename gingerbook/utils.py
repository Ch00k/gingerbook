import json


def read_data(datastore):
    with open(datastore, 'r') as f:
        return json.loads(f.read())


def write_data(datastore, data):
    with open(datastore, 'w') as f:
        f.write(json.dumps(data))


def update_group_member_ids_relationship(data, person_id, *group_ids):
    for group in data['groups']:
        if group['id'] in group_ids:
            group['member_ids'].append(person_id)
    return data

def check_group_ids_exist(data, group_ids):
    existing_group_ids = [group['id'] for group in data['groups']]
    for group_id in group_ids:
        if group_id not in existing_group_ids:
            raise RuntimeError("Group {0} not found".format(group_id))
