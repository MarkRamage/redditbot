import time
import zmq
import praw
import pickle

subreddit_topics = {}
delayedRepliesList = []


try:
    with open('topics_list.p', 'rb') as f:
        subreddit_topics = dict(pickle.load(f))
except IOError:
    print("1: File does not exist")
    pickle.dump(subreddit_topics, open('topics_list.p', 'wb'))

try:
    file = open("login.txt", "r")
except IOError:
    print("1: File does not exist")
    
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
socket.RCVTIMEO = 5000 
reddit = praw.Reddit(client_id=file.readline().rstrip(),
                     client_secret=file.readline().rstrip(),
                     password=file.readline().rstrip(),
                     user_agent=file.readline().rstrip(),
                     username=file.readline().rstrip())
print(reddit.user.me())

def run():
    #main while loop of the function
    while True:
        #check to see if we have a response to wait on
        if len(delayedRepliesList) != 0:
            print("checking")
            for response in delayedRepliesList:
                subreddit = reddit.subreddit(response[0])
                for topic in subreddit.new(limit = 25):
                    if response[1] in topic.title:
                        try:
                            topic.reply(response[2])
                            delayedRepliesList.remove(response)
                        except:
                            print("Too soon")
                        
                        break
        #wait for next request from client
        try:
            message =socket.recv_string()
        except zmq.ZMQError as e:
            continue
        reply = ""
        
        
        '''This will read out the unread messages in the users inbox'''
        if message == "Inbox":
            size = 0
            for comment in reddit.inbox.unread():
                size=size+1
                
            reply+="0You have " + str(size) + " unread messages. Would you like to read them?"
            answer = askClient(msg = reply)
            while answer not in [1,0]:
                answer = askClient(msg = "0Please answer yes/no")
            if answer == 1:
                reply = "1"
                for comment in reddit.inbox.unread():
                    reply += (comment.body) + "\n"
                if size == 0:
                    reply += "No messages"
            if answer == 0:
                reply = "1Thank you"
            if answer == -1:
                reply = "1I didn't understand that"
        elif message == "Topics":
            reply += "1Here are all of the watched topics in your favorite subreddits"
            for sub in subreddit_topics:
                subreddit = reddit.subreddit(sub)
                reply += "\n\n/r/"+sub
                for topic in subreddit.new(limit = 25):
                    if any(keyWord in topic.title.lower() for keyWord in subreddit_topics[sub]):
                        newTopic = "".join([i for i in topic.title if i.isprintable()])
                        reply +="\n    " + newTopic
        elif message == "Subreddit":
            reply+="0Here are all of the subreddits you have favorited"
            for sub in subreddit_topics:
                reply+="\n     "+sub
            reply+="\nWould you like to add a new one?"
            answer = askClient(msg = reply)
            while answer not in [1,0]:
                answer = askClient(msg = "0Please answer yes/no")
            if answer == 1:
                newSub = getreplyString(msg = "0What is this subreddit's name?")
                if newSub not in subreddit_topics:
                    subreddit_topics[newSub] = []
                reply = "1Added new subreddit"
                pickle.dump(subreddit_topics, open('topics_list.p', 'wb'))
            if answer == 0:
                reply = "1Thank you"
            if answer == -1:
                reply = "1I didn't understand that"
        elif message == "RemoveSubreddit":
            reply+="0Here are all of the subreddits you have favorited"
            for sub in subreddit_topics:
                reply+="\n     "+sub
            reply+="\nWould you like to remove one?"
            answer = askClient(msg = reply)
            while answer not in [1,0]:
                answer = askClient(msg = "0Please answer yes/no")
            if answer == 1:
                newSub = getreplyString(msg = "0What is this subreddit's name?")
                if newSub in subreddit_topics:
                    del subreddit_topics[newSub]
                reply = "1Added new subreddit"
                pickle.dump(subreddit_topics, open('topics_list.p', 'wb'))
            if answer == 0:
                reply = "1Thank you"
            if answer == -1:
                reply = "1I didn't understand that"
        elif message == "SubTopic":
            reply+="0Here are all of the subreddits you have favorited"
            for sub in subreddit_topics:
                reply+="\n     "+sub
            reply+="\nWould you like to add a new favored topic to one?"
            answer = askClient(msg = reply)
            while answer not in [1,0]:
                answer = askClient(msg = "0Please answer yes/no")
            if answer == 1:
                sub = getreplyString(msg = "0Which Subreddit are you changing?")
                while sub not in subreddit_topics:
                    sub = getreplyString(msg = "0That is not a recognized subreddit, please pick from the list, or add this subreddit")
                reply="0Here is a list of topics being watched in this sub"
                for topic in subreddit_topics[sub]:
                    reply+="\n     "+topic
                reply+="\nWhat new topic should I watch for?"
                print(reply)
                newTopic = getreplyString(msg = reply)
                subreddit_topics[sub].append(newTopic)
                reply = "1Topic Added"
            if answer == 0:
                reply = "1Thank you"
            if answer == -1:
                reply = "1I didn't understand that"
        elif message == "RemoveSubTopic":
            reply+="0Here are all of the subreddits you have favorited"
            for sub in subreddit_topics:
                reply+="\n     "+sub
            reply+="\nWould you like to remove a favored topic in one?"
            answer = askClient(msg = reply)
            while answer not in [1,0]:
                answer = askClient(msg = "0Please answer yes/no")
            if answer == 1:
                sub = getreplyString(msg = "0Which Subreddit are you changing?")
                while sub not in subreddit_topics:
                    sub = getreplyString(msg = "0That is not a recognized subreddit, please pick from the list, or add this subreddit")
                reply="0Here is a list of topics being watched in this sub"
                for topic in subreddit_topics[sub]:
                    reply+="\n     "+topic
                reply+="\nWhat  topic should I remove?"
                print(reply)
                delTopic = getreplyString(msg = reply)
                if delTopic in subreddit_topics[sub]:
                    subreddit_topics[sub].remove(delTopic)
                
                reply = "1Topic deleted"
            if answer == 0:
                reply = "1Thank you"
            if answer == -1:
                reply = "1I didn't understand that"
        elif message == "SetResponse":
            sub = getreplyString(msg = "0Which Subreddit are you setting a response to?") #get subreddit name
            title = getreplyString(msg = "0What is the title, or partial title of this topic you wish to respond too?").lower() #get topic title, does not need to be full title
            response = getreplyString(msg = "2Write your response, use enter as needed. Three blank lines ends the response.") #gets a full reddit comment
            delayedRepliesList.append([sub, title, response]) #adds to list of delayed comments
            reply = "1All set, it will be posted"
        elif message.lower() in ['quit', 'exit', 'q']:
            reply = "#Goodnight"
        else:
        
            reply = "1Please enter any of the following:\nInbox\nTopics\nSubreddit\nRemoveSubreddit\nSubTopic\nRemovenSubTopic"
        #send replay back to client
        socket.send_string(reply)

def askClient(msg = "you should not get this"):
    global socket
    socket.RCVTIMEO = -1 #disable timeout while waiting
    socket.send_string(msg)
    #get reply
    reply = socket.recv_string()
    print(reply)
    reply = reply.lower()
    while reply not in ['1', 'yes', 'y', '0', 'no', 'n']:
        socket.send_string("0Please Enter Yes Or No")
        reply = socket.recv_string()
        reply = reply.lower()
    socket.RCVTIMEO = 5000 
    if reply in ['1', 'yes', 'y']:
        return 1
    elif reply in ['0', 'no', 'n']:
        return 0
    else:
        return -1
def getreplyString(msg = "you should not get this"):
    global socket
    socket.RCVTIMEO = -1 #disable timeout while waiting
    socket.send_string(msg)
    #get reply
    reply = socket.recv_string()
    print(reply)
    reply = reply.lower()
    socket.RCVTIMEO = 5000 
    return reply
if  __name__ == "__main__":
    run()
