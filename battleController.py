import sys
import pygame as pg
import saveSet as svst
import screenPainter as scpt
import copy
from cardBattle import cardAttack, TrashCard, Character, clashDealing

gSet = sys.modules['__main__'].__dict__ # global settings

selectedCards = set()
hoveredCards = None
selectedFriendCard = None

def rgb(r:int, g:int, b:int):
    return r, g, b

def systemInit():
    # kether
    gSet['cardSpace'] = 10

    # button sizes
    gSet['endTurnButtonWidth'] = 75
    gSet['endTurnButtonHeight'] = 75
    gSet['endTurnButtonSize'] = gSet['endTurnButtonWidth'], gSet['endTurnButtonHeight']
    gSet['draw&undoButtonWidth'] = 180
    gSet['draw&undoButtonHeight'] = 75
    gSet['draw&undoButtonSize'] = gSet['draw&undoButtonWidth'], gSet['draw&undoButtonHeight']

    # colors
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

def mouseSelect(event:pg.event, friendUnit:Character, enemyUnit:Character):
    global hoveredCards, selectedFriendCard
    if event.type == pg.MOUSEMOTION:
        hoveredCards = None
        mousePos = event.pos
        cardSpacing = gSet['cardSpace']

        for card in friendUnit.onHandCards + enemyUnit.onHandCards:
            cardImg = pg.image.load(card.imgLocation).convert_alpha()
            cardWidth, cardHeight = cardImg.get_size()
            maxCardsPerRow = (gSet['screenWidth'] // 2 - 20) // (cardWidth + cardSpacing)  # 每行最多显示的卡牌数量
            if card in friendUnit.onHandCards:
                index = friendUnit.onHandCards.index(card)
                row = index // maxCardsPerRow
                col = index % maxCardsPerRow
                x = 10 + col * (cardWidth + cardSpacing)
                y = gSet['screenHeight'] - cardHeight - 10 - row * (cardHeight + cardSpacing)
                if y < gSet['screenHeight'] - gSet['draw&undoButtonHeight'] - 20:
                    y = gSet['screenHeight'] - gSet['draw&undoButtonHeight'] - 20 - cardHeight - row * (cardHeight + cardSpacing)
            else:
                index = enemyUnit.onHandCards.index(card)
                row = index // maxCardsPerRow
                col = index % maxCardsPerRow
                x = gSet['screenWidth'] - (col + 1) * (cardWidth + cardSpacing)
                y = gSet['screenHeight'] - cardHeight - 10 - row * (cardHeight + cardSpacing)
                if y < gSet['screenHeight'] - gSet['draw&undoButtonHeight'] - 20:
                    y = gSet['screenHeight'] - gSet['draw&undoButtonHeight'] - 20 - cardHeight - row * (cardHeight + cardSpacing)

            card_rect = cardImg.get_rect(topleft=(x, y))
            if card_rect.collidepoint(mousePos):
                hoveredCards = card
                break

    elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        if hoveredCards:
            if hoveredCards in selectedCards:
                selectedCards.remove(hoveredCards)
            else:
                if hoveredCards in friendUnit.onHandCards:
                    if friendUnit.SP - friendUnit.SPlossThisTurn() > 0:
                        if selectedFriendCard is None:
                            selectedFriendCard = hoveredCards
                            selectedCards.add(hoveredCards)
                        elif selectedFriendCard == hoveredCards:
                            selectedFriendCard = None
                            selectedCards.remove(hoveredCards)
                else:
                    selectedCards.add(hoveredCards)
            checkCardSelection(friendUnit, enemyUnit)

def checkCardSelection(friendUnit:Character, enemyUnit:Character):
    global selectedFriendCard, selectedCards
    if selectedFriendCard is None:
        return

    gate = selectedFriendCard.gate
    if gate == 'not' and len(selectedCards) == 2:
        enemyCard = next(card for card in selectedCards if card != selectedFriendCard)
        newCard = cardAttack(gate, selectedFriendCard, enemyCard)
        enemyUnit.onHandCards.append(newCard)
        friendUnit.useCard(selectedFriendCard)
        enemyUnit.lostCard(enemyCard)
        selectedCards.clear()
        selectedFriendCard = None
    elif gate in ['and', 'or', 'xor'] and len(selectedCards) == 3:
        enemyCards = [card for card in selectedCards if card != selectedFriendCard]
        newCard = cardAttack(gate, selectedFriendCard, enemyCards[0], enemyCards[1])
        enemyUnit.onHandCards.append(newCard)
        friendUnit.useCard(selectedFriendCard)
        enemyUnit.lostCard(enemyCards[0])
        enemyUnit.lostCard(enemyCards[1])
        selectedCards.clear()
        selectedFriendCard = None

recordedTurnState = None
def recordTurnState(friendUnit:Character, enemyUnit:Character):
    global recordedTurnState
    recordedTurnState = copy.deepcopy([friendUnit, enemyUnit])

def endTurn(friendUnit:Character, enemyUnit:Character):
    # Clear the cards that are used or cancelled this turn
    friendUnit.SP -= friendUnit.SPlossThisTurn()
    enemyUnit.SP -= enemyUnit.SPlossThisTurn()
    friendUnit.useThisTurn.clear()
    enemyUnit.useThisTurn.clear()
    friendUnit.getThisTurn.clear()
    enemyUnit.getThisTurn.clear()
    friendUnit.lostThisTurn.clear()
    enemyUnit.lostThisTurn.clear()

    # Heal SP
    friendUnit.SP += friendUnit.SPHeal
    if friendUnit.SP > friendUnit.maxSP:
        friendUnit.SP = friendUnit.maxSP
    enemyUnit.SP += enemyUnit.SPHeal
    if enemyUnit.SP > enemyUnit.maxSP:
        enemyUnit.SP = enemyUnit.maxSP

    # Deal with clash
    clashDealing(friendUnit=friendUnit,enemyUnit=enemyUnit)

    # refresh the record of the turn state
    recordTurnState(friendUnit, enemyUnit)

def drawCard(friendUnit:Character):
    if friendUnit.SP - friendUnit.SPlossThisTurn() > 0:
        newCard = friendUnit.getCard()

def undoTurn():
    global recordedTurnState
    return copy.deepcopy(recordedTurnState)

def main():
    pg.init()
    systemInit()
    pg.display.set_caption("Oops! A battle.")
    FriendUnit, EnemyUnit = svst.readSettings(location="./save/1.json", willModify=True)
    recordTurnState(FriendUnit, EnemyUnit)
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
                # Select a card
                mouseSelect(event, FriendUnit, EnemyUnit)

                # Click the end turn button
                turnEndImgRect = pg.Rect(gSet['screenWidth'] // 2 - gSet['endTurnButtonWidth'] // 2, 10, gSet['endTurnButtonWidth'], gSet['endTurnButtonHeight'])
                if turnEndImgRect.collidepoint(event.pos):
                    endTurn(friendUnit=FriendUnit, enemyUnit=EnemyUnit)

                # Click the draw button
                drawImgRect = pg.Rect(gSet['screenWidth'] // 2 - gSet['draw&undoButtonWidth'] // 2 - 90, gSet['screenHeight'] - gSet['draw&undoButtonHeight'] - 10, gSet['draw&undoButtonWidth'], gSet['draw&undoButtonHeight'])
                if drawImgRect.collidepoint(event.pos):
                    drawCard(friendUnit=FriendUnit)

                # Click the undo button
                undoImgRect = pg.Rect(gSet['screenWidth'] // 2 - gSet['draw&undoButtonWidth'] // 2 + 90, gSet['screenHeight'] - gSet['draw&undoButtonHeight'] - 10, gSet['draw&undoButtonWidth'], gSet['draw&undoButtonHeight'])
                if undoImgRect.collidepoint(event.pos):
                    FriendUnit, EnemyUnit = undoTurn()
    
            elif event.type == pg.MOUSEMOTION:
                mouseSelect(event, FriendUnit, EnemyUnit)
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                endTurn(friendUnit=FriendUnit, enemyUnit=EnemyUnit)

        Screen.blit(pg.transform.scale(gSet['bg_img'], gSet['screenSize']), (0, 0))
        scpt.drawBattleInfo(screen=Screen, friendUnit=FriendUnit, enemyUnit=EnemyUnit)
        scpt.drawCards(screen=Screen, friendUnit=FriendUnit, enemyUnit=EnemyUnit)
        scpt.drawCardBorders(screen=Screen, friendUnit=FriendUnit, enemyUnit=EnemyUnit, selectedCards=selectedCards, hoveredCards=hoveredCards)
        scpt.drawCardDetail(screen=Screen, card=hoveredCards)
        pg.display.flip()
        clock.tick(gSet['fps'])

if __name__ == "__main__":
    main()
