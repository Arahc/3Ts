import json
import cardBattle

def readSettings(location="./save/1.json", willModify=False):
    """
    Read settings from the location and modify the global settings if willModify=True
    """
    with open(location, 'r', encoding='utf-8') as file:
        settings = json.load(file)

    if willModify:
        from battleController import Initialization
        globalSettings = settings['globalSettings']
        Initialization(
            screenWidth = globalSettings['Screen']['Width'],
            screenHeight = globalSettings['Screen']['Height'],
            bg_img_loaction = globalSettings['Background'],
            fps = globalSettings['fps'] 
        )

    friendUnitData = settings['Characters']['friendUnit'][0]
    enemyUnitData = settings['Characters']['enemyUnit'][0]

    def create_card(card_data):
        effects = [cardBattle.Effect(**effect) for effect in card_data['effects']]
        return cardBattle.Card(
            ID=card_data['ID'],
            title=card_data['title'],
            description=card_data['description'],
            gate=card_data['gate'],
            type=card_data['type'] == 'True',
            level=card_data['level'],
            effects=effects,
            imgLocation=card_data['imgLocation']
        )

    friendUnit = cardBattle.Character(
        ID=friendUnitData['ID'],
        name=friendUnitData['name'],
        HP=friendUnitData['HP'],
        SP=friendUnitData['SP'],
        maxHP=friendUnitData['maxHP'],
        maxSP=friendUnitData['maxSP'],
        cards=[create_card(card) for card in friendUnitData['cards']],
        imgLocation=friendUnitData['imgLocation']
    )

    enemyUnit = cardBattle.Character(
        ID=enemyUnitData['ID'],
        name=enemyUnitData['name'],
        HP=enemyUnitData['HP'],
        maxHP=enemyUnitData['maxHP'],
        maxSP=enemyUnitData['maxSP'],
        SP=enemyUnitData['SP'],
        cards=[create_card(card) for card in enemyUnitData['cards']],
        imgLocation=enemyUnitData['imgLocation']
    )

    return friendUnit, enemyUnit