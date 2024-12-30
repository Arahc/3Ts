'''
移动相关的库
人物和地图的左右移动（跟随镜头）
人物的跳跃（重力加速度）
与地图块的碰撞检测
'''

import pygame
import sys
from GenMap import GenMap
from GameSettings import *
from Utility import Scene

class MapPage(Scene):

    def __init__(self):
        # 设置人物&运动状态
        self.maper = GenMap()
        self.facing = "right"
        self.frame = 0 # 人物运动到第几帧，一共4帧
        self.leftImage = [pygame.image.load(r".\assets\left1.png"), pygame.image.load(r".\assets\left2.png"), pygame.image.load(r".\assets\left3.png"), pygame.image.load(r".\assets\left4.png")]
        self.rightImage = [pygame.image.load(r".\assets\right1.png"), pygame.image.load(r".\assets\right2.png"), pygame.image.load(r".\assets\right3.png"), pygame.image.load(r".\assets\right4.png")]
        self.edgeDist = MoveSettings.edgeDist
        self.speed = MoveSettings.speed
        self.playerHeight = MoveSettings.playerHeight
        self.playerWidth = MoveSettings.playerWidth
        for i in range(4):
            self.leftImage[i] = pygame.transform.scale(self.leftImage[i], (self.playerWidth, self.playerHeight))
            self.rightImage[i] = pygame.transform.scale(self.rightImage[i], (self.playerWidth, self.playerHeight))
        self.player = self.rightImage[0]
        self.playerRect = self.player.get_rect()

        # 设置地图&碰撞检测
        self.width = WindowSettings.width
        self.height = WindowSettings.height
        self.blockSize = MoveSettings.blockSize
        self.background = pygame.image.load(r".\assets\background.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.myMap = [[None for j in range(self.maper.col)] for i in range(self.maper.row)]
        self.numMap = self.maper.map1
        self.mapRect = [[None for j in range(self.maper.col)] for i in range(self.maper.row)]
        blocks = [r".\assets\air.png", r".\assets\dirt.png", r".\assets\grassland.png", r".\assets\rock.png"]
        self.mapDelta = 0 # 地图移动距离

        for i in range(self.maper.row):
            for j in range(self.maper.col):
                self.myMap[i][j] = pygame.image.load(blocks[self.numMap[i][j]])
                self.myMap[i][j] = pygame.transform.scale(self.myMap[i][j], (self.blockSize, self.blockSize))
                
                # window.blit(self.myMap[i][j], (j * self.blockSize, i * self.blockSize))
                self.mapRect[i][j] = self.myMap[i][j].get_rect()
                self.mapRect[i][j].x = j * self.blockSize
                self.mapRect[i][j].y = i * self.blockSize
        
        # 重力加速度模拟
        self.gravity = MoveSettings.gravity
        self.initialSpeed = MoveSettings.initialSpeed
        self.jumpTime = 0
        self.fallTime = 0
        self.deltaY = 0
        self.onJump = False
        self.falling = False


    '''
    画地图&人物
    '''
    def show(self,window):
        window.blit(self.background, (0, 0))
        for i in range(self.maper.row):
            for j in range(self.maper.col):
                window.blit(self.myMap[i][j], self.mapRect[i][j])
        window.blit(self.player, self.playerRect)

    def handle(self, event):
        # bad code
        # keys = pygame.key.get_pressed()
        # if (keys[pygame.K_a]) or (keys[pygame.K_d]) or (keys[pygame.K_w]):
        #     self.move()
        #     return None
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return 'EnterMenu'

    def move(self):
        # 按键检测
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.tryMoveX(-self.speed)
            if self.facing != "left":
                self.facing = "left"
                self.frame = 0
            else:
                self.frame = (self.frame + 1) % 4
        if keys[pygame.K_d]:
            self.tryMoveX(self.speed)
            if self.facing != "right":
                self.facing = "right"
                self.frame = 0
            else:
                self.frame = (self.frame + 1) % 4
        if keys[pygame.K_w] and self.touchDown():
            self.jumpTime = pygame.time.get_ticks()
            self.tryMoveY(-1)
            self.deltaY = 0
            self.onJump = True
        
        # 考虑重力加速度
        if self.onJump:
            delta = (pygame.time.get_ticks() - self.jumpTime) / 1000
            lastDeltaY = self.deltaY
            self.deltaY = int(-self.initialSpeed * delta + 0.5 * self.gravity * delta * delta)
            self.tryMoveY(self.deltaY - lastDeltaY)
            if self.touchDown():
                self.onJump = False
        
        if self.onJump == False and self.falling == False and self.touchDown() == False:
            self.falling = True
            self.fallTime = pygame.time.get_ticks()
            self.deltaY = 0

        if self.falling:
            delta = (pygame.time.get_ticks() - self.fallTime) / 1000
            lastDeltaY = self.deltaY
            self.deltaY = int(0.5 * self.gravity * delta * delta)
            self.tryMoveY(self.deltaY - lastDeltaY)
            if self.touchDown():
                self.falling = False
        
        # 更新人物显示
        if self.facing == "left":
            self.player = self.leftImage[self.frame]
        else:
            self.player = self.rightImage[self.frame]


    '''
    人物移动 & 地图移动
    '''
    def touchDown(self): # 检测是否接触地面
        for i in range(self.maper.row):
            for j in range(self.maper.col):
                if self.numMap[i][j] != 0 and self.playerRect.colliderect(self.mapRect[i][j]) and self.mapRect[i][j].y >= self.playerRect.y + self.playerHeight - 1:
                    return True
        return False

    def touchUp(self): # 检测是否接触上面
        for i in range(self.maper.row):
            for j in range(self.maper.col):
                if self.numMap[i][j] != 0 and self.playerRect.colliderect(self.mapRect[i][j]) and self.mapRect[i][j].y + self.blockSize - 1 >= self.playerRect.y:
                    return True
        return False

    def touchSide(self): # 检测是否接触左右面
        for i in range(self.maper.row):
            for j in range(self.maper.col):
                if self.numMap[i][j] != 0 and self.playerRect.colliderect(self.mapRect[i][j]) and not self.mapRect[i][j].y >= self.playerRect.y + self.playerHeight - 1:
                    return True
        return False

    def moveMap(self,sgnx):
        if self.mapDelta + sgnx > 0:
            return
        self.mapDelta += sgnx
        for i in range(self.maper.row):
            for j in range(self.maper.col):
                self.mapRect[i][j].x += sgnx

    def tryMoveX(self,dx):
        sgnx = 1 if dx > 0 else -1
        for i in range(abs(dx)):
            if self.playerRect.x + self.playerWidth >= self.width - self.edgeDist and dx > 0:
                self.moveMap(-1)
                if self.touchSide():
                    self.moveMap(1)
            elif self.playerRect.x <= self.edgeDist and dx < 0 and self.mapDelta != 0:
                self.moveMap(1)
                if self.touchSide():
                    self.oveMap(-1)
            else:
                self.playerRect.x += sgnx
                if self.touchSide() or self.playerRect.x < 0:
                    self.playerRect.x -= sgnx
                    break

    def tryMoveY(self,dy):
        sgny = 1 if dy > 0 else -1
        for i in range(abs(dy)):
            self.playerRect.y += sgny
            if self.touchDown():
                break
            elif self.touchUp():
                self.tryMoveY(1)
                self.falling = True
                self.onJump = False
                self.fallTime = pygame.time.get_ticks()
                self.deltaY = 0
                break

    def sinkDown(self):
        while not self.touchDown():
            self.playerRect.y += 1