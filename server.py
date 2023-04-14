import socket
import struct
import time

HOST = ('127.0.0.1', 2022)


def get_time_offset():
    with open('time_offset.txt', 'r') as file:
        return int(file.read())


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


if __name__ == "__main__":
    start_server()
