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


.. _class-yaperson:

yaPerson
--------

.. autoclass:: pyyaru.pyyaru.yaPerson
    :members:
    :inherited-members:
