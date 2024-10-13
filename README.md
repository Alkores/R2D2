# R2D2
Проект представленный командой R2D2 для окружного хакатона СЗФО.
## Кейс
*Преобразование каталога товаров ОАО «РЖД»*

В связи с необходимостью прогнозирования потребления в закупках и снабжении важно определять характеристики материалов для создания параметрической базы данных о товарах. Участникам необходимо разработать программный модуль для анализа каталога товаров, используемых в ОАО «РЖД», с целью определения ключевых характеристик каждого товара и его классификации. Без метрики и лидерборда.

## Catolog 
Содержит скрипт, который выделяет товар, например "Сорочка мужская..." и разбивает товары с этим наименованием на группы при помощи характеристик. Ниже приведён пример работы кода.
ДО:
![alt text](https://s.iimg.su/s/13/hV5GzUuitSC2ehwiciDu7DVXabAqCqiHErQsVlRl.png)
ПОСЛЕ:
![alt text](https://s.iimg.su/s/13/fZLGTm0CgYGC6elbW3tV0DluzRPen6ItBQQf4KBn.png)


## Corrector
Содержит скрипт с запросами к Gigachat, для корректировки неверно введенных ОКПД2 (для нормализации данных) на основе контекста: Наименование, ГОСТ/ТУ, характеристики. К сожалению, освоить API для корректной работы не вышло. Скрипт возвращает ошибку:
```{bash}<пробел>{Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 169, in _new_conn
    conn = connection.create_connection(
  File "/usr/lib/python3/dist-packages/urllib3/util/connection.py", line 73, in create_connection
    for res in socket.getaddrinfo(host, port, family, socket.SOCK_STREAM):
  File "/usr/lib/python3.10/socket.py", line 955, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
socket.gaierror: [Errno -2] Name or service not known

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 700, in urlopen
    httplib_response = self._make_request(
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 383, in _make_request
    self._validate_conn(conn)
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 1017, in _validate_conn
    conn.connect()
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 353, in connect
    conn = self._new_conn()
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 181, in _new_conn
    raise NewConnectionError(
urllib3.exceptions.NewConnectionError: <urllib3.connection.HTTPSConnection object at 0x7f77019d0940>: Failed to establish a new connection: [Errno -2] Name or service not known

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/requests/adapters.py", line 439, in send
    resp = conn.urlopen(
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 756, in urlopen
    retries = retries.increment(
  File "/usr/lib/python3/dist-packages/urllib3/util/retry.py", line 574, in increment
    raise MaxRetryError(_pool, url, error or ResponseError(cause))
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='api.gigachat.com', port=443): Max retries exceeded with url: /v1/okpd (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f77019d0940>: Failed to establish a new connection: [Errno -2] Name or service not known'))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/sirofim/hack-a-ton/app.py", line 36, in <module>
    new_okpd = get_okpd_from_gigachat(product_name, gost_tu, parameters)
  File "/home/sirofim/hack-a-ton/app.py", line 22, in get_okpd_from_gigachat
    response = requests.post(url, headers=headers, json=payload)
  File "/usr/lib/python3/dist-packages/requests/api.py", line 119, in post
    return request('post', url, data=data, json=json, **kwargs)
  File "/usr/lib/python3/dist-packages/requests/api.py", line 61, in request
    return session.request(method=method, url=url, **kwargs)
  File "/usr/lib/python3/dist-packages/requests/sessions.py", line 544, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/lib/python3/dist-packages/requests/sessions.py", line 657, in send
    r = adapter.send(request, **kwargs)
  File "/usr/lib/python3/dist-packages/requests/adapters.py", line 516, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='api.gigachat.com', port=443): Max retries exceeded with url: /v1/okpd (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f77019d0940>: Failed to establish a new connection: [Errno -2] Name or service not known'))
}
```
## Hakaton - Copy.py
Представляет собой вторую весию каталогизации использующую в качестве индекса OKPD2. Который сам по себе тоже имеет категории.
