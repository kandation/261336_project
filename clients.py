import websocket

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.create_connection("ws://128.199.173.142:9999/ww")
    print("Sending 'Hello, World'...")
    ws.send("Hello, World")
    print("Sent")
    print("Receiving...")
    #result = ws.recv()
    #print("Received '%s'" % result)
ws.close()