import time
import zmq
import praw

try:
    file = open("login.txt", "r")
except IOError:
    print("1: File does not exist")
    
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
reddit = praw.Reddit(client_id=file.readline().rstrip(),
                     client_secret=file.readline().rstrip(),
                     password=file.readline().rstrip(),
                     user_agent=file.readline().rstrip(),
                     username=file.readline().rstrip())
print(reddit.user.me())

def run():
    while True:
        #wait for next request from client
        message = socket.recv_string()
        reply = ""
        if message == "inbox":
            size = 0
            for comment in reddit.inbox.all():
                size=size+1
                
            reply+="0You have " + str(size) + " unread messages. Would you like to read them?"
            answer = askClient(msg = reply)
            while answer not in [1,0]:
                answer = askClient(msg = "0Please answer yes/no")
            if answer == 1:
                reply = "1"
                for comment in reddit.inbox.all():
                    reply += (comment.body) + "\n"
                if size == 0:
                    reply += "No messages"
            if answer == 0:
                reply = "1Thank you"
            if answer == -1:
                reply = "1I didn't understand that"
        elif message == "topics":
            reply += "1Here are the hottest topcs for each of your favorite subbreddits"
            for sub in ['games', 'all', 'askreddit']:
                subreddit = reddit.subreddit(sub)
                reply += "\n\n/r/"+sub
                for topic in subreddit.new(limit = 3):
                    newTopic = "".join([i for i in topic.title if i.isprintable()])
                    reply +="\n    " + newTopic
                    
        else:
        
            reply = "1Please enter any of the following:\ninbox\ntopics"
        

        #send replay back to client
        
        socket.send_string(reply)
    

    
def askClient(msg = "you should not get this"):
    global socket
    socket.send_string(msg)
    #get reply
    reply = socket.recv_string()
    print(reply)
    reply = reply.lower()
    if reply in ['1', 'yes', 'y']:
        return 1
    elif reply in ['0', 'no', 'n']:
        return 0
    else:
        return -1

if  __name__ == "__main__":
    run()
