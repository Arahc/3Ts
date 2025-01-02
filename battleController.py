import sys
import pygame as pg
import saveSet as svst
import screenPainter as scpt
from cardBattle import cardAttack, TrashCard

gSet = sys.modules['__main__'].__dict__ # global settings
"""
screenHeight: The height of the screen. (px)
screenWidth: The width of the screen. (px)
bg_img_loaction: The location of the background img
"""

selectedCards = set()
hoveredCards = None
selectedFriendCard = None

def rgb(r:int, g:int, b:int):
    return r, g, b

def systemInit():
    gSet['--font-color-light'] = rgb(242, 253, 255)
    gSet['--HP-ground'] = rgb(0, 99, 29)
    gSet['--HP-front'] = rgb(0, 205, 102)
    gSet['--SP-ground'] = rgb(25, 25, 112)
    gSet['--SP-front'] = rgb(65, 105, 225)
    gSet['--SP-third'] = rgb(120, 169, 255)
    gSet['--select-card'] = rgb(252, 243, 207)
    gSet['--selected-card'] = rgb(245, 183, 177)
    gSet['--card-info-ground'] = rgb(31, 30, 51)

def Initialization(screenWidth:int, screenHeight:int, bg_img_loaction:str, fps:int):
    gSet['screenSize'] = screenWidth, screenHeight
    gSet['screenWidth'] = screenWidth
    gSet['screenHeight'] = screenHeight
    gSet['bg_img'] = pg.image.load(bg_img_loaction)
    gSet['fps'] = fps

def mouseSelect(event, friendUnit, enemyUnit):
    global hoveredCards, selectedFriendCard
    if event.type == pg.MOUSEMOTION:
        hoveredCards = None
        mousePos = event.pos
        for card in friendUnit.onHandCards + enemyUnit.onHandCards:
            card_image = pg.image.load(card.imgLocation).convert_alpha()
            card_rect = card_image.get_rect()
            if card in friendUnit.onHandCards:
                card_rect.topleft = (10 + friendUnit.onHandCards.index(card) * (card_image.get_width() + 10), gSet['screenHeight'] - card_image.get_height() - 10)
            else:
                card_rect.topleft = (gSet['screenWidth'] - (enemyUnit.onHandCards.index(card) + 1) * (card_image.get_width() + 10), gSet['screenHeight'] - card_image.get_height() - 10)
            if card_rect.collidepoint(mousePos):
                hoveredCards = card
                break
    elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        if hoveredCards:
            if hoveredCards in selectedCards:
                selectedCards.remove(hoveredCards)
            else:
                if hoveredCards in friendUnit.onHandCards:
                    if friendUnit.SP > 0:
                        if selectedFriendCard is None:
                            selectedFriendCard = hoveredCards
                            selectedCards.add(hoveredCards)
                        elif selectedFriendCard == hoveredCards:
                            selectedFriendCard = None
                            selectedCards.remove(hoveredCards)
                else:
                    selectedCards.add(hoveredCards)
            checkCardSelection(friendUnit, enemyUnit)

def checkCardSelection(friendUnit, enemyUnit):
    global selectedFriendCard, selectedCards
    if selectedFriendCard is None:
        return

    gate = selectedFriendCard.gate
    if gate == 'not' and len(selectedCards) == 2:
        enemyCard = next(card for card in selectedCards if card != selectedFriendCard)
        newCard = cardAttack(gate, selectedFriendCard, enemyCard)
        enemyUnit.onHandCards.append(newCard)
        friendUnit.useCards(selectedFriendCard)
        enemyUnit.useCards(enemyCard)
        selectedCards.clear()
        selectedFriendCard = None
    elif gate in ['and', 'or', 'xor'] and len(selectedCards) == 3:
        enemyCards = [card for card in selectedCards if card != selectedFriendCard]
        newCard = cardAttack(gate, selectedFriendCard, enemyCards[0], enemyCards[1])
        enemyUnit.onHandCards.append(newCard)
        friendUnit.useCards(selectedFriendCard)
        enemyUnit.useCards(enemyCards[0])
        enemyUnit.useCards(enemyCards[1])
        selectedCards.clear()
        selectedFriendCard = None

def endTurn(friendUnit, enemyUnit):

    friendUnit.SP -= len(friendUnit.useThisTurn)
    friendUnit.useThisTurn.clear()

    enemyUnit.SP -= len(enemyUnit.useThisTurn)
    enemyUnit.useThisTurn.clear()

    print("回合结束")

def main():
    pg.init()
    systemInit()
    pg.display.set_caption("Oops! A battle.")
    FriendUnit, EnemyUnit = svst.readSettings(location="./save/1.json", willModify=True)
    gSet['friendUnit'] = FriendUnit
    gSet['enemyUnit'] = EnemyUnit

    clock = pg.time.Clock()
    Screen = pg.display.set_mode(gSet['screenSize'], pg.RESIZABLE)
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.VIDEORESIZE:
                gSet['screenSize'] = gSet['screenWidth'], gSet['screenHeight'] = event.size[0], event.size[1]
                Screen = pg.display.set_mode(gSet['screenSize'], pg.RESIZABLE)
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseSelect(event, FriendUnit, EnemyUnit)
                # 检查是否点击了结束回合的按钮
                turnEndImgRect = pg.Rect(gSet['screenWidth'] // 2 - 50, 10, 100, 100)
                if turnEndImgRect.collidepoint(event.pos):
                    endTurn(friendUnit=FriendUnit, enemyUnit=EnemyUnit)
            elif event.type == pg.MOUSEMOTION:
                mouseSelect(event, FriendUnit, EnemyUnit)
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                endTurn()

        Screen.blit(pg.transform.scale(gSet['bg_img'], gSet['screenSize']), (0, 0))
        scpt.drawBattleInfo(screen=Screen, friendUnit=FriendUnit, enemyUnit=EnemyUnit)
        scpt.drawCardBorders(screen=Screen, friendUnit=FriendUnit, enemyUnit=EnemyUnit, selectedCards=selectedCards, hoveredCards=hoveredCards)
        scpt.drawCardDetail(screen=Screen, card=hoveredCards)
        pg.display.flip()
        clock.tick(gSet['fps'])

if __name__ == "__main__":
    main()
