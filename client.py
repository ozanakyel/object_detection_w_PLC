import socket

HOST = socket.gethostname()  # The server's hostname or IP address
PORT = 65432        # The port used by the server
print("host=",HOST)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        giris=input("giriniz:")
        s.sendall(b'160#125645#123#start#bottle')
        data = s.recv(1024)

        print('Received', repr(data))