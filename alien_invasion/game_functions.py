import sys

import pygame

from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    # 键盘按下左右移动
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event,ship):
    # 键盘抬起停止左右移动
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    #监控鼠标和键盘事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type== pygame.MOUSEBUTTONDOWN:
            mouse_x , mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type ==pygame.KEYUP:
            check_keyup_events(event,ship)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    #单击play并处于非活动状态时开始游戏
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计
        stats.reset_stats()
        stats.game_active=True

        #重置记分牌
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #清空外星人子弹列表
        aliens.empty()
        bullets.empty()

        #创建外星人，飞船居中
        creat_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

def check_high_score(stats,sb):
    if stats.score > stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    # 检测发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)


    #外星人全部被射杀后重新创建，删除子弹,加速外星人，提高等级
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level+=1
        sb.prep_level()
        creat_fleet(ai_settings, screen, ship, aliens)


def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    #更新子弹的位置，删除已经消失的子弹
    bullets.update()

    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

def fire_bullet(ai_settings,screen,ship,bullets):
    #子弹数目小于规定值可以发射
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings,alien_width):
    #获得一行容纳多少个
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    #获得外星人行数
    available_space_y=ai_settings.screen_height-ship_height-3*alien_height
    number_rows=int(available_space_y/(2*alien_height))
    return number_rows

def creat_alien(ai_settings,screen,aliens,alien_number,row_number):
    #确定某外星人的位置
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)


def creat_fleet(ai_settings,screen,ship,aliens):
    #创建外星人群，用for循环嵌套显示
    alien=Alien(ai_settings,screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            creat_alien(ai_settings, screen, aliens, alien_number,row_number)

def check_fleet_edges(ai_settings,aliens):
    #测试外星人群组中是否有碰到边缘的
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    #整群外星人下移并改变方向
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1

def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
    #检测外星人是否到屏幕边缘
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

    #检测外星人与飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)

    #检测是否有飞船到底端
    check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)

def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
    if stats.ship_left>0:
        # 发生碰撞，余下飞船-1
        stats.ship_left -= 1

        #更新记分牌
        sb.prep_ships()

        # 清空子弹和外星人
        bullets.empty()
        aliens.empty()

        # 重新创建外星人,飞船居中
        creat_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
            break


def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,paly_button):
    #更新屏幕图像
    screen.fill(ai_settings.bg_color)
    ship.blitme()

    #绘制子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    #最后绘制外星人
    aliens.draw(screen)

    #绘制得分
    sb.show_score()

    # 非活动状态设置paly按钮
    if not stats.game_active:
        paly_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()