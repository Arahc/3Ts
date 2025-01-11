import pygame, sys
from GameSettings import *
from Utility import Scene

class ShopPage(Scene):

    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(FontSettings.FontPath, 36)

        self.tip_text = self.font.render("", True, WHITE)
        self.tip_rect = self.tip_text.get_rect()
        self.tip_rect.center = (ShopSettings.width // 2, ShopSettings.shop_y + 400)  
        self.width = ShopSettings.width
        self.height = ShopSettings.height
        self.shop_x = ShopSettings.shop_x
        self.shop_y = ShopSettings.shop_y
        self.shop_rect = pygame.Rect(self.shop_x, self.shop_y, self.width, self.height)
        self.shop_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.shop_surface.fill(ShopSettings.shopbox_color)
        self.buytime = -1000
    
    def show(self, window):
        self.window = window

        # 加载商品图标
        self.card_icon = pygame.image.load(r'.\assets\card.png')
        self.card_icon = pygame.transform.scale(self.card_icon, (60, 50))
        self.health_icon = pygame.image.load(r'.\assets\hp.png')
        self.health_icon = pygame.transform.scale(self.health_icon, (50, 70))

        # 定义商店界面文本
        self.store_text = self.font.render("商店", True, WHITE)
        self.store_rect = self.store_text.get_rect()
        self.store_rect.center = (self.width // 2, self.shop_x + 50)

        # 定义商品价格文本
        self.card_price_text = self.font.render("20 吉欧", True, WHITE)
        self.card_price_rect = self.card_price_text.get_rect()
        self.card_price_rect.center = (self.width // 2 + 100, self.shop_x + 180)

        self.health_price_text = self.font.render("25 吉欧", True, WHITE)
        self.health_price_rect = self.health_price_text.get_rect()
        self.health_price_rect.center = (self.width // 2 + 100, self.shop_x + 280)

        window.blit(self.shop_surface, (self.shop_x, self.shop_y))
        window.blit(self.store_text, self.store_rect)
        window.blit(self.card_icon, (self.width // 2 - 100, self.shop_x + 150))
        window.blit(self.card_price_text, self.card_price_rect)
        window.blit(self.health_icon, (self.width // 2 - 100, self.shop_x + 250))
        window.blit(self.health_price_text, self.health_price_rect)
        tim = pygame.time.get_ticks()
        if (tim - self.buytime < 500):
            window.blit(self.tip_text, self.tip_rect)
    
    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 鼠标左键点击
            self.card_icon_rect = self.card_icon.get_rect()
            self.card_icon_rect.topleft = (self.width // 2 - 100, self.shop_x + 150)

            self.health_icon_rect = self.health_icon.get_rect()
            self.health_icon_rect.topleft = (self.width // 2 - 100, self.shop_x + 250)

            mouse_pos = event.pos
            if self.card_icon_rect.collidepoint(mouse_pos) or self.card_price_rect.collidepoint(mouse_pos):
                self.buytime = pygame.time.get_ticks()
                # 点击升级卡牌
                if self.player.money >= 20:
                    self.player.money -= 20
                    self.player.card_level += 1
                    self.tip_text = self.font.render("购买成功", True, WHITE)
                else:
                    self.tip_text = self.font.render("吉欧不足", True, WHITE)
            elif self.health_icon_rect.collidepoint(mouse_pos) or self.health_price_rect.collidepoint(mouse_pos):
                self.buytime = pygame.time.get_ticks()
                # 点击提升血量上限
                if self.player.money >= 25:
                    self.player.money -= 25
                    self.player.hp += 10
                    self.tip_text = self.font.render("购买成功", True, WHITE)
                else:
                    self.tip_text = self.font.render("吉欧不足", True, WHITE)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'QuitShop'