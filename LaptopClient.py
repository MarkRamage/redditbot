import zmq

context = zmq.Context()

# socket talks to server

print("Connecting to hello world Server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://10.68.0.1:5555")



print("Sending request")
socket.send_string("Hello Server")
# get reply
message ="Received comments:" + socket.recv_string()
print(message.encode('utf-8'))


