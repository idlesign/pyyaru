pyyaru
=======================================
[http://github.com/idlesign/pyyaru]()

### Что это? ###

pyyaru — это Python-интерфейс для API блог-сервиса ya.ru.  

* pyayru предназначен для разработчиков.
* pyyaru переплюнул API Я.ру и находится в стадии глубокой альфы.
* pyyaru пока умеет только читать данные с ресурсов Я.ру.


### Зависимости ###

1.  lxml


### Авторизация ###

Для доступа к некотором типам ресурсов Я.ру требуется авторизация.  
На данный момент в pyyaru реализована упрощенная схема, без взаимодействия с OAuth-сервером.

Для аутентификации необходимо задать ACCESS\_TOKEN равным токену, полученному на странице:  
[https://oauth.yandex.ru/authorize?client_id=25df5dd8e3064e188fbbf56f7c667d5f&response_type=code]()  
_Внимание_: для получения токена по приведенному выше адресу необходимо быть авторизованным на Яндексе.

Полученный файл (token) можно положить рядом с pyyaru.py, в таком случае реквизиты будут взяты из него автоматически.


### Объекты pyyaru ###

Ресурсы Я.ру pyyaru представляет в виде объектов.

* класс yaPerson — ресурс пользователя
* класс yaClub — ресурс клуба
* класс yaEntry — ресурс сообщения (публикации)

Объект создается обычным путем:  
    club = pyyaru.yaClub(resource)

Параметром _resource_ в конструктор может быть передано одно из трех значений:

1. Полноценный URL (н.п. https://api-yaru.yandex.ru/person/153990/)
2. ya-идентификатор URN (н.п. urn:ya.ru:person/153990)
3. URI (н.п. /me/)


**Класс yaResource**

Для получения ресурса, тип которого заранее неизвестен, можно воспользоваться классом yaResource метод _get\_object()_ которого, в случае удачного свершения, вернет объект типа соответствующего заявленному ресурсом.

    yaobj = pyyaru.yaResource(unknown_resource_identifier).get_object()


### Примеры использования ###

*Получение данных пользователя Я.ру*

    person = pyyaru.yaPerson(resource).get()

*Чтение свойств пользователя*

    city = person.city  
    name = person.name

*Перечисление свойств*

    for property_name, property_value in person:  
        print '%s = %s' % (property_name, property_value)
