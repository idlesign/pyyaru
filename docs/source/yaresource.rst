Абстрактный ресурс
==================

Класс описывает абстрактный ресурс.

Этим классом можно воспользоваться для получения ресурса, тип которого заранее неизвестен. Метод *get_object()* данного класса, в случае удачного свершения, вернёт объект типа соответствующего заявленному ресурсом. Пример::

    yaobj = pyyaru.yaResource(resource_id).get_object()


Класс yaResource
----------------

.. autoclass:: pyyaru.pyyaru.yaResource
    :members:
