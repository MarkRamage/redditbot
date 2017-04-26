import zmq
import string

context = zmq.Context()

# socket talks to server
def run():
    print("Connecting to hello world Server")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://10.68.0.185:5555")
    running = True
    question = input("Please enter your request for the server: ")
    print("Sending request")
    socket.send_string(question)
    while running:
        # get reply
        print("getting reply")
        message =socket.recv_string()
        if message[0] == "0":
            reply = input(message[1:len(message)]+": ")
            socket.send_string(reply)
        if message[0] == "1":
            message = message[1:len(message)]
            print(message.replace(u"\u2018", "'").replace(u"\u2019", "'"))
            question = input("Please enter your request for the server: ")
            print("Sending request")
            socket.send_string(question)
    

if  __name__ == "__main__":
    run()
    

