.. image:: https://travis-ci.org/Ch00k/gingerbook.svg?branch=master
    :target: https://travis-ci.org/Ch00k/gingerbook
    :alt: Travis-CI


gingerbook
==========
gingerbook is a simple address book written in Python. It supports adding people and groups, while also adding people to those groups.

A person can have first name, last name, one or more email addresses, one or more street addresses, one or more phone numbers. A person can be a member of one or more groups.

Installation
------------
::

  pip install gingerbook

or (untill the package is on PyPI)::

	python setup.py install

Usage
-----
To start using gingerbook you first need to create an instance of ``GingerBook`` class passing it a file path that will be used as the datastore. If the file passed does not already exist it will be created

.. code-block:: python

  >>> from gingerbook import GingerBook

  >>> gb = GingerBook('/tmp/gingerbook.db')
  >>> gb
  <GingerBook '/tmp/gingerbook.db'>

Creating entities (groups or people) is done by instantiating a corresponding entity class (``Group`` or ``Person``) and passing the instance (or multiple instances) to ``GingerBook.add``, like this

.. code-block:: python

  >>> from gingerbook.group import Group
  >>> from gingerbook.person import Person

  >>> friends_group = Group(name='friends')
  >>> gb.add(friends_group)

  >>> friend_1 = Person(
  ...     first_name='Arthur',
  ...     last_name='Leander',
  ...     email_addresses=['arthur@leander.com', 'a.leander@elgin.ca'],
  ...     street_addresses=['Thompson Street 11'],
  ...     phone_numbers=['555-11-22', '+120-555-12-12'],
  ...     group_ids=[friends_group.id]
  ... )

  >>> friend_2 = Person(
  ...     first_name='Kirsten',
  ...     last_name='Raymonde',
  ...     email_addresses=['k.raymonde@elgin.ca'],
  ...     street_addresses=['Carroll Str., 123'],
  ...     phone_numbers=['555-99-88'],
  ...     group_ids=[friends_group.id]
  ... )

  >>> gb.add(friend_1, friend_2)

Note that you have to pass group IDs, not group names, as ``group_ids`` argument value.

At this point the address book has one group and two people that belong to this group. To query the address book for entities (groups or people) use ``GingerBook.find``, passing it the class of the entity you want to find. You can then output query results by calling ``all()``

.. code-block:: python

  >>> all_groups = gb.find(Group).all()
  >>> all_groups
  [<Group 'friends'>]

  >>> all_groups[0].name
  friends

  >>> all_people = gb.find(Person).all()
  >>> all_people
  [<Person 'Arthur Leander'>, <Person 'Kirsten Raymonde'>]

  >>> all_people[1].email_addresses
  ['k.raymonde@elgin.ca']

  >>> all_people[1].group_ids
  ['71c5a95b-e916-4a48-8ce2-7124865896f0']

You can as well filter the results by different criteria by calling ``filter()`` in place of ``all()``. The ``filter()`` method accepts one or more expressions that must be of a certain format. If multiple expressions are passed, they are implicitly joined using ``AND`` operator.

The format of the filter expression is ``<entity_field_name> is|not|contains <value>``. Entity field name is the entity class attribute name; operator is one of ``is``, ``not``, ``contains``; value is a string to search for in the entity field value

.. code-block:: python

  >>> gb.find(Person).filter('first_name is Kirsten')
  [<Person 'Kirsten Raymonde'>]

  >>> gb.find(Person).filter('last_name is Leander')
  [<Person 'Arthur Leander'>]

  >>> gb.find(Person).filter('first_name is Arthur', 'last_name is Leander')
  [<Person 'Arthur Leander'>]

  >>> gb.find(Person).filter('email_addresses contains .com')
  [<Person 'Arthur Leander'>]

  >>> gb.find(Person).filter('street_addresses contains Str')
  [<Person 'Arthur Leander'>, <Person 'Kirsten Raymonde'>]

Note that in case of fields that can have multiple values, like ``email_addresses``, ``street_addresses``, ``phone_numbers``, ``group_ids``, the filtering operator is applied to each value in the list individually and the whole expression returns ``True`` if it returns ``True`` for at least one element in the list.

.. code-block:: python

  >>> gb.find(Person).filter('email_addresses is arthur@leander.com')
  [<Person 'Arthur Leander'>]

  >>> gb.find(Person).filter('email_addresses contains k.raymonde')
	[<Person 'Kirsten Raymonde'>]

There also exists a simple back reference from a group to its members. By calling ``Group.member_ids`` you can see all people who belong to this group

.. code-block:: python

  >>> friends = gb.find(Group).filter('name is friends')
  >>> friends
  [<Group 'friends'>]

  >>> friends = friends[0]
  >>> friends.member_ids
  ['c9048052-d5be-44e4-ab40-f915165551e3', '71c5a95b-e916-4a48-8ce2-7124865896f0']

  >>> [ab.find(Person).filter('id is {0}'.format(member_id))[0] for member_id in friends.member_ids]
  [<Person 'Arthur Leander'>, <Person 'Kirsten Raymonde'>]

Running tests
-------------
To run the tests::

	pip install -r dev-requirements.txt
	py.test tests

or (and I'll buy you a beer if you tell me why tox does not work for me: https://gist.github.com/Ch00k/d96111763a92df0d205232ec3c461415)::

	tox
