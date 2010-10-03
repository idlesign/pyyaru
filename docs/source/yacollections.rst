Ресурсы-коллекции
=================

Ресурсы-коллекции (pyyaru описывает их классами *yaPersons*, *yaClubs*, *yaEntries*, порожденными от *yaCollection*) транслируются в списки объектов соответствующих типов (*yaPerson*, *yaClub*, *Entry*) и хранятся в свойстве '*objects*' объектов-контейнеров.  
Например, обнаружить всех друзей пользователя и вывести их имена можно так::

    friends = pyyaru.yaPersons(person.links['friends']).get()
    for friend in friends.objects:
        print friend.name

А теперь получим названия последних публикаций пользователя::

    my_entries = pyyaru.yaEntries(person.links['posts']).get()
    for entry in my_entries.objects:
        print entry.title

Чтобы упростить доступ к записям пользователей можно воспользоваться методом *entries()* объекта yaPerson::

    my_entries = person.entries('text')

Переданное методу *entries()* значение '*text*' говорит, что мы желаем получить записи только указанного типа (обычные публикации — «мысли»). Если параметр не задан, с ресурса будут запрошены записи всех типов.

Получить публикации друзей поможет метод friends_entries()::

    friends_entries = person.friends_entries('status')

Следует заметить, что одного обращения к ресурсу может оказаться недостаточно, если вложенных объектов много. Для того, чтобы получить следующую порцию необходимо воспользоваться методом *more()* — он запросит с сервера и вернёт очередной набор объектов, при этом дополнив им свойство-список '*objects*' собирательного класса::

    more_entries = my_entries.more()

Для того чтобы пройти по всем существующим вложенным объектам используется метод *iter()*::

    for entry in my_entries.iter():
        print entry.title

Функция *len()*, примененная к объекту-коллекции вернёт количество вложенных объектов, уже полученных с сервера (см. методы *more()* и *iter()*).


.. _class-yaentries:

yaEntries
---------
.. autoclass:: pyyaru.pyyaru.yaEntries
    :members:
    :inherited-members:
    :exclude-members: delete, save

.. _class-yapersons:

yaPersons
---------
.. autoclass:: pyyaru.pyyaru.yaPersons
    :members:
    :inherited-members:
    :exclude-members: delete, save


.. _class-yaclubs:

yaClubs
-------
.. autoclass:: pyyaru.pyyaru.yaClubs
    :members:
    :inherited-members:
    :exclude-members: delete, save
