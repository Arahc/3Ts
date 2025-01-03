class Effect:
    def __init__(self, time:str, title:str, description:str, value:int, obj:object, fragile:bool):
        """
        time: The time that the effect starts.
        title: The title of the effect.
        description: The description of the effect.
        value: The value of the effect. Positive for adding, negative for subtracting.
        obj: The object that the effect is applied to, may be HP, SP, buff, debuff, etc.
        fragile: If True, the effect will be removed if the card is operated.
        """
        self.time = time
        self.title = title
        self.description = description
        self.value = value
        self.obj = obj
        self.fragile = fragile

class Card:
    def __init__(self, ID:int, title:str, description:str, gate:str, type:bool, level:int, effects:list, imgLocation:str):
        """
        ID: The id of the card. Unique for each card.
        title: The title of the card.
        description: The description of the card.
        gate: The gate that the card is in. and/or/xor/not. Can be None if the card doesn't contain a gate.
        type: True = Yang, False = Yin
        level: The number of the number of the type (3 0s, etc.)
        effects: The effects of the card. List of Effect objects.
        imgLocation: The location of the image of the card.
        """
        self.ID = ID
        self.title = title
        self.description = description
        self.gate = gate
        self.type = type
        self.level = level
        self.effects = effects
        self.imgLocation = imgLocation
    def __str__(self):
        return self.title

TrashCard = Card(ID=-1, title="Trash Card", description="A card that will not appear, set as a null card", gate="None", type=True, level=0, effects=[], imgLocation="./assets/card/-1.png")

def cardAttack(gate:str, card0:Card, card1:Card, card2:Card=TrashCard)->Card:
    """
    Use the gate of self to attack the cards
    gate: The gate of the card that is attacking.
    card1, card2: The cards that are being attacked.
    When attacked, the cards will be merged into one, 
        with the effects of the card being applied to the new card (except for fragile effects).
    The level of the new card will be the sum of the levels of the two cards.
    """
    if card0.gate != gate:
        raise ValueError("Invalid operation: the gate of the card is not the same as the gate of the operation")
    resultCard = Card(ID=0, title='operated card', description='operated card', gate='None', type=True, level=0, effects=[], imgLocation='./assets/card/res.png')
    if gate == 'not':
        if card2 != TrashCard:
            raise ValueError("Invalid operation: 'not' gate operates on one card")
        resultCard.type = not card1.type
        resultCard.level = card1.level
        for effect in card1.effects:
            if not effect.fragile:
                resultCard.effects.append(effect)
    elif gate == 'and':
        if card2 == TrashCard:
            raise ValueError("Invalid operation: 'and' gate operates on two cards")
        resultCard.type = card1.type and card2.type
        resultCard.level = (card1.level + card2.level) // 2
        for effect in card1.effects:
            if not effect.fragile:
                resultCard.effects.append(effect)
        for effect in card2.effects:
            if not effect.fragile:
                resultCard.effects.append(effect)
    elif gate == 'or':
        if card2 == TrashCard:
            raise ValueError("Invalid operation: 'or' gate operates on two cards")
        resultCard.type = card1.type or card2.type
        resultCard.level = (card1.level + card2.level) // 2
        for effect in card1.effects:
            if not effect.fragile:
                resultCard.effects.append(effect)
        for effect in card2.effects:
            if not effect.fragile:
                resultCard.effects.append(effect)
    elif gate == 'xor':
        if card2 == TrashCard:
            raise ValueError("Invalid operation: 'xor' gate operates on two cards")
        resultCard.type = card1.type != card2.type
        resultCard.level = (card1.level + card2.level) // 2
        for effect in card1.effects:
            if not effect.fragile:
                resultCard.effects.append(effect)
        for effect in card2.effects:
            if not effect.fragile:
                resultCard.effects.append(effect)
    else:
        raise ValueError("Invalid gate: the gate does not exist")
    return resultCard

import random

