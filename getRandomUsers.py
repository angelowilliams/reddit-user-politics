from loadPraw import load
import praw
import pandas
from model import createModels

data = pandas.read_excel('data.xlsx')
allSubs = list(data.columns)[2:]
reddit = load()

print("getting all users from subreddit")
users = []
subreddit = reddit.subreddit(f'politics')
for submission in subreddit.hot(limit=1):
    for comment in submission.comments:
        if isinstance(comment, praw.models.MoreComments):
            break
        if comment.author not in users:
            users.append(comment.author)

print(f"getting all comments for every user ({len(users)}) found")
data = []
for i, user in enumerate(users):
    try:
        if i % 10 == 0:
            print(f'\t{i}')

        userDict = {}
        userComments = user.comments.hot(limit=15)
        for id in userComments:
            comment = reddit.comment(id=id)
            if comment.subreddit.display_name in allSubs:
                if comment.subreddit.display_name in userDict:
                    userDict[comment.subreddit.display_name] += comment.score
                else:
                    userDict[comment.subreddit.display_name] = comment.score
        dataRow = []
        for sub in allSubs:
            if sub in userDict:
                dataRow.append(userDict[sub])
            else:
                dataRow.append(0)
        data.append(dataRow)
    except:
        print(f'\terror on user {user}')

xModel, yModel = createModels()
xPred = xModel.predict(data)
yPred = yModel.predict(data)

with open('predictions.txt', 'w+') as fp:
    for i in range(len(xPred)):
        fp.write(f'{xPred[i]} {yPred[i]}\n')
