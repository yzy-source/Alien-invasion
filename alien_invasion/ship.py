import pygame

from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_settings,screen):
        super(Ship,self).__init__()
        #初始化飞船设置其初始位置
        self.screen=screen
        self.ai_settings=ai_settings

        #加载飞船图像获取其外接矩形
        self.image=pygame.image.load('images/ship.bmp')
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()

        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom

        #在飞船的属性center中存储小数
        self.center=float(self.rect.centerx)

        #移动标志
        self.moving_right=False
        self.moving_left=False

    def blitme(self):
        self.screen.blit(self.image,self.rect)

    def update(self):
        #速度大于1更新center 而不是rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
           # self.rect.centerx+=1
            self.center+=self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            # self.rect.centerx-=1
            self.center-=self.ai_settings.ship_speed_factor

        #更新rect
        self.rect.centerx=self.center

    def center_ship(self):
        self.center=self.screen_rect.centerx

