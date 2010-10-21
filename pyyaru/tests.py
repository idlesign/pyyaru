# -*- coding: utf-8 -*-

"""Юнит тесты для pyyaru."""

import pyyaru
import unittest
import datetime

resource_uri_me = '/me/'

resource_urn_person = 'urn:ya.ru:person/96845657'
resource_url_person = 'https://api-yaru.yandex.ru/person/96845657/'
resource_url_persons = 'https://api-yaru.yandex.ru/person/96845657/friend/'

resource_urn_entry = 'urn:ya.ru:post/153990/219'
resource_url_entry = 'https://api-yaru.yandex.ru/person/153990/post/219/'
resource_url_entry_imported = 'https://api-yaru.yandex.ru/person/153990/post/2116/'
resource_url_entries = 'https://api-yaru.yandex.ru/person/153990/post/'

resource_urn_club = 'urn:ya.ru:club/4611686018427439760'
resource_url_club = 'https://api-yaru.yandex.ru/club/4611686018427439760/'
resource_url_clubs = 'https://api-yaru.yandex.ru/person/96845657/club/'


class yaPersonCheck(unittest.TestCase):

    def setUp(self):
        self.person = pyyaru.yaPerson(resource_url_person).get()

    def test_geitem(self):
        """Проверка возможности доступа к свойстам объекта в нотации self[key]."""
        self.assertEqual(self.person['id'], 'urn:ya.ru:person/96845657')

    def test_id_isset(self):
        """Запись первого параметра конструктора в свойство id."""
        person = pyyaru.yaPerson(resource_urn_person)
        self.assertEqual(person.id, resource_urn_person)

    def test_id_without_fails(self):
        """Крушение без указания первого параметра конструктора."""
        self.assertRaises(TypeError, pyyaru.yaPerson)

    def test_type(self):
        """Соответствие типа ресура имени класса, заданному строчными буквами без префикса ya."""
        person = pyyaru.yaPerson(resource_urn_person)
        self.assertEqual(person._type, 'person')

    def test_chaining_load(self):
        """Загрузка профиля, используя get() в цепи."""
        person = pyyaru.yaPerson(resource_url_person).get()
        self.assertEqual(person.id, resource_urn_person)

    def test_lazy_load_on_attrib_access(self):
        """Автоматическое наполнение объекта при обращении к отсутствующему свойству."""
        person = pyyaru.yaPerson(resource_url_person)
        city = person.city
        self.assertEqual(person.id, resource_urn_person)

    def test_me_resource(self):
        """Загрузка профиля с ресурса /me/.
        Требует авторизации.

        """
        person = pyyaru.yaPerson(resource_uri_me).get()
        self.assertNotEqual(person.id, resource_uri_me)

    def test_error_typemismatch(self):
        """Крушение в случае несоответствия типа объекта pyyaru."""
        not_a_person = pyyaru.yaPerson(resource_urn_entry)
        self.assertRaises(pyyaru.yaObjectTypeMismatchError, not_a_person.get)

    def test_links_list_exists(self):
        """Существование списка со ссылками для данного ресурса."""
        person = pyyaru.yaPerson(resource_url_person).get()
        self.assertEqual('self' in person.links, True)

    def test_error_rolemismatch(self):
        """Крушение в случае неопознанной роли пользователя в клубе."""
        self.assertRaises(pyyaru.yaPersonInclubRoleUnkwnownError, self.person.clubs, 'mine')

    def test_clubs(self):
        """Получение списка клубов пользователя."""
        clubs = self.person.clubs()
        self.assertNotEqual(len(clubs), 0)

    def test_friends(self):
        """Получение списка друзей пользователя."""
        friends = self.person.friends()
        self.assertNotEqual(len(friends), 0)

    def test_entries(self):
        """Получение списка публикаций пользователя."""
        person_entries = self.person.entries()
        self.assertNotEqual(len(person_entries), 0)

    def test_friends_entries(self):
        """Получение списка публикаций друзей пользователя."""
        person_friends_entries = self.person.friends_entries()
        self.assertNotEqual(len(person_friends_entries), 0)


