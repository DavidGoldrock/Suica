import socket
import threading
from os import system

import Protocol
from Protocol import RequestType
import GameThread
import Definitions
from types import NoneType

# green terminal:
system('color a')

# create socket
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, Definitions.PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
# global variables
playerCount = 0


def sendMessage(code: int, conn: socket.socket, value=None, ShouldPrint=False):
    msg = Protocol.Response(code, value)
    if ShouldPrint:
        msg.print(True)
    message = msg.toByteArray()  # turn to bytes
    # send length of message in header bytes
    msgLength = str(len(message)).encode(Definitions.FORMAT)
    msgLength += b' ' * (Definitions.HEADER - len(msgLength))
    if len(msgLength) > Definitions.HEADER:
        raise Exception("Header Size Overrun")
    conn.send(msgLength + message)


def handleClient(conn):
    global playerCount
    print(f"[CONNECT]{conn.getpeername()}")
    connected = True
    gameThread = None
    Cardinality = None
    while connected:
        # get Message from user
        msgLength = conn.recv(Definitions.HEADER).decode(Definitions.FORMAT)
        if msgLength:
            msgLength = int(msgLength)
            msg = Protocol.Request.fromByteArray(conn.recv(msgLength))  # receive number of bytes told by user
            # act in different ways depending on the request type
            match msg.RequestType:
                # adds a ball from user in position x
                case RequestType.ADD_BALL:
                    gameThread.gameVars.generateNewFruit(msg.value["x"], msg.value["Cardinality"], msg.value["nextFruitType"])
                # creates a new game with name and password
                case RequestType.CREATE_GAME:
                    if msg.value is not None:
                        key = Definitions.randStr(64)
                        gameThread = GameThread.GameThread(Definitions.Game(), Definitions.Connected(True, False), key)
                        gameThread.start()
                        Definitions.games[key] = {"thread": gameThread, "name": msg.value["name"],
                                                  "password": msg.value["password"]}
                        print(f"[Game Added] {msg.value}")
                        Cardinality = 0
                        print(f"[Player Dict Updated]")
                        sendMessage(200, conn, Cardinality)
                    else:
                        sendMessage(402, conn)
                # joins gae wih password and name
                # if name isn't found it sends 403
                # if passwords don't match it sends 401
                # if server crashed due to internal error it sends 500
                # if all is well it sends 200 with the Cardinality of the user (0 if first user, 1 if second)
                case RequestType.JOIN_GAME:
                    # has the game been found in games
                    found = False
                    for g in Definitions.games.values():
                        if g is not None and g is not NoneType:
                            try:
                                if g["name"] == msg.value["name"]:
                                    found = True
                                    print(F"[FOUND GAME] {g['name']}")
                                    # TODO add check that the game isn't already filled
                                    if g["password"] is None or g["password"] == NoneType or g["password"] == "" or g[
                                        "password"] == msg.value["password"]:
                                        print(f"[PASSWORD] {msg.value['password']} is correct")
                                        gameThread = g["thread"]
                                        Cardinality = 1
                                        gameThread.connected.connected2 = True
                                        sendMessage(200, conn, Cardinality)
                                    else:
                                        print(f"[PASSWORD] {msg.value['password']} is incorrect. correct password is {g['password']}")
                                        sendMessage(401, conn)
                                    break
                            except KeyError:
                                sendMessage(500, conn)
                                continue
                    if not found:
                        print(f"[JOIN GAME FAILED] for name {g['name']}")
                        sendMessage(403, conn)
                # sends current game vars
                case RequestType.GET_GAME_VARS:
                    sendMessage(200, conn, value=gameThread.gameVars)
                # returns the games currently active
                # if one of the game is broken and has no name, sends 500
                case RequestType.RETRIEVE_GAMES:
                    try:
                        sendMessage(200, conn, value=[i["name"] for i in Definitions.games.values()])
                    except KeyError:
                        sendMessage(500, conn)
                        continue
                # disconnects from server
                case RequestType.DISCONNECT:
                    connected = False
                    playerCount -= 1
                    if Cardinality == 0:
                        gameThread.connected.connected1 = False
                    # if not gameThread.connected.connected2:
                    #     gameThread.connected.quit = True
                    else:
                        gameThread.connected.connected2 = False
                    # if not gameThread.connected.connected1:
                    #     gameThread.connected.quit = True
                    print(f"[DISCONNECT]{conn.getpeername()}")
                    print(f"[STATUS] Number of active users:{playerCount}")
                case other_message:
                    sendMessage(400, conn)
                    print(f"[UNEXPECTED REQUEST] type:{other_message} value: {msg.value}")


def start():
    global playerCount
    while True:
        server.listen()
        conn = server.accept()[0]
        thread = threading.Thread(target=handleClient, args=(conn,), daemon=True)
        thread.start()
        playerCount += 1
        print(f"[STATUS] Number of active users:{playerCount}")


def debugPrinting():
    pass


if __name__ == "__main__":
    t = threading.Thread(target=debugPrinting, daemon=True)
    t.start()
    print(f"[STARTING] SERVER: {SERVER} PORT: {Definitions.PORT}")
    start()
