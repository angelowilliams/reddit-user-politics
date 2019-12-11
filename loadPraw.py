import praw

def load():
    return praw.Reddit(client_id='your_id',
                     client_secret='your_secret',
                     password='your_password',
                     user_agent='script by /u/your_name',
                     username='your_name')
