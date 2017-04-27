import zmq
import string

#global variables
context = zmq.Context()
socket = context.socket(zmq.REQ)


    
# socket talks to server
def run():
    print("Connecting to hello world Server")
    #socket.connect("tcp://10.68.0.185:5555")
    socket.connect("tcp://localhost:5555")
    socket.RCVTIMEO = 5000 
    running = True
    question = input("Please enter your request for the server: ")
    print("Sending request")
    socket.send_string(question)
    while running:
        # get reply
        print("getting reply")
        try:
            message =socket.recv_string()   #Ever loop starts with this, but if it timesout, we restart the client connection
        except zmq.ZMQError as e:
            print(e)
            print("Server Failed to respond, resetting connection")
            socket_restart() #this function restarts the program
            question = input("Please enter your request for the server: ") #we always need to sends a request before ending the loop, even here.
            print("Sending request")
            socket.send_string(question)
            continue    #restart while loop
            
        #A first character of zero implies that the server has asked a question, and wants a response
        if message[0] == "0":
            reply = input(message[1:len(message)]+": ")
            print("Sending reply: "+reply)
            socket.send_string(reply)
            
        #A first character of 1 says that this is the final message in a text tree
        if message[0] == "1":
            message = message[1:len(message)]
            print(message.replace(u"\u2018", "'").replace(u"\u2019", "'"))
            question = input("Please enter your request for the server: ")
            print("Sending request")
            socket.send_string(question)
            
        #When the first character is 2, then the server expects a full reddit comment
        if message[0] == "2":
            message = message[1:len(message)]
            print(message.replace(u"\u2018", "'").replace(u"\u2019", "'"))
            question =getRedditComment()
            print("Sending request")
            socket.send_string(question)
            
        #This simply closes the program after sending exit, quit, or q
        if message[0] == "#":
            exit()
'''This function gathers and returns a multiline reddit comment. Reddit comments ignore 
the third empty line, so three empty lines have been chosen as the cutoff point'''
def getRedditComment():
    emptyLines = 0
    reply = ""
    while emptyLines<3:
        string = input()
        if len(string) == 0:
            emptyLines = emptyLines+1
        else: #reset empty lines counter
            emptyLines = 0
        reply += string +"\n"
    return reply            

#resets the socket as needed
def socket_restart():
    global socket
    socket.close()
    socket = context.socket(zmq.REQ)
    #socket.connect("tcp://10.68.0.185:5555")
    socket.connect("tcp://localhost:5555")
    socket.RCVTIMEO = 5000

if  __name__ == "__main__":
    run()