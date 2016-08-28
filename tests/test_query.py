import pytest
from deepdiff import DeepDiff

from gingerbook import GingerBook
from gingerbook.group import Group
from gingerbook.person import Person

from gingerbook.utils import read_data, write_data


def test_find_all_groups(address_book, data):
    result = address_book.find(Group).all()
    expected_result = [Group(**group_data) for group_data in data['groups']]
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_find_all_people(address_book, data):
    result = address_book.find(Person).all()
    expected_result = [Person(**person_data) for person_data in data['people']]
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_find_group_by_id(address_book, data):
    result = address_book.find(Group).filter('id is 36029f15-36b1-4f00-be5d-60deb8a96e23')
    expected_result = [
        Group(**group_data) for group_data in data['groups']
        if group_data['id'] == '36029f15-36b1-4f00-be5d-60deb8a96e23'
    ]
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_find_group_by_name_existing(address_book):
    result = address_book.find(Group).filter('name is family')
    expected_result = address_book.find(Group).filter('id is d083994d-b15f-42cd-b452-3fdbe1863005')
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_find_group_by_name_non_existent(address_book):
    result = address_book.find(Group).filter('name is foo')
    expected_result = []
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_find_person_by_id(address_book, data):
    result = address_book.find(Person).filter('id is c9048052-d5be-44e4-ab40-f915165551e3')
    expected_result = [
        Person(**person_data) for person_data in data['people']
        if person_data['id'] == 'c9048052-d5be-44e4-ab40-f915165551e3'
    ]
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_find_person_by_first_name(address_book):
    result = address_book.find(Person).filter('first_name is Alice')
    expected_result = address_book.find(Person).filter('id is 476240a3-8655-47c1-902c-8ce0d7a3da4d')
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_find_person_by_last_name(address_book):
    result = address_book.find(Person).filter('last_name is Baker')
    expected_result = [
        address_book.find(Person).filter('id is 7b7d9008-fa36-489f-91c2-a7f75f63edce')[0],
        address_book.find(Person).filter('id is 811e5fd1-a067-449b-a169-512622730069')[0]
    ]
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_find_person_by_full_name(address_book):
    result = address_book.find(Person).filter('first_name is John', 'last_name is Doe')
    expected_result = address_book.find(Person).filter('id is c9048052-d5be-44e4-ab40-f915165551e3')
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_find_person_multiple_filters_non_existent(address_book):
    result = address_book.find(Person).filter('first_name is John', 'last_name is Baker')
    expected_result = []
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_contains_operator(address_book):
    result = address_book.find(Person).filter('first_name contains J')
    expected_result = [
        address_book.find(Person).filter('id is c9048052-d5be-44e4-ab40-f915165551e3')[0],
        address_book.find(Person).filter('id is 71c5a95b-e916-4a48-8ce2-7124865896f0')[0]
    ]
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_multiple_contains_operators(address_book):
    result = address_book.find(Person).filter('first_name contains o', 'last_name contains e')
    expected_result = address_book.find(Person).filter('id is c9048052-d5be-44e4-ab40-f915165551e3')
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_multiple_contains_operators_non_existent(address_book):
    result = address_book.find(Person).filter('first_name contains J', 'last_name contains x')
    expected_result = []
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_not_operator(address_book):
    result = address_book.find(Person).filter('last_name not Baker')
    expected_result = [
        address_book.find(Person).filter('id is c9048052-d5be-44e4-ab40-f915165551e3')[0],
        address_book.find(Person).filter('id is 71c5a95b-e916-4a48-8ce2-7124865896f0')[0],
        address_book.find(Person).filter('id is 476240a3-8655-47c1-902c-8ce0d7a3da4d')[0]
    ]
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_not_operator_multiple_expressions(address_book):
    result = address_book.find(Person).filter('last_name not Baker', 'first_name not Jane')
    expected_result = [
        address_book.find(Person).filter('id is c9048052-d5be-44e4-ab40-f915165551e3')[0],
        address_book.find(Person).filter('id is 476240a3-8655-47c1-902c-8ce0d7a3da4d')[0]
    ]
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_query_list_field_one_element(address_book):
    result = address_book.find(Person).filter('email_addresses is a@cooper.com')
    expected_result = address_book.find(Person).filter('id is 476240a3-8655-47c1-902c-8ce0d7a3da4d')
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_query_list_field_multiple_elements(address_book):
    result = address_book.find(Person).filter('email_addresses is jdoe@jmail.com')
    expected_result = address_book.find(Person).filter('id is c9048052-d5be-44e4-ab40-f915165551e3')
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_query_list_field_multiple_elements_multiple_expressions(address_book):
    result = address_book.find(Person).filter(
        'email_addresses is jdoe@jmail.com',
        'email_addresses is j@doe.com'
    )
    expected_result = address_book.find(Person).filter('id is c9048052-d5be-44e4-ab40-f915165551e3')
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_query_list_field_multiple_elements_multiple_expressions_with_not(address_book):
    result = address_book.find(Person).filter(
        'email_addresses is jdoe@jmail.com',
        'email_addresses is j@doe.com',
        'email_addresses not jane@roe.com'
    )
    expected_result = address_book.find(Person).filter('id is c9048052-d5be-44e4-ab40-f915165551e3')
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_query_list_field_multiple_elements_multiple_expressions_non_existent(address_book):
    result = address_book.find(Person).filter(
        'email_addresses is jdoe@jmail.com',
        'email_addresses is j@doe.com',
        'email_addresses is foo@bar',
    )
    expected_result = []
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_query_list_field_contains_operator(address_book):
    result = address_book.find(Person).filter('email_addresses contains .com')
    expected_result = [
        address_book.find(Person).filter('id is c9048052-d5be-44e4-ab40-f915165551e3')[0],
        address_book.find(Person).filter('id is 71c5a95b-e916-4a48-8ce2-7124865896f0')[0],
        address_book.find(Person).filter('id is 476240a3-8655-47c1-902c-8ce0d7a3da4d')[0]
    ]
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff


def test_mixed_operators(address_book):
    result = address_book.find(Person).filter(
        'group_ids is 36029f15-36b1-4f00-be5d-60deb8a96e23',
        'phone_numbers not +31621231212',
        'email_addresses contains .com',
    )
    expected_result = [
        address_book.find(Person).filter('id is c9048052-d5be-44e4-ab40-f915165551e3')[0],
        address_book.find(Person).filter('id is 71c5a95b-e916-4a48-8ce2-7124865896f0')[0],
    ]
    diff = DeepDiff(result, expected_result, ignore_order=True)
    assert not diff, diff
