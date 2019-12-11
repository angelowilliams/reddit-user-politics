import matplotlib.pyplot as plt
import os

test_file = os.path.join(os.getcwd(), 'subredditPlacements.txt')

subList = []

with open(test_file, 'r') as fp:
    counter = 0
    for line in fp.readlines():
        info = line.split('\n')[0]
        if counter % 3 == 0:
            sub = info
        elif counter % 3 == 1:
            x = float(info)
        else:
            y = float(info)
            subList.append([sub, x, y])
        counter += 1

bg = plt.imread(os.path.join('images', 'compass.png'))

ax = plt.gca()
ax.imshow(bg, zorder=-10, extent=[-10, 10, -10, 10])
for sub in subList:
    plt.scatter(sub[1], sub[2], color='red')
    ax.annotate('r/' + sub[0], (sub[1] - 1, sub[2] + 0.4), size=6)

plt.axis('off')

plt.text(-12.75, -0.5, 'Left', fontsize=14)
plt.text(10.25, -0.5, 'Right', fontsize=14)

plt.text(-4, 11, 'Authoritarian', fontsize=14)
plt.text(-3.5, -11.2, 'Libertarian', fontsize=14)

plt.show()
