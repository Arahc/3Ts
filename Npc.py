import pygame
import sys
from GameSettings import *
# from openai import OpenAI
from typing import List, Dict
from GameSettings import *


class Npc():
    def __init__(self, imgpath, id, width, height, posX, posY):

        self.image = pygame.image.load(imgpath)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.imageRect = pygame.Rect(posX, posY, width, height)
        
        # 设置 AI
        # self.client = OpenAI(
        #     base_url="http://10.15.88.73:5006/v1",
        #     api_key="ollama",
        # )

        if (id == 'seer'):
            self.messages: List[Dict] = [
                {
                    "role": "system",
                    "content": "你要扮演游戏《空洞骑士》里的蛾子一族里的先知。玩家扮演的小骑士会向你发出一系列问题，请给出符合你身份的回答。",
                }
            ]

        self.npc_response = ""

    def update(self, input_text: str):
        self.messages.append({"role": "user", "content": input_text})
        response = self.client.chat.completions.create(
            model="llama3.2",
            messages=self.messages,
        )
        self.npc_response = response.choices[0].message.content
        # 将助手添加到对话历史
        self.messages.append({"role": "assistant", "content": self.npc_responce})

