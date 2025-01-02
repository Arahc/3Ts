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
    if friendUnit.SP > 0:
        usedRatio = len(friendUnit.useThisTurn) / friendUnit.SP  # 本回合已使用相对于当前可用 SP 的占比
        usedWidth = barWidth * friendSPratio * usedRatio
        # 从右向左画出第三颜色:
        pg.draw.rect(
            screen,
            gSet['--SP-third'],
            (
                10 + barWidth * friendSPratio - usedWidth,
                40,
                usedWidth,
                barHeight
            )
        )

    # Display enemy unit's HP and SP bars at the top right corner
    enemyHPratio = enemyUnit.HP / enemyUnit.maxHP
    pg.draw.rect(screen, gSet['--HP-ground'], (gSet['screenWidth'] - barWidth - 10, 10, barWidth, barHeight))
    pg.draw.rect(screen, gSet['--HP-front'], (gSet['screenWidth'] - barWidth - 10, 10, barWidth * enemyHPratio, barHeight))

    # SP bar
    enemySPratio = enemyUnit.SP / enemyUnit.maxSP
    pg.draw.rect(screen, gSet['--SP-ground'], (gSet['screenWidth'] - barWidth - 10, 40, barWidth, barHeight))
    pg.draw.rect(screen, gSet['--SP-front'], (gSet['screenWidth'] - barWidth - 10, 40, barWidth * enemySPratio, barHeight))
    if enemyUnit.SP > 0:
        usedRatio = len(enemyUnit.useThisTurn) / enemyUnit.SP  # 本回合已使用相对于当前可用 SP 的占比
        usedWidth = barWidth * friendSPratio * usedRatio
        # 从右向左画出第三颜色:
        pg.draw.rect(
            screen,
            gSet['--SP-third'],
            (
                gSet['screenWidth'] - barWidth - 10 + (barWidth * enemySPratio - usedWidth),
                40,
                usedWidth,
                barHeight
            )
        )

    # Display friend unit's HP and SP at the top left corner
    font = pg.font.Font(None, 36)
    friendHPtext = font.render(f'HP: {friendUnit.HP}', True, gSet['--font-color-light'])
    friendSPtext = font.render(f'SP: {friendUnit.SP} (-{len(friendUnit.useThisTurn)})', True, gSet['--font-color-light'])
    screen.blit(friendHPtext, (10, 10))
    screen.blit(friendSPtext, (10, 40))

    # Display enemy unit's HP and SP at the top right corner
    enemyHPtext = font.render(f'HP: {enemyUnit.HP}', True, gSet['--font-color-light'])
    enemySPtext = font.render(f'SP: {enemyUnit.SP} (-{len(enemyUnit.useThisTurn)})', True, gSet['--font-color-light'])
    screen.blit(enemyHPtext, (gSet['screenWidth'] - enemyHPtext.get_width() - 10, 10))
    screen.blit(enemySPtext, (gSet['screenWidth'] - enemySPtext.get_width() - 10, 40))

    # Display friend unit's image at the center left
    friendImg = pg.image.load(friendUnit.imgLocation).convert_alpha()
    screen.blit(friendImg, (gSet['screenWidth'] // 4 - friendImg.get_width() // 2, gSet['screenHeight'] // 2 - friendImg.get_height() // 2))

    # Display enemy unit's image at the center right
    enemyImg = pg.image.load(enemyUnit.imgLocation).convert_alpha()
    screen.blit(enemyImg, (3 * gSet['screenWidth'] // 4 - enemyImg.get_width() // 2, gSet['screenHeight'] // 2 - enemyImg.get_height() // 2))

    # Display friend unit's cards at the bottom left
    for i, card in enumerate(friendUnit.onHandCards):
        cardImg = pg.image.load(card.imgLocation).convert_alpha()
        screen.blit(cardImg, (10 + i * (cardImg.get_width() + 10), gSet['screenHeight'] - cardImg.get_height() - 10))

    # Display enemy unit's cards at the bottom right
    for i, card in enumerate(enemyUnit.onHandCards):
        cardImg = pg.image.load(card.imgLocation).convert_alpha()
        screen.blit(cardImg, (gSet['screenWidth'] - (i + 1) * (cardImg.get_width() + 10), gSet['screenHeight'] - cardImg.get_height() - 10))
    
    # Display the turn end bottom at the top center
    turnEndImg = pg.image.load('./assets/turn_end.png').convert_alpha()
    turnEndImg = pg.transform.scale(turnEndImg, (75, 75))
    screen.blit(turnEndImg, (gSet['screenWidth'] // 2 - turnEndImg.get_width() // 2, 10))

def drawCardBorders(screen: pg.Surface, friendUnit: Character, enemyUnit: Character, selectedCards:list, hoveredCards:list):
    from battleController import gSet
    # Draw borders for friend unit's cards
    for i, card in enumerate(friendUnit.onHandCards):
        cardImg = pg.image.load(card.imgLocation).convert_alpha()
        cardRect = cardImg.get_rect(topleft=(10 + i * (cardImg.get_width() + 10), gSet['screenHeight'] - cardImg.get_height() - 10))

        if card == hoveredCards:
            pg.draw.rect(screen, gSet['--select-card'], cardRect, 3)
        elif card in selectedCards:
            pg.draw.rect(screen, gSet['--selected-card'], cardRect, 3)

    # Draw borders for enemy unit's cards
    for i, card in enumerate(enemyUnit.onHandCards):
        cardImg = pg.image.load(card.imgLocation).convert_alpha()
        cardRect = cardImg.get_rect(topleft=(gSet['screenWidth'] - (i + 1) * (cardImg.get_width() + 10), gSet['screenHeight'] - cardImg.get_height() - 10))

        if card == hoveredCards:
            pg.draw.rect(screen, gSet['--select-card'], cardRect, 3)
        elif card in selectedCards:
            pg.draw.rect(screen, gSet['--selected-card'], cardRect, 3)

def drawCardDetail(screen: pg.Surface, card):
    from battleController import gSet
    if not card:
        return

    # 使用支持中文的字体文件
    infoFont = pg.font.Font("./assets/font/STKAITI.TTF", 24)
    cardInfo = [
        f"名称: {card.title}",
        f"门: {'与' if card.gate == 'and' else '非' if card.gate == 'not' else '或' if card.gate == 'or' else '异'}",
        f"类型: {'阳' if card.type else '阴'}",
        f"等级: {card.level}",
        f"描述: {card.description}"
    ]
    if card in gSet['friendUnit'].onHandCards:
        x, y = 10, 70
    else:
        x, y = gSet['screenWidth'] - gSet['screenWidth'] // 3 - 10, 70

    # 计算背景矩形的高度
    backgroundHeight = len(cardInfo) * 24 + 10  # 每行24像素，加上一些间距

    # 计算背景矩形的宽度
    maxWidth = max(infoFont.size(line)[0] for line in cardInfo) + 20  # 每行文字的最大宽度，加上一些间距

    # 绘制背景矩形
    backgroundRect = pg.Surface((maxWidth, backgroundHeight))
    backgroundRect.set_alpha(178)  # 透明度 0.7
    backgroundRect.fill(gSet['--card-info-ground'])

    barWidth = gSet['screenWidth'] // 3

    if card in gSet['friendUnit'].onHandCards:
        screen.blit(backgroundRect, (x, y))
    else:
        screen.blit(backgroundRect, (x + barWidth - maxWidth, y))

    for line in cardInfo:
        infoText = infoFont.render(line, True, gSet['--font-color-light'])
        if card in gSet['friendUnit'].onHandCards:
            screen.blit(infoText, (x + 10, y))  # 加上一些左边距
        else:
            screen.blit(infoText, (x + barWidth - maxWidth + 10, y))  # 加上一些左边距
        y += 24