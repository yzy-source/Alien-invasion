import pygame.ftfont

from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    #显示得分信息
    def __init__(self,ai_settings,screen,stats):
        self.screen=screen
        self.screen_rect=screen.get_rect()
        self.ai_settings=ai_settings
        self.stats=stats

        #得分信息字体
        self.text_color=(30,30,30)
        self.font=pygame.ftfont.SysFont(None,32)

        #当前得分 和最高得分,等级
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        #得分渲染为图像
        rounded_score=int(round(self.stats.score,-1))
        score_str="{:,}".format(rounded_score)
        score_str="score: "+score_str
        self.score_image=self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)

        #得分放在右上角
        self.score_rect=self.score_image.get_rect()
        self.score_rect.right=self.screen_rect.right-20
        self.score_rect.top=20

    def prep_high_score(self):
        high_score=int(round(self.stats.high_score,-1))
        high_score_str="{:,}".format(high_score)
        high_score_str="highest_score: "+high_score_str
        self.high_score_image=self.font.render(high_score_str,True,self.text_color,self.ai_settings.bg_color)

        #最高得分放在屏幕顶部中央
        self.high_score_rect=self.high_score_image.get_rect()
        self.high_score_rect.centerx=self.screen_rect.centerx
        self.high_score_rect.top=self.score_rect.top

    def prep_level(self):
        level_str="level: "+str(self.stats.level)
        self.level_image=self.font.render(level_str,True,self.text_color,self.ai_settings.bg_color)

        #等级放在得分下方
        self.level_rect=self.level_image.get_rect()
        self.level_rect.right=self.score_rect.right
        self.level_rect.top=self.score_rect.bottom+10

    def prep_ships(self):
        #剩余飞船数目
        self.ships=Group()
        for ship_number in range(self.stats.ship_left):
            ship=Ship(self.ai_settings,self.screen)
            ship.rect.x=10+ship_number*ship.rect.width
            ship.rect.y=10
            self.ships.add(ship)


    def show_score(self):
        #显示当前和最高得分,等级
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)
