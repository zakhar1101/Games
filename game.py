#!/usr/bin/python 

import random
from random import randint
import os
import copy
import sys
from time import sleep
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame




colorBlack=(0,0,0)
colorWhite=(255,255,255)
lineColor=(0,255,0)




from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE, KEYDOWN,
    QUIT,
)





clear = lambda: os.system('clear')

def edit(cellx, celly, clear, mb, objects):
    pos = pygame.mouse.get_pos()
    x = pos[0]//(cellx)
    y = pos[1]//(celly)
    mb[y][x]=clear
    objects.append((3+pos[0]-(pos[0]%cellx), 3+pos[1]-(pos[1]%celly), cellx-4, celly-4))
    pygame.display.flip()

def drawNotZero(game_map, rows, cols, screen, cellx,celly):
    global colorBlack, colorWhite
    for i in range(0, rows):
        for j in range(0, cols):
            if game_map[i][j]==1:
                pygame.draw.rect(screen, colorBlack, (j*cellx+2, i*celly+2, cellx-4, celly-4))
            else:
                pygame.draw.rect(screen, colorWhite, (j*cellx+2, i*celly+2, cellx-4, celly-4))



def getCoords(mb, mbd, rows, cols, cellx, celly, screen):
    for i in range(0, rows):
        for j in range(0, cols):
            if i==0 and j==0:
                nnc=mb[rows-1][cols-1]+mb[rows-1][j]+mb[rows-1][j+1]+mb[i][rows-1]+mb[i][j+1]+mb[i+1][cols-1]+mb[i+1][j]+mb[i+1][j+1]
            elif i==rows-1 and j==cols-1:
                nnc=mb[i-1][j-1]+mb[i-1][j]+mb[i-1][0]+mb[i][j-1]+mb[i][0]+mb[0][j-1]+mb[0][j]+mb[0][0]
            elif i==rows-1 and j==0:
                nnc=mb[i-1][cols-1]+mb[i-1][j]+mb[i-1][j+1]+mb[i][cols-1]+mb[i][j+1]+mb[0][cols-1]+mb[0][j]+mb[0][j+1]
            elif i==0 and j==cols-1:
                nnc=mb[rows-1][j-1]+mb[rows-1][j]+mb[rows-1][0]+mb[i][j-1]+mb[i][0]+mb[i+1][j-1]+mb[i+1][j]+mb[i+1][0]
            elif i==0:
                nnc=mb[rows-1][j-1]+mb[rows-1][j]+mb[rows-1][j+1]+mb[i][j-1]+mb[i][j+1]+mb[i+1][j-1]+mb[i+1][j]+mb[i+1][j+1]
            elif i==rows-1:
                nnc=mb[i-1][j-1]+mb[i-1][j]+mb[i-1][j+1]+mb[i][j-1]+mb[i][j+1]+mb[0][j-1]+mb[0][j]+mb[0][j+1]
            elif j==0:
                nnc=mb[i-1][cols-1]+mb[i-1][j]+mb[i-1][j+1]+mb[i][cols-1]+mb[i][j+1]+mb[i+1][cols-1]+mb[i+1][j]+mb[i+1][j+1]
            elif j==cols-1:
                nnc=mb[i-1][j-1]+mb[i-1][j]+mb[i-1][0]+mb[i][j-1]+mb[i][0]+mb[i+1][j-1]+mb[i+1][j]+mb[i+1][0]
            else:
                nnc=mb[i-1][j-1]+mb[i-1][j]+mb[i-1][j+1]+mb[i][j-1]+mb[i][j+1]+mb[i+1][j-1]+mb[i+1][j]+mb[i+1][j+1]


            if nnc==3:
                mbd[i][j]=1
                #pygame.draw.rect(screen, colorBlack, (j*cellx+2, i*celly+2, cellx-4, celly-4))
            elif nnc==2:
                mbd[i][j]=mb[i][j]
                #if mbd[i][j]==1:
                #    pygame.draw.rect(screen, colorBlack, (j*cellx+2, i*celly+2, cellx-4, celly-4))
                #else:
                #    pygame.draw.rect(screen, colorWhite, (j*cellx+2, i*celly+2, cellx-4, celly-4))
            else:
                mbd[i][j]=0
                #pygame.draw.rect(screen, colorWhite, (j*cellx+2, i*celly+2, cellx-4, celly-4))
    #map(sum, )
    summ=sum(sum(el) for el in mbd)
    # print(f'sum: {summ}')
    if summ==0:
        global play
        play=False
    
    return mbd


