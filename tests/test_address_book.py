import pytest
from deepdiff import DeepDiff

from gingerbook import GingerBook
from gingerbook.group import Group
from gingerbook.person import Person

from gingerbook.utils import read_data, write_data


def test_initialize_datastore(datastore):
    address_book = GingerBook(datastore=datastore)
    data = read_data(datastore=datastore)
    expected_data = {'groups': [], 'people': []}
    diff = DeepDiff(data, expected_data, ignore_order=True)
    assert not diff, diff


def test_add_group(address_book):
    group = Group(name='foobar')
    address_book.add(group)

    result = address_book.find(Group).all()
    expected_result = [
        address_book.find(Group).filter('id is d083994d-b15f-42cd-b452-3fdbe1863005')[0],
        address_book.find(Group).filter('id is 36029f15-36b1-4f00-be5d-60deb8a96e23')[0],
        address_book.find(Group).filter('id is f87afefb-c0c0-43a6-a7cf-799b3a93b2f9')[0],
        address_book.find(Group).filter('id is {0}'.format(group.id))[0]
    ]
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_add_person(address_book):
    person = Person(
        first_name='Winston',
        last_name='Smith',
        email_addresses=['w@smith.pty'],
        street_addresses=['Outer Party 000'],
        phone_numbers=['+11112233'],
        group_ids=['36029f15-36b1-4f00-be5d-60deb8a96e23', 'f87afefb-c0c0-43a6-a7cf-799b3a93b2f9']
    )
    address_book.add(person)

    result = address_book.find(Person).all()
    expected_result = [
        address_book.find(Person).filter('id is c9048052-d5be-44e4-ab40-f915165551e3')[0],
        address_book.find(Person).filter('id is 71c5a95b-e916-4a48-8ce2-7124865896f0')[0],
        address_book.find(Person).filter('id is 476240a3-8655-47c1-902c-8ce0d7a3da4d')[0],
        address_book.find(Person).filter('id is 7b7d9008-fa36-489f-91c2-a7f75f63edce')[0],
        address_book.find(Person).filter('id is 811e5fd1-a067-449b-a169-512622730069')[0],
        address_book.find(Person).filter('id is {0}'.format(person.id))[0]
    ]
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_add_to_empty_address_book(datastore):
    address_book = GingerBook(datastore=datastore)

    group_1 = Group(name='group_1')
    group_2 = Group(name='group_2')
    address_book.add(group_1, group_2)

    person = Person(
        first_name='John',
        last_name='Doe',
        email_addresses=['j@doe.moc', 'john@johns.work'],
        street_addresses=['Elm Street 666', 'Baker Street 221b'],
        phone_numbers=['+31641234567', '+105556789'],
        group_ids=[group_1.id, group_2.id]
    )
    address_book.add(person)

    people = address_book.find(Person).all()
    groups = address_book.find(Group).all()
    for group in group_1, group_2:
        group.member_ids = [person.id]

    groups_diff = DeepDiff(groups, [group_1, group_2], ignore_order=True)
    assert not groups_diff, groups_diff

    people_diff = DeepDiff(people, [person], ignore_order=True)
    assert not people_diff, people_diff

    for group in groups:
        assert group.member_ids == [person.id]


def test_add_person_nonexistent_group_id(address_book):
    person = Person(
        first_name='John',
        last_name='Doe',
        email_addresses=['j@doe.moc', 'john@johns.work'],
        street_addresses=['Elm Street 666', 'Baker Street 221b'],
        phone_numbers=['+31641234567', '+105556789'],
        group_ids=['123qwe']
    )
    with pytest.raises(RuntimeError) as exc_info:
        address_book.add(person)

    assert str(exc_info.value) == 'Group 123qwe not found'


def test_add_multiple(address_book):
    group_1 = Group(name='group_1')
    group_2 = Group(name='group_2')

    person_1 = Person(
        first_name='Winston',
        last_name='Smith',
        email_addresses=['w@smith.pty'],
        street_addresses=['Outer Party 000'],
        phone_numbers=['+11112233'],
        group_ids=['36029f15-36b1-4f00-be5d-60deb8a96e23', 'f87afefb-c0c0-43a6-a7cf-799b3a93b2f9']
    )
    person_2 = Person(
        first_name='Arthur',
        last_name='Leander',
        email_addresses=['a.leander@theater.ny'],
        street_addresses=['5th Avenue'],
        phone_numbers=['+1005551234'],
        group_ids=[]
    )

    address_book.add(group_1, group_2, person_1, person_2)

    g1 = address_book.find(Group).filter('id is {0}'.format(group_1.id))[0]
    g2 = address_book.find(Group).filter('id is {0}'.format(group_2.id))[0]
    p1 = address_book.find(Person).filter('id is {0}'.format(person_1.id))[0]
    p2 = address_book.find(Person).filter('id is {0}'.format(person_2.id))[0]

    assert g1.name == 'group_1'
    assert g2.name == 'group_2'
    assert p1.first_name == 'Winston'
    assert p2.first_name == 'Arthur'
