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

.. _yaperson-publish_entry:

Создадим и опубликуем новую запись::

    entry = pyyaru.yaEntry(
            attributes={
                'type': 'text',
                'title': 'Сообщение из pyyaru',
                'content': 'Это сообщение является тестовым.',
                'access': 'private',
            }
            )
    entry = person.publish_entry(entry)

Это сообщение оригинальностью не блещет и никому кроме вас не видно ('access': 'private'), поэтому удалим его за ненадобностью::

    entry.delete()

Пробежимся по всем публикациям пользователя типа ссылка (link)::

    person_entries = person.entries('link')
    for entry in person_entries.iter():
        print entry.title

Узнаем, для каких клубов пользователь является модератором::

    moderated_clubs = person.clubs('moderator')
    for club in moderated_clubs.iter():
        print club.name

Заведём дружбу с пользователем с идентификатором urn:ya.ru:person/153990::

    person.friend('urn:ya.ru:person/153990', 'Я буду дружить с этим человеком.')

А теперь внезапно поссоримся::

    person.unfriend('urn:ya.ru:person/153990', 'А с виду и не скажешь %)')

Запишемся в клуб https://api-yaru.yandex.ru/club/4611686018427439760/::

    person.join_club('https://api-yaru.yandex.ru/club/4611686018427439760/', 'И я с вами!')

Покинем тот же клуб::

    person.leave_club('https://api-yaru.yandex.ru/club/4611686018427439760/', 'У них скучно.')


.. _class-yaperson:

yaPerson
--------

.. autoclass:: pyyaru.pyyaru.yaPerson
    :members:
    :inherited-members:
