import numpy as np
import tkinter as tk
import random
import time

# ================ 迷宮地圖 ================
maze = np.array([
    [0, 0, -1, 0, 0],
    [0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [1, 0, 1, 1, 0],
    [0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0],
    [0, 0, 1, 1, 1],
    [1, 0, 0, 0, 2]
])  # 5*9

column, row = len(maze)*len(maze[0]), 4  # 9,5
Qtable = np.zeros([column, row])  # Qtable [45][4]


# ================ 走迷宮 ================

def runMaze(Qtable):
    # 找起點
    for x in range(len(maze)):
        for y in range(len(maze[0])):
            if maze[x, y] == -1:
                now = (x+1)*(y+1)-1
                NowX, NowY = x, y

# 定義方向
    actionlist = ["上", "下", "左", "右"]
    actionDict = {"上": -len(maze[0]), "下": len(maze[0]), "左": -1, "右": 1}
    mazeActionDict = {"上": -1, "下": 1, "左": -1, "右": 1}

# ================ 開始走 ================

    fin, step = 0, 0
    eGreddy, alpha, gama = 0.95, 0.7, 0.9
    nextNow, nextNowX, nextNowY = 0, 0, 0
    walkDirNumlist = []  # 放最大分數的重複方向
    while fin == 0:
        if random.random() > eGreddy:  # 隨機選擇路線
            walkdir = random.choice(actionlist)

            walk = actionDict[walkdir]
            for i in range(len(actionlist)):
                if actionlist[i] == walkdir:
                    walkDirNum = i
                    mazewalk = actionlist[walkDirNum]

        else:  # 習慣路線
            maxGrade = np.max(Qtable[now])

            for x in range(len(Qtable[now])):
                if Qtable[now, x] == maxGrade:
                    walkDirNumlist.append(x)

            if len(walkDirNumlist) == 1:  # 唯一最大
                walkDirNum = walkDirNumlist[0]

            else:  # 有多個最大分數
                walkDirNum = random.choice(walkDirNumlist)

            walk = actionDict[actionlist[walkDirNum]]
            mazewalk = actionlist[walkDirNum]


# ================ 判斷方向，並計算下格座標 ================

        nextNow = now + walk  # 下一步座標

        if mazewalk == "上" or mazewalk == "下":
            nextNowX = mazeActionDict[mazewalk]
            nextNowY = 0

        elif mazewalk == "左" or mazewalk == "右":
            nextNowY = mazeActionDict[mazewalk]
            nextNowX = 0

        nextNowX = NowX + nextNowX
        nextNowY = NowY + nextNowY

# ================ 判斷是否能走 ================

        if nextNow >= 0 and nextNow <= 44 and nextNowX >= 0 and nextNowX <= 8 and nextNowY >= 0 and nextNowY <= 4:  # 下一格為牆

            if maze[nextNowX, nextNowY] == 0 or maze[nextNowX, nextNowY] == -1:  # 下一格為路
                maxGrade = np.max(Qtable[nextNow])
                nextReward = alpha*(-1 + (gama*maxGrade) -
                                    Qtable[now, walkDirNum])
                beforeReward = (1-alpha)*Qtable[now, walkDirNum]
                Qtable[now, walkDirNum] = beforeReward + nextReward
                now, NowX, NowY = nextNow, nextNowX, nextNowY

            elif maze[nextNowX, nextNowY] == 1:  # 下一格為牆
                maxGrade = np.max(Qtable[nextNow])
                nextReward = alpha*(-10 + (gama*maxGrade) -
                                    Qtable[now, walkDirNum])
                beforeReward = (1-alpha)*Qtable[now, walkDirNum]
                Qtable[now, walkDirNum] = beforeReward + nextReward

            elif maze[nextNowX, nextNowY] == 2:  # 下一格為終點
                maxGrade = np.max(Qtable[nextNow])
                nextReward = alpha*(100 + (gama*maxGrade) -
                                    Qtable[now, walkDirNum])
                beforeReward = (1-alpha)*Qtable[now, walkDirNum]
                Qtable[now, walkDirNum] = beforeReward + nextReward
                now, NowX, NowY = nextNow, nextNowX, nextNowY
                fin = 1
                print("抵達終點")

        else:
            maxGrade = np.max(Qtable[now])
            nextReward = alpha*(-10 + (gama*maxGrade) -
                                Qtable[now, walkDirNum])
            beforeReward = (1-alpha)*Qtable[now, walkDirNum]
            Qtable[now, walkDirNum] = beforeReward + nextReward

        step += 1

    print("步數:", step)
    return Qtable


# ================ 執行次數 ================

def runTime(Qtable, runlimit):
    run = 0
    while run <= runlimit:
        Qtable = runMaze(Qtable)
        # print("%d. Qtable分數" % run, Qtable)
        run += 1
        # print("第%d版Q:" % i, Qtable)
    return Qtable


# ================ 印出路線圖 main ================

Qtable = runTime(Qtable, 40)
actionlist = ["上", "下", "左", "右"]
print("迷宮:\n", maze)
for x in range(45):
    maxGrade = np.max(Qtable[x])
    for y in range(4):
        if Qtable[x, y] == maxGrade:
            maxY = y
    if x != 0 and (x % 5) == 4:
        print(actionlist[maxY] + "\n", end="")
    else:
        print(actionlist[maxY], end="")
