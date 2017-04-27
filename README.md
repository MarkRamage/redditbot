This consists of two programs, a client that can be run on any system, and a server.

To run the server, supply a login.txt file with the username, password, secret, user agent, and statement in the order I have in my example login.txt. After doing this, your bot can login for you and has the following commands.

Inbox, the server will check for any unread messages in your reddit inbox
Subreddit, the server will make additional queries to have you supply a favored subreddit 
SubTopic, the server will add a favored topic to a favored subreddit
Topics, The server will search the favored subreddits for the favored topics, and provide a list of them
SetResponse, specify a subreddit, title, and response. When a topic with that title appears in that subreddit, it will automatically respond.

The client program has been supplied to aid in using this program. Change the IP address to your needs in line 13/
