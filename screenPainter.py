import pygame as pg
from cardBattle import Character, Card

def drawBattleInfo(screen:pg.Surface, friendUnit:Character, enemyUnit:Character):
    from battleController import gSet
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
    if friendUnit.SP > 0 and friendUnit.SPlossThisTurn() > 0:
        usedRatio = friendUnit.SPlossThisTurn() / friendUnit.SP  # 本回合已使用相对于当前可用 SP 的占比
        usedWidth = barWidth * friendSPratio * usedRatio
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
    if enemyUnit.SP > 0 and enemyUnit.SPlossThisTurn() > 0:
        usedRatio = enemyUnit.SPlossThisTurn() / enemyUnit.SP  # 本回合已使用相对于当前可用 SP 的占比
        usedWidth = barWidth * friendSPratio * usedRatio
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

    # Display Character unit's HP and SP at the top left corner
    font = pg.font.Font(None, 36)
    friendHPtext = font.render(f'HP: {friendUnit.HP}', True, gSet['--font-color-light'])
    friendSPtextContent = f'SP: {friendUnit.SP}'
    if friendUnit.SPlossThisTurn() > 0:
        friendSPtextContent += f' (-{friendUnit.SPlossThisTurn()})'
    friendSPtext = font.render(friendSPtextContent, True, gSet['--font-color-light'])
    screen.blit(friendHPtext, (10, 10))
    screen.blit(friendSPtext, (10, 40))

    # Display enemy unit's HP and SP at the top right corner
    enemyHPtext = font.render(f'HP: {enemyUnit.HP}', True, gSet['--font-color-light'])
    enemySPtextContent = f'SP: {enemyUnit.SP}'
    if enemyUnit.SPlossThisTurn() > 0:
        enemySPtextContent += f' (-{enemyUnit.SPlossThisTurn()})'
    enemySPtext = font.render(enemySPtextContent, True, gSet['--font-color-light'])
    screen.blit(enemyHPtext, (gSet['screenWidth'] - enemyHPtext.get_width() - 10, 10))
    screen.blit(enemySPtext, (gSet['screenWidth'] - enemySPtext.get_width() - 10, 40))

    # Display Character unit's image at the center left
    friendImg = pg.image.load(friendUnit.imgLocation).convert_alpha()
    screen.blit(friendImg, (gSet['screenWidth'] // 4 - friendImg.get_width() // 2, gSet['screenHeight'] // 2 - friendImg.get_height() // 2))

    # Display enemy unit's image at the center right
    enemyImg = pg.image.load(enemyUnit.imgLocation).convert_alpha()
    screen.blit(enemyImg, (3 * gSet['screenWidth'] // 4 - enemyImg.get_width() // 2, gSet['screenHeight'] // 2 - enemyImg.get_height() // 2))
    
    # Display the turn end bottom at the top center
    turnEndImg = pg.image.load('./assets/img/turn_end.png').convert_alpha()
    turnEndImg = pg.transform.scale(turnEndImg, gSet['endTurnButtonSize'])
    screen.blit(turnEndImg, (gSet['screenWidth'] // 2 - turnEndImg.get_width() // 2, 10))

    # Display the draw button at the bottom center (slightly left)
    drawImg = pg.image.load('./assets/img/draw_button.png').convert_alpha()
    drawImg = pg.transform.scale(drawImg, gSet['draw&undoButtonSize'])
    screen.blit(drawImg, (gSet['screenWidth'] // 2 - drawImg.get_width() // 2 - 90, gSet['screenHeight'] - drawImg.get_height() - 10))

    # Display the undo button at the bottom center (slightly right)
    undoImg = pg.image.load('./assets/img/undo_button.png').convert_alpha()
    undoImg = pg.transform.scale(undoImg, gSet['draw&undoButtonSize'])
    screen.blit(undoImg, (gSet['screenWidth'] // 2 - undoImg.get_width() // 2 + 90, gSet['screenHeight'] - undoImg.get_height() - 10))

def drawCards(screen: pg.Surface, friendUnit: Character, enemyUnit: Character):
    from battleController import gSet
    cardSpacing = gSet['cardSpace']

    # Display friend unit's cards at the bottom left
    for i, card in enumerate(friendUnit.onHandCards):
        cardImg = pg.image.load(card.imgLocation).convert_alpha()
        cardWidth, cardHeight = cardImg.get_size()
        maxCardsPerRow = (gSet['screenWidth'] // 2 - 20) // (cardWidth + cardSpacing)  # 每行最多显示的卡牌数量
        row = i // maxCardsPerRow
        col = i % maxCardsPerRow
        x = 10 + col * (cardWidth + cardSpacing)
        y = gSet['screenHeight'] - cardHeight - 10 - row * (cardHeight + cardSpacing)
        if y < gSet['screenHeight'] - gSet['draw&undoButtonHeight'] - 20:
            y = gSet['screenHeight'] - gSet['draw&undoButtonHeight'] - 20 - cardHeight - row * (cardHeight + cardSpacing)
        screen.blit(cardImg, (x, y))

    # Display enemy unit's cards at the bottom right
    for i, card in enumerate(enemyUnit.onHandCards):
        cardImg = pg.image.load(card.imgLocation).convert_alpha()
        cardWidth, cardHeight = cardImg.get_size()
        maxCardsPerRow = (gSet['screenWidth'] // 2 - 20) // (cardWidth + cardSpacing)  # 每行最多显示的卡牌数量
        row = i // maxCardsPerRow
        col = i % maxCardsPerRow
        x = gSet['screenWidth'] - (col + 1) * (cardWidth + cardSpacing)
        y = gSet['screenHeight'] - cardHeight - 10 - row * (cardHeight + cardSpacing)
        if y < gSet['screenHeight'] - gSet['draw&undoButtonHeight'] - 20:
            y = gSet['screenHeight'] - gSet['draw&undoButtonHeight'] - 20 - cardHeight - row * (cardHeight + cardSpacing)
        screen.blit(cardImg, (x, y))

def drawCardBorders(screen: pg.Surface, friendUnit: Character, enemyUnit: Character, selectedCards:list, hoveredCards:list):
    from battleController import gSet
    cardSpacing = gSet['cardSpace']

    # Draw borders for friend unit's cards
    for i, card in enumerate(friendUnit.onHandCards):
        cardImg = pg.image.load(card.imgLocation).convert_alpha()
        cardWidth, cardHeight = cardImg.get_size()
        maxCardsPerRow = (gSet['screenWidth'] // 2 - 20) // (cardWidth + cardSpacing)  # 每行最多显示的卡牌数量
        row = i // maxCardsPerRow
        col = i % maxCardsPerRow
        x = 10 + col * (cardWidth + cardSpacing)
        y = gSet['screenHeight'] - cardHeight - 10 - row * (cardHeight + cardSpacing)
        if y < gSet['screenHeight'] - gSet['draw&undoButtonHeight'] - 20:
            y = gSet['screenHeight'] - gSet['draw&undoButtonHeight'] - 20 - cardHeight - row * (cardHeight + cardSpacing)
        cardRect = cardImg.get_rect(topleft=(x, y))

        if card == hoveredCards:
            pg.draw.rect(screen, gSet['--select-card'], cardRect, 3)
        elif card in selectedCards:
            pg.draw.rect(screen, gSet['--selected-card'], cardRect, 3)

    # Draw borders for enemy unit's cards
    for i, card in enumerate(enemyUnit.onHandCards):
        cardImg = pg.image.load(card.imgLocation).convert_alpha()
        cardWidth, cardHeight = cardImg.get_size()
        maxCardsPerRow = (gSet['screenWidth'] // 2 - 20) // (cardWidth + cardSpacing)  # 每行最多显示的卡牌数量
        row = i // maxCardsPerRow
        col = i % maxCardsPerRow
        x = gSet['screenWidth'] - (col + 1) * (cardWidth + cardSpacing)
        y = gSet['screenHeight'] - cardHeight - 10 - row * (cardHeight + cardSpacing)
        if y < gSet['screenHeight'] - gSet['draw&undoButtonHeight'] - 20:
            y = gSet['screenHeight'] - gSet['draw&undoButtonHeight'] - 20 - cardHeight - row * (cardHeight + cardSpacing)
        cardRect = cardImg.get_rect(topleft=(x, y))

        if card == hoveredCards:
            pg.draw.rect(screen, gSet['--select-card'], cardRect, 3)
        elif card in selectedCards:
            pg.draw.rect(screen, gSet['--selected-card'], cardRect, 3)

def drawCardDetail(screen: pg.Surface, card: Card):
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