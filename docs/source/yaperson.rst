Пользователи
============

Класс yaPerson описывает ресурс пользователя Я.ру.

Получение данных пользователя
-----------------------------

Получим данные о себе (с ресурса '/me/')::

    person = pyyaru.yaPerson('/me/').get()

Прочтём некоторые свойства объекта::

    city = person.city  
    name = person.name

А теперь перечислим все свойства::

    for property_name, property_value in person:  
        print '%s = %s' % (property_name, property_value)

Получим ссылку на аватар (userpic) пользователя из словаря ссылок объекта::

    avatar = person.links['userpic']

Сменим себе настроение::

    person.set_status("Yeap, that's me from pyyaru.")

Пробежимся по всем публикациям пользователя типа ссылка (link)::

    person_entries = person.entries('link')
    for entry in person_entries.iter():
        print entry.title

Узнаем, для каких клубов пользователь является модератором::

    moderated_clubs = person.clubs('moderator')
    for club in moderated_clubs.iter():
        print club.name


.. _class-yaperson:

yaPerson
--------

.. autoclass:: pyyaru.pyyaru.yaPerson
    :members:
    :inherited-members:
