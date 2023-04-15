# Exact Time Server #
## Задача: ##
_Написать сервер точного времени, который «врет» на заданное в своем конфигурационном файле число секунд. Сервер прослушивает 123 порт UDP. Время сервер узнает
либо у ОС, либо у другого надежного сервера точного времени, например, time.windows.com.
В конфигурационном файле сервера указано, на сколько секунд он должен «врать», т. е. из
точного времени сервер вычитает или прибавляет указанное число секунд._

## Использование: ##
_Для получения времени клиентом, сначала запускаем файл "server.py",
затем запускаем простую реализацию клиента "client.py".
В файле "time_offset.txt" задано время(в секундах) по умолчанию на сколько «врет» 
сервер отправляя нам время_
_Пример результата программы: «Sat Apr 15 01:21:13 2023»_

# Разберём подробно работу: #
+ server.py 

_Функция "get_time_offest()" возвращает время, на которое сервер «врет»_
```python
def get_time_offset():
    with open('time_offset.txt', 'r') as file:
        return int(file.read())
```

_С помощью функции " request_time_from_NtpServer(NTPServer='time.windows.com.') " <br/>
узнаёт время у другого надежного сервера точного времени, а именно  «time.windows.com.» <br/>
запрос на надёжный за счёт пакета NTP UDP. Данное поле данных представляет собой: 0x1B затем 47 раз 0. «\x1b' + 47 * b'\0»_
```python
def request_time_from_NtpServer(NTPServer='time.windows.com.'):
    REF_TIME_1970 = 2208988800
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_server:
        data = b'\x1b' + 47 * b'\0'
        client_server.sendto(data, (NTPServer, 123))
        data, ad = client_server.recvfrom(1024)
        if data:
            t = struct.unpack('!12I', data)[10]
            t -= REF_TIME_1970
        return time.ctime(t + get_time_offset())
```
_Функция " start_server() " непосредственно запускает сам сервер, который будет принимать запросы от пользователей на получение точного времени._
```python
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind(HOST)
        print('Server working...')
        while True:
            data, address = server.recvfrom(1024)
            if data == b'\x1b' + 47 * b'\0':
                data_from_NTP = request_time_from_NtpServer()
                response = bytes(data_from_NTP, 'utf-8')
                server.sendto(response, address)
            else:
                response = bytes('invalid request...', 'utf-8')
                server.sendto(response, address)
```
__Программу написал Матус Матвей (МЕН-210201)__