class Character:
    def __init__(self, ID:int, name:str, HP:int, SP:int, SPHeal:int, maxHP:int, maxSP:int, cards:list, imgLocation:str):
        """
        ID: The id of the character. Unique for each character.
        name: The name of the character.
        HP: The HP of the character.
        SP: The SP of the character.
        cards: The cards that the character has. List of Card objects.
        imgLocation: The location of the image of the character.
        """
        self.ID = ID
        self.name = name
        self.HP = HP
        self.SP = SP
        self.SPHeal = SPHeal
        self.cards = cards
        self.imgLocation = imgLocation
        self.maxHP = maxHP
        self.maxSP = maxSP
        self.onHandCards = cards
        self.usedCards = []
        self.unusedCards = []
        self.useThisTurn = []
        self.lostThisTurn = []
        self.getThisTurn = []
    def __str__(self):
        return self.name
    def initCharacter(self)->list:
        """
        Initialize the cards of the character.
            Draw SP cards from the cards of the character.
        Initialize the HP and SP of the character.
        """
        self.usedCards = []
        self.onHandCards = random.choices(self.cards, k=self.SP)
        self.unusedCards = self.cards.copy()
        for card in self.onHandCards:
            self.unusedCards.remove(card)
        return self.onHandCards

    def SPlossThisTurn(self)->int:
        """
        Get the SP loss of the character this turn.
        """
        return len(self.useThisTurn) + len(self.getThisTurn)

    def useCard(self, card:Card)->None:
        """
        Use a card.
        If the card has effect "When used ..." [time='use'], apply the effect.
        """
        for effect in card.effects:
            if effect.time == 'use':
                pass # TODO <------------------------------------------------------------------------------------------ apply the effect
        try:
            self.onHandCards.remove(card)
        except ValueError:
            raise ValueError("Invalid card: the card is not on hand")
        self.usedCards.append(card)
        self.useThisTurn.append(card)
        if self.SP - len(self.useThisTurn) < 0:
            raise ValueError("Invalid SP: the SP of the character is negative")
    def lostCard(self, card:Card)->None:
        """
        Lost a card
        If the card has effect "When lost ..." [time='lost'], apply the effect.
        """
        for effect in card.effects:
            if effect.time == 'lost':
                pass # TODO <------------------------------------------------------------------------------------------ apply the effect
        try:
            self.onHandCards.remove(card)
        except ValueError:
            raise ValueError("Invalid card: the card is not on hand")
        self.usedCards.append(card)
        self.lostThisTurn.append(card)
    def getCard(self)->Card:
        import random
        """
        Get a card.
        If the card has effect "When get ..." [time='get'], apply the effect.
        If the character has no cards left, shuffle the used cards and set them as the cards of the character.
        If no used cards are left, return TrashCard.
        """
        if self.unusedCards == []:
            self.unusedCards = self.usedCards
            self.usedCards = []
            if self.unusedCards == []:
                return TrashCard
        card = random.choice(self.unusedCards)
        self.unusedCards.remove(card)
        for effect in card.effects:
            if effect.time == 'get':
                pass # TODO <------------------------------------------------------------------------------------------ apply the effect
        self.getThisTurn.append(card)
        self.onHandCards.append(card)
        return card

def clashDealing(friendUnit:Character, enemyUnit:Character):
    friendLevel = 0
    for card in friendUnit.onHandCards:
        friendLevel += card.level
    enemyLevel = 0
    for card in enemyUnit.onHandCards:
        enemyLevel += card.level
    
    """
    If draw, nothing happen.
    If one character wins, cause damage to another character.
    """
    if friendLevel == enemyLevel:
        pass
    elif friendLevel < enemyLevel:
        yin = 0
        yang = 0
        for card in enemyUnit.onHandCards:
            if card.type:
                yang += 1
            else:
                yin += 1
        damage = max(yin, yang) * (enemyLevel - friendLevel)
        friendUnit.HP -= damage
        if friendUnit.HP < 0:
            friendUnit.HP = 0
    else:
        yin = 0
        yang = 0
        for card in friendUnit.onHandCards:
            if card.type:
                yang += 1
            else:
                yin += 1
        damage = max(yin, yang) * (enemyLevel - friendLevel)
        enemyUnit.HP -= damage
        if enemyUnit.HP < 0:
            enemyUnit.HP = 0