# -*- coding: utf-8 -*-

"""pyyaru реализует Python-интерфейс к API блог-сервиса Я.ру http://wow.ya.ru."""

import logging
import os
from urllib2 import urlopen, Request, URLError
from lxml import etree
from __init__ import VERSION

LOG_LEVEL = logging.ERROR

API_SERVER = 'https://api-yaru.yandex.ru'

URN_PREFIX = 'urn:ya.ru:'

# Соотнонения URN-типов и объектов
URN_TYPES = {
    'person': 'yaPerson',
    'persons': 'yaPersons',
    'entry': 'yaEntry',
    'club': 'yaClub',
    'clubs': 'yaClubs',
   }

NAMESPACES = { 
    'a': 'http://www.w3.org/2005/Atom', 
    'y': 'yandex:data', 
}

ACCESS_TOKEN = None

# Если в директории бибилиотеки лежит файл token, то берем реквизиты из него
token_filepath = '%s/token' % os.path.dirname(os.path.realpath(__file__))
if os.path.exists(token_filepath):
    token_file = open(token_filepath, 'rb')
    token = eval(token_file.read())
    if isinstance(token, dict):
        ACCESS_TOKEN = token['access_token']
    token_file.close()
     

logging.basicConfig(level=LOG_LEVEL, format="** %(asctime)s - %(name)s - %(levelname)s\n%(message)s\n")


class yaError(Exception):
    """Базовый класс ошибок модуля."""
    pass


class yaObjectTypeMismatchError(yaError):
    """Ошибка несоответствия класса pyyaru типу данных, заявленному ресурсом."""
    pass


class Logger(object):
    """Класс логирования."""
    
    def __init__(self):
        self._logger = None
    
    def __get__(self, instance, owner):
        if self._logger is None:
            self._logger = logging.getLogger(owner.__module__ + "." + owner.__name__)
            
        return self._logger


class yaBase(object):
    """Класс, осуществляющий базовое представляющий ресурса Я.ру в виде объека pyyaru."""
    
    __logger = Logger()
    
    def __init__(self, id, lazy=False):
        self.__parsed = False
        self.id = id
        if lazy:
            self.get()
    
    def __getattr__(self, name):
        """При обращении к любому из свойств объекта, в случае, если данные
        еще не были загружены с ресурса,
        
        """ 
        if self.__parsed == False:
            self.get()
    
        try:
            return self.__dict__[name]
        except KeyError as e:
            raise AttributeError(e)
    
    def __str__(self):
        """Трансляцией объекта в строку является идентификатор объекта."""
        return self.id
    
    def __iter__(self):
        """Реализует возможность прохода по всем свойствам объекта в
        конструкции for key, value in ...
        Вернет кортеж, где первый элемент является именем свойства класса,
        а второй значением свойства.
        
        """
        for attribute in self.__dict__:
            if not attribute.startswith('_'):
                yield (attribute, self.__dict__[attribute])
                
    def _parse(self, resource_data):
        """Запускает механизм парсинга xml, полученного с ресурса.
        Дерево xml транслирует в свойства объекта.
        
        """
        root = etree.fromstring(resource_data[1])
        for attrib in self.__parse_recursion(root):
            self.__dict__[attrib.keys()[0]] = attrib.values()[0]
        
        self.__dict__['links'] = {}
        for link in root.xpath('//a:link | //y:link', namespaces=NAMESPACES):
            self.__dict__['links'][link.attrib['rel']] = link.attrib['href']
            
        self.__parsed = True
     
    def __parse_recursion(self, root, usedict=None):
        """Итератор, проходящий по xml дереву и составляющий списки,
        которые в последстии станут свойствами объекта.
        Выбрасывает пары ключ-значение.
        
        """
        for el in root:
            tagname = el.tag.replace('{%s}' % el.nsmap[None], '')
            
            if tagname != 'link':
                if len(el) > 0:
                    usedict = []
                    for subel in self.__parse_recursion(el, usedict):
                        usedict.append(subel)
                    tagcontent = usedict    
                else:
                    tagcontent = el.text
                
                if isinstance(tagcontent, str):
                    tagcontent = tagcontent.strip()
                    if tagcontent == '':
                        tagcontent = None
                
                yield {tagname: tagcontent}

    @property
    def _type(self):
        """Свойство тип ресурса."""
        return self.__class__.__name__.lstrip('ya').lower()
        
    def get(self):
        """Запрашивает объект с сервера и направляет его в парсер."""
        resource_data = yaResource(self.id).get()
        if resource_data is not None:
            if resource_data[0] == self._type:
                self._parse(resource_data)
            else:
                raise yaObjectTypeMismatchError('Data type "%s" defined by resource mismatches pyyaru object "%s"' 
                       % (resource_data[0], self.__class__.__name__) )
        return self


