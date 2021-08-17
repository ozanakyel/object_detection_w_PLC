import cv2
import socket

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("host=",HOST)
    print("port=", PORT)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            print("data=",data)
            string_data= data.decode('utf-8')
            print("string data=",string_data)
            if not data:
                break
            conn.sendall(data)