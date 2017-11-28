import socket
import hashlib
import base64
import threading
import urllib.request


WS_MAGIC_STRING = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

class server:
    sock = 0

    def __init__(self, ip, port, connections):
        self.sock = MySocket(ip, port, connections, self )

class MyUser:
    user_id = 0
    socket = 0
    handshack = 0

    def __init__(self, socket, user_id):
        self.user_id = user_id
        self.socket = socket


class MySocket:
    uid = 0
    users = []
    server = 0

    def __init__(self, address, port, connections, server):
        self.server = server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((TCP_IP, TCP_PORT))
        server.listen(connections)
        while True:
            channel, detials = server.accept()
            self.uid = self.uid + 1
            self.users.append(MyUser(channel, self.uid))
            WS(channel, detials, self).start()



class WS(threading.Thread):
    def __init__(self, channel, details, websocket):
        self.channel = channel
        self.details = details
        self.websocket = websocket
        threading.Thread.__init__(self)

    def run(self):
        print("Sockey> Received connection ", self.details[0],self.details[1])
        self.hand_shake_connect(self.channel)
        while True:
            # Alway Connection
            self.interact(self.channel)

    def hand_shake_connect(self, channel):
        # self.request is the TCP socket connected to the client
        self.data = channel.recv(1024).strip()
        dd = str(self.data.decode('ascii'))
        headers = dd.split("\r\n")
        print(headers)

        # is it a websocket request?
        if "Connection: Upgrade" in headers and "Upgrade: websocket" in headers:
            # getting the websocket key out
            for h in headers:
                if "Sec-WebSocket-Key" in h:
                    key = h.split(" ")[1]
                    #print(key)
            # let's shake hands shall we?
            self.shake_hand(key, client=channel)
        else:
            channel.sendall(bytes("HTTP/1.1 400 Bad Request\r\n" + \
                                 "Content-Type: text/plain\r\n" + \
                                 "Connection: close\r\n" + \
                                 "\r\n" + \
                                 "Incorrect request", encoding="utf-8"))

    def finduser(self, client):
        for user in self.websocket.users:
            if user.socket == client:
                return user
        return 0

    def interact(self, client):
        users = self.websocket.users
        this_user = self.finduser(client)

        aaa = client.recv(1024).strip()
        try:
            payload = self.decode_frame(bytearray(aaa))
        except:
            print("Frame is Unknow")

        try:
            decoded_payload = payload.decode('utf-8')
            print(decoded_payload)

            # Exit Command
            if "p" == decoded_payload.lower():
                print("Bidding goodbye to our client...", self.details)
                exit(0)
        except:
            print("error Cannot decode, Exit connection")
            exit(0)
        self.send_frame(payload)

    def shake_hand(self,key, client):
        # calculating response as per protocol RFC
        key = key + WS_MAGIC_STRING
        aa = hashlib.sha1(key.encode('ascii')).digest()
        resp_key = base64.standard_b64encode(aa)

        resp = "HTTP/1.1 101 Switching Protocols\r\n" + \
             "Upgrade: websocket\r\n" + \
             "Connection: Upgrade\r\n" + \
             "Sec-WebSocket-Accept: %s\r\n\r\n"%(resp_key.decode('ascii'))
        client.sendall(resp.encode('ascii'))

    def decode_frame(self,frame):
        opcode_and_fin = frame[0]
        # assuming it's masked, hence removing the mask bit(MSB) to get len. also assuming len is <125
        payload_len = frame[1] - 128

        mask = frame [2:6]
        encrypted_payload = frame [6: 6+payload_len]

        payload = bytearray([ encrypted_payload[i] ^ mask[i%4] for i in range(payload_len)])

        return payload

    def send_frame(self, payload):
        # setting fin to 1 and opcpde to 0x1
        frame = [129]
        # adding len. no masking hence not doing +128
        frame += [len(payload)]
        # adding payload
        frame_to_send = bytearray(frame) + payload

        self.channel.sendall(frame_to_send)



if __name__ == "__main__":
    url = "https://gist.githubusercontent.com/kandation/73be69f40ae02471573cc488630614ab/raw/ippop"
    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = str(html.decode('ascii')).split(";")
    html = ['','','']

    print(html)
    TCP_IP =  str(html[0]) if html[0] != '' else "127.0.0.1"
    TCP_PORT = int(html[1]) if html[1] != '' else 9999
    CONNECTIONS = int(html[2]) if html[2] != '' else 100
    web = server(TCP_IP, TCP_PORT, CONNECTIONS)
