import pygame
import sys
import Map
from Settings import *

'''
初始化
'''
def init():
    global width, height, playerWidth, playerHeight, blockSize, gravity, initialSpeed, jumpTime, fallTime, deltaY, onJump, falling, background, player, playerRect, myMap, numMap, mapRect, leftImage, rightImage, facing, frame, edgeDist, speed, mapDelta

    # 设置人物&运动状态
    facing = "right"
    frame = 0 # 人物运动到第几帧，一共4帧
    leftImage = [pygame.image.load(r".\assets\left1.png"), pygame.image.load(r".\assets\left2.png"), pygame.image.load(r".\assets\left3.png"), pygame.image.load(r".\assets\left4.png")]
    rightImage = [pygame.image.load(r".\assets\right1.png"), pygame.image.load(r".\assets\right2.png"), pygame.image.load(r".\assets\right3.png"), pygame.image.load(r".\assets\right4.png")]
    edgeDist = WindowSettings.edgeDist
    speed = WindowSettings.speed
    playerHeight = WindowSettings.playerHeight
    playerWidth = WindowSettings.playerWidth
    for i in range(4):
        leftImage[i] = pygame.transform.scale(leftImage[i], (playerWidth, playerHeight))
        rightImage[i] = pygame.transform.scale(rightImage[i], (playerWidth, playerHeight))
    player = rightImage[0]
    playerRect = player.get_rect()

    # 设置地图&碰撞检测
    width = WindowSettings.width
    height = WindowSettings.height
    blockSize = WindowSettings.blockSize
    myMap = [[None for j in range(Map.col)] for i in range(Map.row)]
    numMap = Map.map1
    mapRect = [[None for j in range(Map.col)] for i in range(Map.row)]
    blocks = [r".\assets\air.png", r".\assets\dirt.png", r".\assets\grassland.png", r".\assets\rock.png"]
    mapDelta = 0 # 地图移动距离

    for i in range(Map.row):
        for j in range(Map.col):
            myMap[i][j] = pygame.image.load(blocks[numMap[i][j]])
            myMap[i][j] = pygame.transform.scale(myMap[i][j], (blockSize, blockSize))
            
            # screen.blit(myMap[i][j], (j * blockSize, i * blockSize))
            mapRect[i][j] = myMap[i][j].get_rect()
            mapRect[i][j].x = j * blockSize
            mapRect[i][j].y = i * blockSize
    
    # 重力加速度模拟
    gravity = WindowSettings.gravity
    initialSpeed = WindowSettings.initialSpeed
    jumpTime = 0
    fallTime = 0
    deltaY = 0
    onJump = False
    falling = False


'''
画地图&人物
'''
def draw(screen):
    for i in range(Map.row):
        for j in range(Map.col):
            screen.blit(myMap[i][j], mapRect[i][j])
    screen.blit(player, playerRect)

'''
人物移动 & 地图移动
'''
def touchDown(): # 检测是否接触地面
    for i in range(Map.row):
        for j in range(Map.col):
            if numMap[i][j] != 0 and playerRect.colliderect(mapRect[i][j]) and mapRect[i][j].y >= playerRect.y + playerHeight - 1:
                return True
    return False

def touchUp(): # 检测是否接触上面
    for i in range(Map.row):
        for j in range(Map.col):
            if numMap[i][j] != 0 and playerRect.colliderect(mapRect[i][j]) and mapRect[i][j].y + blockSize - 1 >= playerRect.y:
                return True
    return False

def touchSide(): # 检测是否接触左右面
    for i in range(Map.row):
        for j in range(Map.col):
            if numMap[i][j] != 0 and playerRect.colliderect(mapRect[i][j]) and not mapRect[i][j].y >= playerRect.y + playerHeight - 1:
                return True
    return False

def moveMap(sgnx):
    global mapDelta
    if mapDelta + sgnx > 0:
        return
    mapDelta += sgnx
    for i in range(Map.row):
        for j in range(Map.col):
            mapRect[i][j].x += sgnx

def tryMoveX(dx):
    sgnx = 1 if dx > 0 else -1
    for i in range(abs(dx)):
        if playerRect.x + playerWidth >= width - edgeDist and dx > 0:
            moveMap(-1)
            if touchSide():
                moveMap(1)
        elif playerRect.x <= edgeDist and dx < 0 and mapDelta != 0:
            moveMap(1)
            if touchSide():
                moveMap(-1)
        else:
            playerRect.x += sgnx
            if touchSide() or playerRect.x < 0:
                playerRect.x -= sgnx
                break

def tryMoveY(dy):
    global falling, fallTime, deltaY, onJump
    sgny = 1 if dy > 0 else -1
    for i in range(abs(dy)):
        playerRect.y += sgny
        if touchDown():
            break
        elif touchUp():
            tryMoveY(1)
            falling = True
            onJump = False
            fallTime = pygame.time.get_ticks()
            deltaY = 0
            break

def sinkDown():
    while not touchDown():
        playerRect.y += 1

def move():
    global facing, frame, player, onJump, jumpTime, fallTime, deltaY, falling
    # 按键检测
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        tryMoveX(-speed)
        if facing != "left":
            facing = "left"
            frame = 0
        else:
            frame = (frame + 1) % 4
    if keys[pygame.K_RIGHT]:
        tryMoveX(speed)
        if facing != "right":
            facing = "right"
            frame = 0
        else:
            frame = (frame + 1) % 4
    if keys[pygame.K_UP] and touchDown():
        jumpTime = pygame.time.get_ticks()
        tryMoveY(-1)
        deltaY = 0
        onJump = True
    
    # 考虑重力加速度
    if onJump:
        delta = (pygame.time.get_ticks() - jumpTime) / 1000
        lastDeltaY = deltaY
        deltaY = int(-initialSpeed * delta + 0.5 * gravity * delta * delta)
        tryMoveY(deltaY - lastDeltaY)
        if touchDown():
            onJump = False
    
    if onJump == False and falling == False and touchDown() == False:
        falling = True
        fallTime = pygame.time.get_ticks()
        deltaY = 0

    if falling:
        delta = (pygame.time.get_ticks() - fallTime) / 1000
        lastDeltaY = deltaY
        deltaY = int(0.5 * gravity * delta * delta)
        tryMoveY(deltaY - lastDeltaY)
        if touchDown():
            falling = False
    
    # 更新人物显示
    if facing == "left":
        player = leftImage[frame]
    else:
        player = rightImage[frame]
