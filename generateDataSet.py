from loadPraw import load
import praw
import xlsxwriter

reddit = load()
subDict = {}
print("reading subreddits")
with open('subredditPlacements.txt', 'r') as fp:
    counter = 0
    for line in fp.readlines():
        info = line.split('\n')[0]
        if counter % 3 == 0:
            sub = info
        elif counter % 3 == 1:
            x = float(info)
        else:
            y = float(info)
            subDict[sub] = [x, y]
        counter += 1

print("getting all users from subreddit")
users = []
for i, sub in enumerate(subDict.keys()):
    print(f'\t{sub}')
    subreddit = reddit.subreddit(f'{sub}')
    userCount = 0
    for submission in subreddit.hot(limit=1):
        for comment in submission.comments:
            if isinstance(comment, praw.models.MoreComments):
                break
            if comment.author not in users:
                userCount += 1
                users.append(comment.author)
            if userCount > 10:
                break

print(f"getting all comments for every user ({len(users)}) found")
data = []
for i, user in enumerate(users):
    try:
        if i % 10 == 0:
            print(f'\t{i}')
        userDict = {}
        userComments = user.comments.hot(limit=25)
        for id in userComments:
            comment = reddit.comment(id=id)
            if comment.subreddit.display_name in userDict:
                userDict[comment.subreddit.display_name] += comment.score
            else:
                userDict[comment.subreddit.display_name] = comment.score
        data.append(userDict)
    except:
        print(f'\terror on user {user}')

print("writing to data.xlsx")
workbook = xlsxwriter.Workbook('data.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write(0, 0, 'x')
worksheet.write(0, 1, 'y')
allSubs = []
i = 2
for userDict in data:
    for sub in list(userDict.keys()):
        if sub not in allSubs:
            allSubs.append(sub)
            worksheet.write(0, i, sub)
            i += 1

for i, userDict in enumerate(data):
    userX = 0
    userY = 0
    totalKarma = 0
    for j, sub in enumerate(allSubs):
        if sub in userDict:
            worksheet.write(i+1, j+2, userDict[sub])
            if sub in subDict:
                userX += subDict[sub][0] * userDict[sub]
                userY += subDict[sub][1] * userDict[sub]
                totalKarma += userDict[sub]
        else:
            worksheet.write(i+1, j+2, 0)
    if totalKarma > 0:
        worksheet.write(i+1, 0, userX / totalKarma)
        worksheet.write(i+1, 1, userY / totalKarma)
    else:
        worksheet.write(i+1, 0, 0)
        worksheet.write(i+1, 1, 0)

workbook.close()
print('done')
