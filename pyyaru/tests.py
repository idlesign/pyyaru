# -*- coding: utf-8 -*-

"""Юнит тесты для pyyaru."""

import pyyaru
import unittest

resource_uri_me = '/me/'

resource_urn_person = 'urn:ya.ru:person/153990'
resource_url_person = 'https://api-yaru.yandex.ru/person/153990/'
resource_url_persons = 'https://api-yaru.yandex.ru/person/153990/friend/'

resource_urn_entry = 'urn:ya.ru:post/153990/219'
resource_url_entry = 'https://api-yaru.yandex.ru/person/153990/post/219/'

resource_urn_club = 'urn:ya.ru:club/4611686018427391272'
resource_url_club = 'https://api-yaru.yandex.ru/club/4611686018427391272/'
resource_url_clubs = 'https://api-yaru.yandex.ru/person/153990/club/'

class yaPersonCheck(unittest.TestCase):
    
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
        """Загрузка профиля с ресурса /me/. Требует авторизации."""
        person = pyyaru.yaPerson(resource_uri_me).get()
        self.assertNotEqual(person.id, resource_uri_me)
        
    def test_error_typemismatch(self):
        """Крушение в случае несоответствия типа объекта pyyaru."""
        not_a_person = pyyaru.yaPerson(resource_url_entry)
        self.assertRaises(pyyaru.yaObjectTypeMismatchError, not_a_person.get)
        
    def test_links_list_exists(self):
        """Существования списка со ссылками для данного ресурса"""
        person = pyyaru.yaPerson(resource_url_person).get()
        self.assertEqual(person.links.has_key('self'), True)
        

class yaResourceCheck(unittest.TestCase):    
         
    def test_id_without_fails(self):
        """Крушение без указания первого параметра конструктора."""
        self.assertRaises(TypeError, pyyaru.yaResource)
        
    def test_resource_uri_to_url(self):
        """Приведение uri к полному адресу."""
        resource = pyyaru.yaResource(resource_uri_me)
        self.assertEqual(resource.url, pyyaru.API_SERVER+resource_uri_me)
        
    def test_resource_urn_to_url(self):
        """Приведение urn к полному адресу."""
        resource = pyyaru.yaResource(resource_urn_person)
        self.assertEqual(resource.url, '%s/resource?id=%s' % (pyyaru.API_SERVER, resource_urn_person))
        
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