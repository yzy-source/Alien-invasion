import sys

import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf
from alien import Alien

def run_game():
    #初始化背景
    pygame.init()
    #创建显示窗口
    ai_settings=Settings()
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #创建一搜飞船
    ship=Ship(ai_settings,screen)
    #创建子弹编组
    bullets=Group()
    #创建外星人
    aliens=Group()
    gf.creat_fleet(ai_settings,screen,ship,aliens)
    #创建游戏统计信息实例
    stats=GameStats(ai_settings)
    #创建paly按钮
    play_button=Button(ai_settings,screen,"Play")
    #创建记分牌
    sb=Scoreboard(ai_settings,screen,stats)

    #游戏主循环
    while True:
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen,stats,sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings,screen, stats, sb, ship, aliens, bullets)

        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)

run_game()