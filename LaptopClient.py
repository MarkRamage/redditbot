import zmq

context = zmq.Context()

# socket talks to server

print("Connecting to hello world Server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://10.68.0.61:5555")

input_message = input("Enter a word to be sent: ")

print("Sending request)
socket.send_string("Hello Server" + input_message)
# get reply
message = socket.recv_string()
print("Received comments:" message)


