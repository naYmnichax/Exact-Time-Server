import socket

host = "127.0.0.1"
port = 2022

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect((host, port))
    s.sendall(b'\x1b' + 47 * b'\0')
    data, address = s.recvfrom(1024)
    print(data.decode())
