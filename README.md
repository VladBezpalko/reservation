# Room reservation app for Light IT portal [![coverage](https://codecov.io/gh/VladBezpalko/reservation/coverage.svg?branch=master)](https://github.com/VladBezpalko/reservation/)

Некоторые имена/ссылки/названия могут быть недостаточно ясны. Могу легко их поменять.

Модель RoomReservation представляет собой запрос пользователя на бронь комнаты. Так же, предполагается, что существует пользователь с правами администратора, у которого есть доступ к списку всех запросов на бронь и подтверждение этих запросов. Если запрос подтвержден - значит комната забронирована пользователем, который отправлял запрос. Подтвердить запрос, временной диапазон которого пересекается с уже подтвержденными запросами невозможно.

Приложение написано так, что бы быть максимально гибким, так как не было четкого ТЗ. В любой момент можно добавить или отключить любой из большого количества написанных валидаторов (проверка на выходные, на рабочие часы, на максимальную\минимальную длительность брони, проверка на минимальное время от создание запроса до времени на которое создается бронь, что бы админ успел проверить и ответить на запрос).

В settings.py можно задать различные параметры - начало/конец рабочего дня, минимальную/максимальную длительность совещания, минимальное время за которое можно запросить бронь, до времени указанного в брони.

На всякий случай был написан небольшой переодичный селери таск, который удаляет старые записи бронирования.

Также написаны тесты. Coverage 100%.

- /reservation/ - основной эндпоинт. Предоставляет CRUD операции для RoomReservation
- /reservation/{id}/reply/ - эндпоинт ответа на запрос. Поддерживает только метод POST. В POST-data нужно отправлять JSON вида {'answer': X}, где X - номер варианта ответа (0 - Запретить, 1 - Разрешить). Возвращает текст ошибки, при попытке подтвердить запрос, временной диапазон которого пересекается с уже подтвержденными запросами. В случае успеха - возвращает обновленный объект резервации.
- /reservation/{id}/overlapping/ - поддерживает только метод GET. Возвращает список объектов резерваций, которые пересекаются с данной. Возвращает тоже самое что и ссылка снизу, только удобнее, так обращение через id.
- /reservation/?start_date__lt={end_date}&end_date__gt={start_date}&answer=1 - возвращает тоже самое что и ссылка выше. (Нет, в ссылке ничего не перепутано)
- /reservation/?start_date__gt={start_day}&end_date__lt={end_day} - таким образом, можно получить список бронирований на определенный день/месяц/что угодно
- /reservation/?creator={user_id} - так можно просмотреть запросы конкретного юзера


TODO:
- Оптимизировать количество фикстур
- Создать отдельную сущность Room, где для каждой комнаты можно будет прописать параметры.
- Возможность создавать расписание для каждой комнаты, с учетом праздников, сокращенных дней и т.п.
- Добавить возможность указывать членов совещания. (Нужно ли?)