class yaClubCheck(unittest.TestCase):

    def setUp(self):
        self.club = pyyaru.yaClub(resource_url_club).get()

    def test_entries(self):
        """Получение списка публикаций клуба."""
        club_entries = self.club.entries()
        self.assertNotEqual(len(club_entries), 0)

    def test_members(self):
        """Получение списка членов клуба."""
        club_members = self.club.members()
        self.assertNotEqual(len(club_members), 0)


class yaBaseCheck(unittest.TestCase):

    def test_kwarg_attributes(self):
        """Проверка трансляции аргумента attributes конструктора в свойства объекта."""
        somebase = pyyaru.yaBase('bounce', attributes={'someattr': True})
        self.assertEqual(somebase.someattr, True)


class yaEntryCheck(unittest.TestCase):

    def test_html_escape(self):
        """Проверка исправности эскейпа HTML для помещения в XML."""
        entry = pyyaru.yaEntry()
        self.assertEqual(entry._html_escape('<p>Html Paragraph</p>'), '&lt;p>Html Paragraph&lt;/p>')

    def test_html_unescape(self):
        """Проверка исправности анэскейпа HTML, изымаемого из XML."""
        entry = pyyaru.yaEntry()
        self.assertEqual(entry._html_unescape('&lt;a href="http://somehost.com/?bingo=1&amp;bongo=2">Link&lt;/a>'), '<a href="http://somehost.com/?bingo=1&bongo=2">Link</a>')

    def test_access_property(self):
        """Проверка существования свойства access."""
        entry = pyyaru.yaEntry(resource_url_entry).get()
        self.assertEqual(entry.access, 'public')

    def test_comments_disabled_property(self):
        """Проверка существования свойства comments_disabled."""
        entry = pyyaru.yaEntry(resource_url_entry)
        self.assertEqual(entry.comments_disabled, False)

    def test_type_property(self):
        """Проверка существования свойства type."""
        entry = pyyaru.yaEntry(resource_url_entry)
        self.assertEqual(entry.type, 'text')

    def test_updated_is_datetime(self):
        """Проверка соответствия свойства updated типу datetime.datetime."""
        entry = pyyaru.yaEntry(resource_url_entry).get()
        self.assertEqual(isinstance(entry.updated, datetime.datetime), True)

    def test_original_property(self):
        """Проверка свойства original для импортированных постов."""
        entry = pyyaru.yaEntry(resource_url_entry_imported).get()
        self.assertEqual(entry.original, 'http://twitter.com/idlesign/statuses/20237021892')

    def test_original_property_is_none(self):
        """Проверка original is None для неимпортированных постов."""
        entry = pyyaru.yaEntry(resource_url_entry).get()
        self.assertEqual(entry.original, None)

    def test_object_to_str(self):
        """Проверка возвращения методом __str__ строки."""
        entry = pyyaru.yaEntry()
        self.assertEqual(str(entry), 'None')

    def test_kwarg_attributes_wrong(self):
        """Крушение при передаче ошибочного значения в аргументе attributes конструктора."""
        self.assertRaises(pyyaru.yaEntryAccessUnknownError, pyyaru.yaEntry, attributes={'access': 'me-and-my-kitten'})

    def test_init_properties(self):
        """Проверка инициализации свойств несвязанного объекта."""
        entry = pyyaru.yaEntry()
        self.assertEqual(entry.access, 'private')
        self.assertEqual(entry.comments_disabled, False)
        self.assertEqual(entry.type, 'text')

    def test_create_delete(self):
        """Проверка создания и удаления публикации.
        Требует авторизации.

        """
        me = pyyaru.yaPerson(resource_uri_me).get()
        entry = pyyaru.yaEntry(
            attributes={
                'type': 'text',
                'title': 'Тестовый заголовок из pyyaru',
                'content': 'Это сообщение является тестовым.',
                'access': 'private',
                'comments_disabled': True,
            }
            ).save(me.links['posts'])
        self.assertNotEqual(entry.id, None)
        entry.delete()
        self.assertEqual(entry.id, None)


