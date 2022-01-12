import socket
import os


def list_cmd(c):
    directory = os.listdir('./')
    msg = ""
    for i in directory:
        msg = msg + " " + i
    c.send(msg.encode(FORMAT))


def retr_cmd(c, filename):
    file = open('./' + filename, 'r')
    data = file.read()
    c.send(data.encode(FORMAT))


def stor_cmd(c, filename):
    file = open('./{}'.format(filename), 'w')
    data = c.recv(SIZE).decode(FORMAT)
    file.write(data)
    file.close()


s = socket.socket()
print("[CREATED] Socket successfully created.")

PORT = 12345
NUM_CLINETS = 5
FORMAT = 'utf-8'
SIZE = 1024

s.bind(('', PORT))
print("[BINDED] socket binded to %s" % (PORT))

s.listen(NUM_CLINETS)
print("[LISTENING] socket is listening")


while True:

    c, addr = s.accept()
    print('[NEW CONNECTION] Got connection from', addr)
    command = c.recv(SIZE).decode(FORMAT).split()

    if command[0] == 'list':
        print("[LIST] Client {} has asked for a list of files from current directory.".format(addr))
        list_cmd(c)

    elif command[0] == 'RETR':
        print("[RETR {}] Client {} has asked for a file.".format(command[1], addr))
        retr_cmd(c, command[1])

    elif command[0] == 'STOR':
        print("[RETR {}] Client {} wants to store a file.".format(command[1], addr))
        stor_cmd(c, command[1])

    c.close()
