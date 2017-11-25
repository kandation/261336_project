import socket

from testing_drop import wsthread, user


class WebSockConnect():
    uid = 0
    users = []
    server = 0

    def __int__(self, address, port , connections, server):
        self.server = server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((address, port))
        server.listen(connections)
        while True:
            chanel, detials = server.accept()
            self.uid = self.uid + 1
            self.users.append(user.user(chanel, self.uid))
            wsthread.WebSocketThread(chanel, detials, self).start()