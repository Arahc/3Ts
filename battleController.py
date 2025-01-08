import sys
import pygame as pg
import saveSet as svst
import screenPainter as scpt

gSet = sys.modules['__main__'].__dict__ # global settings
"""
screenHeight: The height of the screen. (px)
screenWidth: The width of the screen. (px)
bg_img_loaction: The location of the background img
"""

def rgb(r:int, g:int, b:int):
    return r,g,b

def systemInit():
    gSet['--font-color-light'] = rgb(242, 253, 255)
    gSet['--HP-ground'] = rgb(0, 99, 29)
    gSet['--HP-front'] = rgb(0, 205, 102)
    gSet['--SP-ground'] = rgb(25, 25, 112)
    gSet['--SP-front'] = rgb(65, 105, 225)
    gSet['--select-card'] = rgb(252, 243, 207)
    gSet['--selected-card'] = rgb(245, 183, 177)

def Initialization(screenWidth:int, screenHeight:int, bg_img_loaction:str, fps:int):
    gSet['screenSize'] = screenWidth, screenHeight
    gSet['screenWidth'] = screenWidth
    gSet['screenHeight'] = screenHeight
    gSet['bg_img'] = pg.image.load(bg_img_loaction)
    gSet['fps'] = fps

selected_cards = set()
hovered_card = None

def handle_mouse_event(event, friendUnit, enemyUnit):
    global hovered_card
    if event.type == pg.MOUSEMOTION:
        hovered_card = None
        mouse_pos = event.pos
        for card in friendUnit.cards + enemyUnit.cards:
            card_image = pg.image.load(card.imgLocation).convert_alpha()
            card_rect = card_image.get_rect()
            if card in friendUnit.cards:
                card_rect.topleft = (10 + friendUnit.cards.index(card) * (card_image.get_width() + 10), gSet['screenHeight'] - card_image.get_height() - 10)
            else:
                card_rect.topleft = (gSet['screenWidth'] - (enemyUnit.cards.index(card) + 1) * (card_image.get_width() + 10), gSet['screenHeight'] - card_image.get_height() - 10)
            if card_rect.collidepoint(mouse_pos):
                hovered_card = card
                break
    elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        if hovered_card:
            if hovered_card in selected_cards:
                selected_cards.remove(hovered_card)
            else:
                selected_cards.add(hovered_card)

def main():
    pg.init()
    systemInit()
    pg.display.set_caption("Oops! A battle.")
    FriendUnit, EnemyUnit = svst.readSettings(location="./save/1.json", willModify=True)

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
            elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEMOTION:
                handle_mouse_event(event, FriendUnit, EnemyUnit)

        Screen.blit(pg.transform.scale(gSet['bg_img'], gSet['screenSize']), (0, 0))
        scpt.drawBattleInfo(screen=Screen, friendUnit=FriendUnit, enemyUnit=EnemyUnit)
        scpt.drawCardBorders(screen=Screen, friendUnit=FriendUnit, enemyUnit=EnemyUnit, selected_cards=selected_cards, hovered_card=hovered_card)
        pg.display.update()
        clock.tick(gSet['fps'])


if __name__ == "__main__":
    main()
