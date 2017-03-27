import time
import zmq
import praw

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
reddit = praw.Reddit(client_id='h_P0QRHoG1dhZQ',
                     client_secret='d49gcG3H3uFbQXUKnvGiNE9DesM',
                     password='ramagema',
                     user_agent='testscript by Mark Ramage',
                     username='MarkRamageVanderbilt')
print(reddit.user.me())

while True:
    #wait for next request from client
    message = socket.recv_string()
    print("Recieved request: %s" % message)
    comments = ""
    for comment in reddit.inbox.messages():
        comments += (comment.body.encode("utf-8")) + "\n"
        

    #send replay back to client
    socket.send_string("Hello Client, these are your messages" + comments)