class yaPerson(yaBase):
    """Класс описывает ресурс пользователя Я.ру (профиль)."""

    def rename(self, new_name):
        """Смена имени пользователя. Под капотом происходит создание
        новой записи типа 'rename'.
        
        """
        raise NotImplementedError('This one is not yet implemented.')
    
    def set_status(self, status):
        """Смена настроения. Под капотом происходит создание
        новой записи типа 'status'.
        
        """
        raise NotImplementedError('This one is not yet implemented.')
    
    def friend(self):
        """Подружиться. Под капотом происходит создание
        новой записи типа 'friend'.
        
        """
        raise NotImplementedError('This one is not yet implemented.')
    
    def unfriend(self):
        """Раздружиться. Под капотом происходит создание
        новой записи типа 'unfriend'.
        
        """
        raise NotImplementedError('This one is not yet implemented.')


class yaPersons(yaBase):
    """Класс описывает ресурс списка пользователий (н.п. список друзей)."""


class yaClub(yaBase):
    """Класс описывает ресурс клуба."""
    
    def add_news(self, news_text):
        """Публикация новости клуба. Под капотом происходит создание
        новой записи типа 'news'.
        
        """
        raise NotImplementedError('This one is not yet implemented.')
    
    def set_rules(self, rules):
        """Публикация правил клуба. Под капотом происходит создание
        новой записи типа 'rules'.
        
        """
        raise NotImplementedError('This one is not yet implemented.')
    
    def join(self):
        """Вступление в клуб. Под капотом происходит создание
        новой записи типа 'join'.
        
        """
        raise NotImplementedError('This one is not yet implemented.')
    
    def leave(self):
        """Уход из клуба. Под капотом происходит создание
        новой записи типа 'unjoin'.
        
        """
        raise NotImplementedError('This one is not yet implemented.')


class yaClubs(yaBase):
    """Класс описывает ресурс списка клубов (н.п. те, в которых состоит пользователь."""


class yaEntry(yaBase):
    """Класс описывает ресурс сообщения (публикации)."""
    
    TYPES = [
        # Записи
        'link',             # Ссылка
        'text',             # Текст
        'complaint',        # Жалоба
        'photo',            # Фото
        'video',            # Видео
        'poll',             # Опрос
        'wishlist',         # Желание
        'congratulation',   # Поздравление
        # Яндекс.Ответы
        'question',         # Задать вопрос
        'answer',           # Ответить на вопрос
        # Друзья
        'friend',           # Подружиться
        'unfriend',         # Раздружиться
        # Яндекс.Маркет
        'model_grade',      # Оценка товара
        'model_opinion',    # Отзыв о товаре
        'shop_grade',       # Оценка магазина 
        'shop_opinion',     # Отзыв о магазине
        # Пользователь
        'status',           # Изменить настроение
        'userpic',          # Аватар
        'rename',           # Изменить имя
        # Клуб
        'news',             # Новость
        'rules',            # Правила
        'join',             # Присоединиться к клубу
        'unjoin',           # Уйти из клуба
        # Прочее
        'activity_fotki',   # Не используется
        'activity_video',   # Не используется
        'description',      #
        'offline',          # Не используется. Куда все идут.
        'opinion',          # 
        'premoderated',     #
        ]

       
