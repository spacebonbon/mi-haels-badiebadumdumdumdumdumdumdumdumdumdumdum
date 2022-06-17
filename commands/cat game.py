import os
import random
import asyncio
import time

async def que():
    game = await start()
    print(await mark(game[0], game[1]))

async def start():
    level = random.choice(os.listdir("assets/catgame/levels"))
    file = open("assets/catgame/levels/"+level)
    level = file.read()
    file.close()
    level = level.split("\n")
    for index, row in enumerate(level):
        level[index] = row.split(" ")
    player = None
    enemyList = []
    for i, value in enumerate(level):
        for j, item in enumerate(value):
            level[i][j] = int(item)
            if int(item) == 3:
                player = [i,j]
            if int(item) == 4:
                enemyList.append([i,j, None])
    return level,player,enemyList

async def mark(lvl, goalpos):
    starttime = time.time()
    nummies = []
    nummies.append(goalpos)
    nummer = 1
    while True:
        if time.time() - starttime > 1:
            break
        load = nummies.copy()
        print(nummies)
        nummies = []
        print(load)
        for number in load:
            x = number[0]
            y = number[1]
            if int(lvl[x+1][y]) == 0:
                lvl[x+1][y] = nummer
                nummies.append(lvl[x+1][y])
            if int(lvl[x-1][y]) == 0:
                lvl[x-1][y] = nummer
                nummies.append(lvl[x+1][y])
            if int(lvl[x][y+1]) == 0:
                lvl[x][y+1] = nummer
                nummies.append(lvl[x+1][y])
            if int(lvl[x][y-1]) == 0:
                lvl[x][y-1] = nummer
                nummies.append(lvl[x+1][y])
    lvl[goalpos[0]][goalpos[1]] = 0
    return lvl



asyncio.run(que())