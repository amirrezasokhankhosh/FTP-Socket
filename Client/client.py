import socket


def list_cmd(s):
    s.send("list".encode(FORMAT))
    print("[LIST]")
    data = s.recv(SIZE).decode(FORMAT).split()
    print("[LIST RECIEVED]")
    print(data)


def retr_cmd(s, filename):
    s.send("RETR {}".format(filename).encode(FORMAT))
    print("[RETR {}]".format(filename))
    data = s.recv(SIZE).decode(FORMAT)
    print("[DATA RECIEVED]")
    file = open('./{}'.format(filename), 'w')
    file.write(data)
    file.close()


def stor_cmd(s, filename):
    s.send("STOR {}".format(filename).encode(FORMAT))
    print("[STOR {}]".format(filename))
    file = open('./{}'.format(filename), 'r')
    data = file.read()
    s.send(data.encode(FORMAT))
    print("[DATA SENT]")


def stablish_connection(func, filename):
    print("")
    s = socket.socket()
    s.connect((IP, PORT))
    print("[CONNECTED] Clinet is now connected to the server.")
    if func == "list":
        list_cmd(s)
    elif func == "retr":
        retr_cmd(s, filename)
    elif func == "stor":
        stor_cmd(s, filename)
    s.close()
    print("[CONNECTION CLOSED]")
    print("")


PORT = 12345
IP = '127.0.0.1'
FORMAT = 'utf-8'
SIZE = 1024


stablish_connection("list", "")
stablish_connection("retr", "Sepehr.txt")
stablish_connection("stor", "Amirreza.txt")