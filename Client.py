import socket
from Definitions import *
from Protocol import *

SERVER = "192.168.1.232"
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
isConnected = True
errorOccured = False
error = None
try:
    client.connect(ADDR)
except OSError:
    isConnected = False


def send(typ: RequestType, value=None):
    msg = Request(typ, value)
    message = msg.toByteArray()
    msgLength = str(len(message)).encode(FORMAT)
    if HEADER - len(msgLength) < 0:
        raise ValueError(f"[ERROR] HEADER size too small, increase size of HEADER by {len(msgLength) - HEADER} bytes")
    msgLength += b' ' * (HEADER - len(msgLength))
    client.send(msgLength + message)


def recv():
    returnLength = client.recv(HEADER).decode(FORMAT)
    if returnLength != '':
        return Response.fromByteArray(client.recv(int(returnLength)))
    return Response(404)


def sendAndRecv(typ: RequestType, value=None):
    send(typ, value)
    toReturn = recv()
    if toReturn.isError():
        errorOccured = True
        raise ApplicationError(toReturn)
    return toReturn