def drawGrid(cols, rows, lineColor, xStep, yStep, height, width, screen, cellx, celly):
    for _ in range(cols):
        pygame.draw.line(screen, lineColor, (xStep, 0), (xStep, height), 1)
        xStep+=celly

    for _ in range(rows):
        pygame.draw.line(screen, lineColor, (0, yStep), (width, yStep), 1)
        yStep+=cellx
            


def run(cols=100, rows=50):
    clock = pygame.time.Clock()



    width = cols*10
    height = rows*10


    mb = [[0]*cols for _ in range(rows)]
    mbd = copy.deepcopy(mb)
    FPS=60

    cellx=width//cols
    celly=height//rows
    objects = []

    pygame.init()

    screen = pygame.display.set_mode([width, height])

    count=0
    running = True
    x = 250
    y = 250
    play= False
    first=True

    try:
        # Тут мы расставляем точки
        while running:
            #print('start ajusting map')
            clock.tick(FPS)
            keys = pygame.key.get_pressed()

            xStep=cellx
            yStep=celly
            screen.fill((255, 255, 255))
            drawGrid(cols, rows, lineColor, xStep, yStep, height, width,screen,cellx,celly)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        play=False
                        objects.clear()
                    #print(pygame.key.name(event.key))

                if event.type == pygame.KEYUP:
                    if event.key==pygame.K_ESCAPE:
                        play=True
                        objects.clear()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play==True: objects.clear()


            if keys[pygame.K_q]:
                # pygame.quit()
                running=False


            if keys[pygame.K_ESCAPE] and pygame.mouse.get_pressed()[0]:
                screen.fill((10, 10, 10))
                print(pygame.mouse.get_pressed())
                drawNotZero(mb,rows,cols,screen,cellx,celly)
                edit(cellx,celly, True,mb,objects)
                continue

            
            if keys[pygame.K_ESCAPE] and pygame.mouse.get_pressed()[2]:
                screen.fill((10, 10, 10))
                print(pygame.mouse.get_pressed())
                drawNotZero(mb,rows,cols,screen,cellx,celly)
                edit(cellx,celly, False,mb,objects)
                continue

        

            # рисует заполненные ячейки
            for item in objects:
                #print(item)
                pygame.draw.rect(screen, colorBlack, item)


            if pygame.mouse.get_pressed()[0]:
                # при нажатии на левую кнопку мыши рисуем чёрным цветом и
                # отрисовываем карту заново т.к. в налале цикла она закрасилась белым
                drawNotZero(mb,rows,cols,screen, cellx, celly)
                edit(cellx,celly, True, mb, objects)
                continue

            if pygame.mouse.get_pressed()[2]:
                # при нажатии на правую кнопку мыши рисуем белым цветом и
                # отрисовываем карту заново т.к. в налале цикла она закрасилась белым
                drawNotZero(mb,rows,cols,screen,cellx,celly)
                edit(cellx,celly, False, mb, objects)
                continue

            if play:
                #print('start game')
                # запускается процесс игры
                xStep=cellx
                yStep=celly

                # print(keys[pygame.K_q])
                mb=copy.deepcopy(getCoords(mb, mbd,rows,cols,cellx,celly,screen))
                drawNotZero(mb,rows,cols,screen,cellx,celly)
                count+=1
                clear()
                print(f'Стадия: {count}')

                pygame.display.flip()
            #sleep(10)
            if first:
                pygame.display.flip()
                first=False

        pygame.quit()

    except KeyboardInterrupt:
        clear()
        print('Выход ок)')