class yaResource(object):
    """Класс получает абстрактный ресурс Я.ру и/или создает на его основе объект pyyaru."""
    
    __logger = Logger()
    
    def __init__(self, resource_name):
        """Получая на вход имя ресура, определяет для него подхоящий URL.
        
        Понимает следующие виды имён:
        1. Полноценный URL (н.п. https://api-yaru.yandex.ru/person/153990/)
        2. ya-идентификатор (н.п. urn:ya.ru:person/153990)
        3. URI (н.п. /me/)
        
        """
        self.__logger.debug('Resource defined as "%s".' % resource_name)
        
        resource_name = resource_name.lstrip('/')
        url = resource_name
        if not resource_name.startswith(API_SERVER):
            if resource_name.startswith(URN_PREFIX):
                url = '%s/resource?id=%s' % (API_SERVER, resource_name)
            else:
                url = '%s/%s' % (API_SERVER, resource_name)
                
        self.url = url
        
    def __open_url(self, url, data=None):
        """Открывает URL, опционально используя токен авторизации.
        
        Реализована упрощенная схема, без взаимодействия с OAuth-сервером.
        Для аутентификации необходимо задать ACCESS_TOKEN равным токену, 
        полученному на странице
        https://oauth.yandex.ru/authorize?client_id=25df5dd8e3064e188fbbf56f7c667d5f&response_type=code
        Внимание: для получения токена по приведенному ниже адресу 
        необходимо быть авторизованным на Яндексе.
        
        Полученный файл (token) можно положить рядом с pyyaru.py, в таком случае 
        реквизиты будут взяты из него автоматически.
        
        """
        headers = { 'User-Agent': 'pyyaru %s' % '.'.join(map(str, VERSION)) }
        if ACCESS_TOKEN is not None:
            headers.update({ 'Authorization': 'OAuth '+ACCESS_TOKEN })
        
        self.__logger.info('Opening URL "%s" with "%s"...' %(url, headers)) 
        
        urlobj = None
        try:
            urlobj = urlopen(Request(url, data=data, headers=headers))
        except URLError as e:
            self.__logger.error(' Failed to open "%s".\n Error: "%s"' % (url, e))
        
        self.urlobj = urlobj 
        
    def get(self):
        """Забирает данные с URL.
        Вернёт кортеж из типа ресурса и полученных с него данных.
        
        """
        self.__open_url(self.url)
        if self.urlobj is not None:
            urlobj_data = self.urlobj.read()
            self.__logger.info('Returned URL: %s' % (self.urlobj.geturl()))
            self.__logger.debug('Response Headers:\n%s\n%s%s' % ('-----'*4, self.urlobj.info(), '____'*25))
            self.__logger.debug('Response Body:\n%s\n%s%s' % ('-----'*4, urlobj_data, '____'*25) )
            
            resource_type = self.urlobj.info().getparam('type')
            
            # API багфикс
            if resource_type == 'blog':
                resource_type = 'person'

            return (resource_type, urlobj_data)
        else:
            return None
    
    def get_object(self):
        """Забирает данные с ресура и по возможности преобразует ресурс
        в подходящий ya-объект.
        
        """
        obj = None
        resource_data = self.get()
        
        if resource_data is not None:
            resource_type = resource_data[0]
            
            if resource_type in URN_TYPES.keys():
                self.__logger.debug('Resource type "%s" is a valid resource. Now spawning the appropriate object "%s".' % (resource_type, URN_TYPES[resource_type]))
                obj = globals()[URN_TYPES[resource_type]](None)
                obj._parse(resource_data)
            elif resource_type == None:
                self.__logger.warning('Resource type is none')
            else:
                self.__logger.error('Resource type "%s" is unknown' % resource_type)
            
        return obj
                
    def set(self, data=None):
        """Отсылает данные на URL."""
        
        raise NotImplementedError('This one is not yet implemented.')