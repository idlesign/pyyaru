# -*- coding: utf-8 -*-

"""Юнит тесты для pyyaru."""

import pyyaru
import unittest

resource_uri = '/me/'
resource_urn_person = 'urn:ya.ru:person/153990'
resource_url_person = 'https://api-yaru.yandex.ru/person/153990/'
resource_urn_entry = 'urn:ya.ru:post/153990/219'
resource_url_entry = 'https://api-yaru.yandex.ru/person/153990/post/219/'
resource_urn_club = 'urn:ya.ru:club/4611686018427391272'
resource_url_club = 'https://api-yaru.yandex.ru/club/4611686018427391272/'

class yaPersonCheck(unittest.TestCase):
    
    def test_id_isset(self):
        """Запись первого параметра конструктора в свойство id."""
        resource = pyyaru.yaPerson(resource_urn_person)
        self.assertEqual(resource.id, resource_urn_person)
        
    def test_id_without_fails(self):
        """Крушение без указания первого параметра конструктора."""
        self.assertRaises(TypeError, pyyaru.yaPerson)
        
    def test_lazy_load_on_attrib_access(self):
        """Автоматическое наполнение объекта при обращении к
        отсутствующему свойству."""
        person = pyyaru.yaPerson(resource_url_person)
        b = person.city
        self.assertEqual(person.id, resource_urn_person)
        

class yaResourceCheck(unittest.TestCase):    
         
    def test_id_without_fails(self):
        """Крушение без указания первого параметра конструктора."""
        self.assertRaises(TypeError, pyyaru.yaResource)
        
    def test_resource_uri_to_url(self):
        """Приведение uri к полному адресу."""
        resource = pyyaru.yaResource(resource_uri)
        self.assertEqual(resource.url, resource.API_SERVER+resource_uri)
        
    def test_resource_urn_to_url(self):
        """Приведение urn к полному адресу."""
        resource = pyyaru.yaResource(resource_urn_person)
        self.assertEqual(resource.url, '%s/resource?id=%s' % (resource.API_SERVER, resource_urn_person))
        
    def test_resource_url_to_url(self):
        """Приведение url к себе самому."""
        resource = pyyaru.yaResource(resource_url_person)
        self.assertEqual(resource.url, resource_url_person)
        
    def test_resource_get_object_person(self):
        """Возвращение с ресурса объекта yaPerson."""
        resource = pyyaru.yaResource(resource_url_person).get_object()
        self.assertEqual(resource.__class__.__name__, 'yaPerson')

    def test_resource_get_object_entry(self):
        """Возвращение с ресурса объекта yaEntry."""
        resource = pyyaru.yaResource(resource_url_entry).get_object()
        self.assertEqual(resource.__class__.__name__, 'yaEntry')

    def test_resource_get_object_club(self):
        """Возвращение с ресурса объекта yaClub."""
        resource = pyyaru.yaResource(resource_url_club).get_object()
        self.assertEqual(resource.__class__.__name__, 'yaClub')


if __name__ == "__main__":
    unittest.main()