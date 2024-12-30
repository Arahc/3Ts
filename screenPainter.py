import pygame as pg
from cardBattle import Character

def drawBattleInfo(screen:pg.Surface, friendUnit:Character, enemyUnit:Character):
    from battleController import gSet
    # Display friend unit's HP and SP bars at the top left corner
    barWidth = gSet['screenWidth'] // 3
    barHeight = 20

    # HP bar
    friendHPratio = friendUnit.HP / friendUnit.maxHP
    pg.draw.rect(screen, gSet['--HP-ground'], (10, 10, barWidth, barHeight))
    pg.draw.rect(screen, gSet['--HP-front'], (10, 10, barWidth * friendHPratio, barHeight))

    # SP bar
    friendSPratio = friendUnit.SP / friendUnit.maxSP
    pg.draw.rect(screen, gSet['--SP-ground'], (10, 40, barWidth, barHeight))
    pg.draw.rect(screen, gSet['--SP-front'], (10, 40, barWidth * friendSPratio, barHeight))

    # Display enemy unit's HP and SP bars at the top right corner
    enemyHPratio = enemyUnit.HP / enemyUnit.maxHP
    pg.draw.rect(screen, gSet['--HP-ground'], (gSet['screenWidth'] - barWidth - 10, 10, barWidth, barHeight))
    pg.draw.rect(screen, gSet['--HP-front'], (gSet['screenWidth'] - barWidth - 10, 10, barWidth * enemyHPratio, barHeight))

    # SP bar
    enemySPratio = enemyUnit.SP / enemyUnit.maxSP
    pg.draw.rect(screen, gSet['--SP-ground'], (gSet['screenWidth'] - barWidth - 10, 40, barWidth, barHeight))
    pg.draw.rect(screen, gSet['--SP-front'], (gSet['screenWidth'] - barWidth - 10, 40, barWidth * enemySPratio, barHeight))

    # Display friend unit's HP and SP at the top left corner
    font = pg.font.Font(None, 36)
    friendHPtext = font.render(f'HP: {friendUnit.HP}', True, gSet['--font-color-light'])
    friendSPtext = font.render(f'SP: {friendUnit.SP}', True, gSet['--font-color-light'])
    screen.blit(friendHPtext, (10, 10))
    screen.blit(friendSPtext, (10, 40))

    # Display enemy unit's HP and SP at the top right corner
    enemyHPtext = font.render(f'HP: {enemyUnit.HP}', True, gSet['--font-color-light'])
    enemySPtext = font.render(f'SP: {enemyUnit.SP}', True, gSet['--font-color-light'])
    screen.blit(enemyHPtext, (gSet['screenWidth'] - enemyHPtext.get_width() - 10, 10))
    screen.blit(enemySPtext, (gSet['screenWidth'] - enemySPtext.get_width() - 10, 40))

    # Display friend unit's image at the center left
    friendImg = pg.image.load(friendUnit.imgLocation).convert_alpha()
    screen.blit(friendImg, (gSet['screenWidth'] // 4 - friendImg.get_width() // 2, gSet['screenHeight'] // 2 - friendImg.get_height() // 2))

    # Display enemy unit's image at the center right
    enemyImg = pg.image.load(enemyUnit.imgLocation).convert_alpha()
    screen.blit(enemyImg, (3 * gSet['screenWidth'] // 4 - enemyImg.get_width() // 2, gSet['screenHeight'] // 2 - enemyImg.get_height() // 2))

    # Display friend unit's cards at the bottom left
    for i, card in enumerate(friendUnit.cards):
        cardImg = pg.image.load(card.imgLocation).convert_alpha()
        screen.blit(cardImg, (10 + i * (cardImg.get_width() + 10), gSet['screenHeight'] - cardImg.get_height() - 10))

    # Display enemy unit's cards at the bottom right
    for i, card in enumerate(enemyUnit.cards):
        cardImg = pg.image.load(card.imgLocation).convert_alpha()
        screen.blit(cardImg, (gSet['screenWidth'] - (i + 1) * (cardImg.get_width() + 10), gSet['screenHeight'] - cardImg.get_height() - 10))

    pg.display.flip()

def drawCardBorders(screen: pg.Surface, friendUnit: Character, enemyUnit: Character, selectedCards:list, hoveredCards:list):
    from battleController import gSet
    # Draw borders for friend unit's cards
    for i, card in enumerate(friendUnit.cards):
        cardImg = pg.image.load(card.imgLocation).convert_alpha()
        cardRect = cardImg.get_rect(topleft=(10 + i * (cardImg.get_width() + 10), gSet['screenHeight'] - cardImg.get_height() - 10))

        if card == hoveredCards:
            pg.draw.rect(screen, gSet['--select-card'], cardRect, 3)
        elif card in selectedCards:
            pg.draw.rect(screen, gSet['--selected-card'], cardRect, 3)

    # Draw borders for enemy unit's cards
    for i, card in enumerate(enemyUnit.cards):
        cardImg = pg.image.load(card.imgLocation).convert_alpha()
        cardRect = cardImg.get_rect(topleft=(gSet['screenWidth'] - (i + 1) * (cardImg.get_width() + 10), gSet['screenHeight'] - cardImg.get_height() - 10))

        if card == hoveredCards:
            pg.draw.rect(screen, gSet['--select-card'], cardRect, 3)
        elif card in selectedCards:
            pg.draw.rect(screen, gSet['--selected-card'], cardRect, 3)