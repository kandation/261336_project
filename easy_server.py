from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import urllib
import iot_server


class WS(WebSocket):
    def handleMessage(self):
        if iot_server.push_data(self.data):
            print("Push OK >> " + str(self.data))
        else:
            print(self.data)
        # echo message back to client
        self.sendMessage(self.data)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


url = "https://gist.githubusercontent.com/kandation/73be69f40ae02471573cc488630614ab/raw/ippop"
with urllib.request.urlopen(url) as response:
    html = response.read()
    html = str(html.decode('ascii')).split(";")
# html = ['', '', '']

print(html)
TCP_IP = str(html[0]) if html[0] != '' else "127.0.0.1"
TCP_PORT = int(html[1]) if html[1] != '' else 9999

server = SimpleWebSocketServer(TCP_IP, TCP_PORT, WS)
server.serveforever()
