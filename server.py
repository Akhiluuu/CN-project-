import socket
import threading
import ssl

HEADER=64
PORT=12345
SERVER="192.168.228.219"  ##socket.gethostbyname(socket.gethostname()) 
ADDR =(SERVER,PORT)
FORMAT="utf-8"
DISCONNECT="!DISCONNECT"

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile='server-cert.pem', keyfile='server-key.pem')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn_ssl = ssl_context.wrap_socket(conn, server_side=True)
    connected=True
    while connected:
        msg_length=conn_ssl.recv(HEADER).decode(FORMAT)
        conn_ssl.send(("recieved").encode(FORMAT))
        if msg_length:
            msg_length=int(msg_length)
            msg=conn_ssl.recv(msg_length).decode(FORMAT)
            if(msg==DISCONNECT):
                connected=False
        print(f"[{addr}] {msg}")
        conn_ssl.send(("recieved").encode(FORMAT))
    ##conn.close()

def start():
    server.listen()
    print(f"[LISTENING]Server is listening on {SERVER}")
    while True:
        conn,addr=server.accept()
        thread=threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")

print("[STARTING] server is starting")
start()