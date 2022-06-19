from concurrent.futures import process
import os
import random
import asyncio
import time
import pdb
import copy

from click import BadParameter 

async def render(board):
    string = ""
    for line in board:
        for item in line:
            add = "  "
            string += str(item)+add[(len(str(item))-1):]
            
        string += "\n"
    return string

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
    return [level,player,enemyList]

async def prep(board):
    for i, row in enumerate(board):
        for j, item in enumerate(row):
            if item == 1:
                board[i][j] = "e"
            else:
                board[i][j] = 0
    return board

async def mark(lvl, goalpos):
    processed = []
    starttime = time.time()
    nummies = []
    nummies.append(goalpos)
    processed.append(goalpos)
    nummer = 1
    while True:
        if nummer > len(lvl)*len(lvl[0]):
            break
        if time.time() - starttime > 1:
            break
        load = nummies.copy()
        nummies = []
        for number in load:
            x = number[0]
            y = number[1]
            if x < len(lvl)-1:
                if lvl[x+1][y] != "e" and [x+1,y] not in processed:
                    lvl[x+1][y] = nummer
                    nummies.append([x+1,y])
                    processed.append([x+1,y])
            
            if x > 0:
                if lvl[x-1][y] != "e" and [x-1,y] not in processed:
                    lvl[x-1][y] = nummer
                    nummies.append([x-1,y])
                    processed.append([x-1,y])
            if y < len(lvl[0])-1:
                if lvl[x][y+1] != "e" and [x,y+1] not in processed:
                    lvl[x][y+1] = nummer
                    nummies.append([x,y+1])
                    processed.append([x,y+1])
            if y > 0:
                if lvl[x][y-1] != "e" and [x,y-1] not in processed:
                    lvl[x][y-1] = nummer
                    nummies.append([x,y-1])
                    processed.append([x,y-1])
        nummer += 1
    return lvl

async def pathgo(board,pos):
    x = pos[0]
    y = pos[1]
    if x > 0:
        if type(board[x-1][y]) != str:
            if board[x-1][y] < board[x][y]:
                return [x-1,y]
    elif y > 0:
        if type(board[x][y-1]) != str:
            if board[x][y-1] < board[x][y]:
                return [x,y-1]
    elif x < len(board) - 1:
        if type(board[x+1][y]) != str:
            if board[x+1][y] < board[x][y]:
                return [x+1,y]
    elif y < len(board[0]) - 1:
        if type(board[x][y+1]) != str:
            if board[x][y+1] < board[x][y]:
                return [x,y+1]
    return [x,y,pos[2]]


async def que():
    game = await start()
    boardd = copy.deepcopy(game)
    boardd = boardd[0]
    level = await prep(game[0].copy())
    print(await render(level))
    level = await mark(level, game[1])
    print(await render(level))
    print(await render(boardd))
    print(game[2][0])
    game[2][0] = await pathgo(level, game[2][0])
    print(game[2][0])

asyncio.run(que())