class yaCollectionCheck(unittest.TestCase):

    def test_save_unsupported(self):
        """Крушение при вызове метода save."""
        collection = pyyaru.yaCollection('bounce')
        self.assertRaises(pyyaru.yaUnsupportedMethodError, collection.save)

    def test_delete_unsupported(self):
        """Крушение при вызове метода delete."""
        collection = pyyaru.yaCollection('bounce')
        self.assertRaises(pyyaru.yaUnsupportedMethodError, collection.delete)


class yaClubsCheck(unittest.TestCase):

    def test_objects_spawn(self):
        """Создание объектов класса yaClub для элементов списка clubs."""
        clubs = pyyaru.yaClubs(resource_url_clubs).get()
        self.assertNotEqual(len(clubs.objects), 0)


class yaPersonsCheck(unittest.TestCase):

    def test_objects_spawn(self):
        """Создание объектов класса yaPerson для элементов списка person."""
        persons = pyyaru.yaPersons(resource_url_persons).get()
        self.assertNotEqual(len(persons.objects), 0)


class yaEntriesCheck(unittest.TestCase):

    def test_objects_spawn(self):
        """Создание объектов класса yaEntry для элементов списка публикаций."""
        entries = pyyaru.yaEntries(resource_url_entries).get()
        self.assertNotEqual(len(entries.objects), 0)

    def test_method_more(self):
        """Проверка работы метода more()."""
        entries = pyyaru.yaEntries(resource_url_entries)
        self.assertEqual(entries.more(), False)  # на несвязанном объекте
        entries.get()
        self.assertNotEqual(entries.more(), False)  # на связанном объекте

    def test_method_iter(self):
        """Проверка работы метода iter()."""
        entries = pyyaru.yaEntries(resource_url_entries)
        for entry in entries.iter():
            self.assertEqual(entry.__class__.__name__, 'yaEntry')
            break


class yaResourceCheck(unittest.TestCase):

    def test_id_without_fails(self):
        """Крушение без указания первого параметра конструктора."""
        self.assertRaises(TypeError, pyyaru.yaResource)

    def test_resource_uri_to_url(self):
        """Приведение uri к полному адресу."""
        resource = pyyaru.yaResource(resource_uri_me)
        self.assertEqual(resource.url, pyyaru.API_SERVER + resource_uri_me)

    def test_resource_urn_to_url(self):
        """Приведение urn к полному адресу."""
        resource = pyyaru.yaResource(resource_urn_person)
        self.assertEqual(resource.url, '%s/resource/?id=%s' % (pyyaru.API_SERVER, resource_urn_person))

    def test_resource_url_to_url(self):
        """Приведение url к себе самому."""
        resource = pyyaru.yaResource(resource_url_person)
        self.assertEqual(resource.url, resource_url_person)

    def test_resource_get_object_person(self):
        """Возвращение с ресурса объекта yaPerson."""
        resource = pyyaru.yaResource(resource_url_person).get_object()
        self.assertEqual(resource.__class__.__name__, 'yaPerson')

    def test_resource_get_object_persons(self):
        """Возвращение с ресурса объекта yaPersons."""
        resource = pyyaru.yaResource(resource_url_persons).get_object()
        self.assertEqual(resource.__class__.__name__, 'yaPersons')

    def test_resource_get_object_entry(self):
        """Возвращение с ресурса объекта yaEntry."""
        resource = pyyaru.yaResource(resource_url_entry).get_object()
        self.assertEqual(resource.__class__.__name__, 'yaEntry')

    def test_resource_get_object_club(self):
        """Возвращение с ресурса объекта yaClub."""
        resource = pyyaru.yaResource(resource_url_club).get_object()
        self.assertEqual(resource.__class__.__name__, 'yaClub')

    def test_resource_get_object_clubs(self):
        """Возвращение с ресурса объекта yaClubs."""
        resource = pyyaru.yaResource(resource_url_clubs).get_object()
        self.assertEqual(resource.__class__.__name__, 'yaClubs')


if __name__ == "__main__":
    unittest.main()
