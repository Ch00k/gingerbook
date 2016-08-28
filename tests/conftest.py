import pytest

from gingerbook import GingerBook

from gingerbook.utils import write_data


@pytest.fixture
def datastore(tmpdir):
    return tmpdir.join('ab.json').strpath


@pytest.fixture
def data():
    return {
        'groups': [
            {
                'id': 'd083994d-b15f-42cd-b452-3fdbe1863005',
                'name': 'family',
                'member_ids': [
                    '476240a3-8655-47c1-902c-8ce0d7a3da4d',
                    '7b7d9008-fa36-489f-91c2-a7f75f63edce'
                ]
            },
            {
                'id': '36029f15-36b1-4f00-be5d-60deb8a96e23',
                'name': 'work',
                'member_ids': [
                    'c9048052-d5be-44e4-ab40-f915165551e3',
                    '71c5a95b-e916-4a48-8ce2-7124865896f0'
                ]
            },
            {
                'id': 'f87afefb-c0c0-43a6-a7cf-799b3a93b2f9',
                'name': 'friends',
                'member_ids': ['c9048052-d5be-44e4-ab40-f915165551e3']
            }
        ],
        'people': [
            {
                'id': 'c9048052-d5be-44e4-ab40-f915165551e3',
                'first_name': 'John',
                'last_name': 'Doe',
                'email_addresses': [
                    'j@doe.com',
                    'john@work.net',
                    'jdoe@jmail.com'
                ],
                'street_addresses': [
                    'Elm Street 666',
                    'Baker Street 221b'
                ],
                'phone_numbers': [
                    '+31641234567',
                    '+380676743412'
                ],
                'group_ids': [
                    '36029f15-36b1-4f00-be5d-60deb8a96e23',
                    'f87afefb-c0c0-43a6-a7cf-799b3a93b2f9'
                ],
            },
            {
                'id': '71c5a95b-e916-4a48-8ce2-7124865896f0',
                'first_name': 'Jane',
                'last_name': 'Roe',
                'email_addresses': [
                    'j@roe.com',
                    'jane@work.net'
                ],
                'street_addresses': ['Oak Street 777'],
                'phone_numbers': [
                    '+31659873412',
                    '+380501231212'
                ],
                'group_ids': ['36029f15-36b1-4f00-be5d-60deb8a96e23'],
            },
            {
                'id': '476240a3-8655-47c1-902c-8ce0d7a3da4d',
                'first_name': 'Alice',
                'last_name': 'Cooper',
                'email_addresses': ['a@cooper.com'],
                'street_addresses': ['Furnier Street 48'],
                'phone_numbers': ['+31621231212'],
                'group_ids': ['d083994d-b15f-42cd-b452-3fdbe1863005'],
            },
            {
                'id': '7b7d9008-fa36-489f-91c2-a7f75f63edce',
                'first_name': 'Mary',
                'last_name': 'Baker',
                'email_addresses': ['mary@bak.er'],
                'street_addresses': ['Lost Street 111'],
                'phone_numbers': ['+31620989898'],
                'group_ids': ['d083994d-b15f-42cd-b452-3fdbe1863005']
            },
            {
                'id': '811e5fd1-a067-449b-a169-512622730069',
                'first_name': 'Mike',
                'last_name': 'Baker',
                'email_addresses': ['mike@bak.er'],
                'street_addresses': ['Lost Street 111'],
                'phone_numbers': ['+31620989897'],
                'group_ids': ['d083994d-b15f-42cd-b452-3fdbe1863005']
            }
        ]
    }


@pytest.fixture
def address_book(datastore, data):
    address_book = GingerBook(datastore)
    write_data(datastore=datastore, data=data)
    return address_book
