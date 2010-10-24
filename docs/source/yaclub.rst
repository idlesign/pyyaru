Клубы
=====

Класс yaClub описывает ресурс клуба Я.ру.

Получение сведений о клубе
--------------------------

Пробежимся по всем публикациям клуба типа новость (news)::

    club = yaClub(club_url).get()
    club_entries = club.entries('news')
    for entry in club_entries.iter():
        print entry.title

Узнаем, кто состоит в клубе::

    club_members = club.members()
    for member in club_members.iter():
        print entry.name

.. _yaperson-publish_entry:

Опубликуем сообщение в клубе::

    entry = pyyaru.yaEntry(
            attributes={
                'type': 'text',
                'title': 'Сообщение в клубе из pyyaru',
                'content': 'Это сообщение является тестовым.',
            }
            )
    entry = club.publish_entry(entry)

А теперь удалим его за ненадобностью::

    entry.delete()


.. _class-yaclub:

yaClub
------

.. autoclass:: pyyaru.pyyaru.yaClub
    :members:
    :inherited-members:
