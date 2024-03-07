"""
教材「Python でゲーム開発」で使用するシューティングゲームのソースコードです。

"""
# 1 - インポート
import sys
import random
import pygame
from pygame.locals import *
from pygame import mixer
import math

# 2 - ゲームの初期化
pygame.init()
mixer.init()
WIDTH = 400

# ↓ ディスプレイ画面が小さい場合は、HEIGHT = 600に設定してください。
# HEIGHT = 600

# ↓ ディスプレイ画面が大きい場合は、HEIGHT = 800に設定してください。
HEIGHT = 800

p_x, p_y = (200,400)
screen = pygame.display.set_mode((WIDTH,HEIGHT))

# 2.1 player に関する設定
p_v = 3

# 2.2 player の laser に関する設定
p_lasers=[]
p_laser_v = 5

# 2.3 enemy に関する設定
enemies=[]
enemy_frequency = 100
enemy_timer = enemy_frequency
e_v = 1
enemies_max_len = 10

# 2.4 enemy の laser に関する設定
e_lasers=[]
e_laser_frequency = 100
e_laser_timer = e_laser_frequency
e_laser_v = 2

# 2.5 castle に関する設定
castle_size = (64,64)
positions = [(0,500),(100,500),(200,500),(300,500)]
castle_hp_init = 5
castle_hp_list = [castle_hp_init] * 4
castles_rect = [pygame.Rect(positions[i],castle_size) for i in range(4)]

# 2.6 文字に関する設定
font_hp = pygame.font.Font(None, 55)
font_clock = pygame.font.Font(None, 100)
font_counter = pygame.font.Font(None, 45)
font_top = pygame.font.Font(None, 40)
font_score = pygame.font.Font(None, 50)

# 2.7 タイマーに関する設定
GAME_TIME = 30000
timer_height = 70
start_time = 0

# 2.8 画面遷移に関する設定
# 0 -> 「TOP」, 1 -> 「PLAY」, 2 -> 「SCORE」
scene = 0

# 3 - 画像の読み込み
player = pygame.image.load("resources/images/player.png")
p_laser_surface = pygame.image.load("resources/images/p_laser.png") #2
enemy_surface = pygame.image.load("resources/images/enemy.png") #3
e_laser_surface = pygame.image.load("resources/images/e_laser.png") #3
castle = pygame.image.load("resources/images/castle.png")

# 3.1 - 画像のサイズ
p_width = player.get_width()
p_height = player.get_height()
p_laser_width = p_laser_surface.get_width()
p_laser_height = p_laser_surface.get_height()
e_width = enemy_surface.get_width()
e_height = enemy_surface.get_height()
e_laser_width = e_laser_surface.get_width()
e_laser_height = e_laser_surface.get_height()

# 3.2 - 各種カウンター
p_laser_counter = 0
p_hit_enemy_counter = 0
fight_time_counter = 0

# 3.3 - bgm の再生
# ↓ windows環境では起動しない可能性あり
mixer.music.load("resources/bgm/bgm01.mp3")
mixer.music.play(-1)

# 3.4 - スコアの計算
def calc_score(result, hit_rate, result_hp, fight_time_counter):
    score = 0
    score += result * 100
    score += hit_rate * 100
    score += result_hp * 10
    score += fight_time_counter * 5
    return math.floor(score)

# 4 - ループの実行
while True:

    # 5 - 画面を一度消す
    screen.fill(0)

    # 5.1 - 「TOP」画面
    if scene == 0:
        text = font_top.render("Start Game with ENTER", False, (255, 255, 255))
        screen.blit(text, (20, HEIGHT / 2))

    # 5.2 - 「PLAY」画面
    if scene == 1:

        # 6 - 画面に描画する
        screen.blit(player,(p_x,p_y))

        # 6.1 player の レーザーを描画(#2)
        for p_laser_i, p_laser in enumerate(p_lasers):
            p_laser[1] -= p_laser_v

            if p_laser[1] < -p_laser_height:   #2
                p_lasers.pop(p_laser_i)        #2

            screen.blit(p_laser_surface,p_laser)

        # 6.2 敵描画
        enemy_timer -= 1
        if enemy_timer <= 0 and len(enemies) < enemies_max_len:
            enemies.append([random.randint(0, WIDTH - e_width), -e_height + timer_height])
            enemy_timer = enemy_frequency

        for enemy_i, enemy in enumerate(enemies):
            enemy[1] += e_v
            if enemy[1] > HEIGHT:
                enemies.pop(enemy_i)
            screen.blit(enemy_surface,enemy)

            # 6.2.1 - e_lasers へ追加
            e_laser_timer -= 1
            if e_laser_timer <= 0:
                e_lasers.append([enemy[0]+ e_width/2 - e_laser_width/2, enemy[1] + e_laser_height])
                e_laser_timer = e_laser_frequency

            # 6.2.2 - player の攻撃によって敵を削除
            enemy_rect = pygame.Rect(enemy_surface.get_rect())
            enemy_rect.left, enemy_rect.top = enemy

            for p_laser_i, p_laser in enumerate(p_lasers):
                p_raser_rect = pygame.Rect(p_laser_surface.get_rect())
                p_raser_rect.left, p_raser_rect.top = p_laser

                if enemy_rect.colliderect(p_raser_rect):
                    enemies.pop(enemy_i)
                    p_lasers.pop(p_laser_i)
                    p_hit_enemy_counter += 1

        # 6.3 - 敵のレーザー描画
        for e_laser_i, e_laser in enumerate(e_lasers):
            e_laser[1] += e_laser_v
            if e_laser[1] < 0 or e_laser[1] > HEIGHT:
                e_lasers.pop(e_laser_i)
            screen.blit(e_laser_surface,e_laser)

            # 6.3.1 - enemy の攻撃によって城にダメージ
            e_laser_rect = pygame.Rect(e_laser_surface.get_rect())
            e_laser_rect.left, e_laser_rect.top = e_laser

            for castle_i in range(4):
                if e_laser_rect.colliderect(castles_rect[castle_i]):
                    if(castle_hp_list[castle_i] > 0):
                        e_lasers.pop(e_laser_i)
                        castle_hp_list[castle_i] -= 1

        # 6.4 castle を描画
        for castle_i in range(4):
            if(castle_hp_list[castle_i] > 0):
                screen.blit(castle,positions[castle_i])
                #6.4.1 HP を表示
                hp = castle_hp_list[castle_i]
                hp_text = '*' * hp
                text = font_hp.render(hp_text, False,(255,255,255))

                hp_position = [positions[castle_i][0], positions[castle_i][1] + castle_size[1]]
                screen.blit(text, hp_position)

        # 6.5 ゲームタイマーを表示
        pygame.draw.rect(screen, (40, 40, 40), Rect(0, 0, WIDTH, timer_height))
        now_time = pygame.time.get_ticks() - start_time
        fight_time_counter = now_time / 1000
        left_time = (GAME_TIME - now_time) // 1000 if (GAME_TIME - now_time) >= 0 else 0
        time_text = font_clock.render(str(left_time),False,(0,0,255))
        screen.blit(time_text,(0,0))
        lasers_text = font_counter.render("lasers : " + str(p_laser_counter), False, (255, 255, 255))
        screen.blit(lasers_text, (100, 20))
        hit_text = font_counter.render("hit : " + str(p_hit_enemy_counter), False, (255, 255, 255))
        screen.blit(hit_text, (270, 20))

        # 6.6 - スコア画面への遷移
        if sum(castle_hp_list) <= 0 or left_time <= 0:
            scene = 2

    # 5.3 - 「SCORE」画面
    if scene == 2:
        # 5.3.1 - 勝敗を表示
        result = 1 if sum(castle_hp_list) > 0 else 0

        result_char = "Win" if result else "Lose"
        result_text = font_score.render(result_char, False, (0, 0, 255))
        screen.blit(result_text, (20, 20))

        # 5.3.2 - 命中率を表示
        try:
            hit_rate = p_hit_enemy_counter / p_laser_counter
        except ZeroDivisionError:
            hit_rate = 0
        hit_percent = "{:.0%}".format(hit_rate)
        hit_rate_text = font_score.render(
            "Hit Rate : " + hit_percent, False, (255, 255, 255)
        )
        screen.blit(hit_rate_text, (20, 100))

        # 5.3.3 - 城の残りの HP を表示
        result_hp = sum(castle_hp_list)
        result_hp_text = font_score.render(
            "Remaining HP : " + str(result_hp), False, (255, 255, 255)
        )
        screen.blit(result_hp_text, (20, 200))

        # 5.3.4 - プレイ時間を表示
        result_time_text = font_score.render(
            "Fight Time : " + str(fight_time_counter), False, (255, 255, 255)
        )
        screen.blit(result_time_text, (20, 300))

        # 5.3.5 - スコアを表示
        score = calc_score(result, hit_rate, result_hp, fight_time_counter)
        score_text = font_score.render("Score : " + str(score), False, (255, 217, 0))
        screen.blit(score_text, (20, 400))

        # 5.3.6 - ガイド文章を表示
        guid_text = font_score.render("TOP [t] , REPLAY [r]", False, (255, 255, 255))
        screen.blit(guid_text, (20, 500))

    # 7 - 画面を更新する
    pygame.display.flip()
    pygame.time.wait(20)

    # 8 - イベントを確認
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_RETURN and scene == 0:
                start_time = pygame.time.get_ticks()
                scene = 1
            if event.key == K_SPACE and scene == 1:
                p_lasers.append([p_x + p_width/2 - p_laser_width/2, p_y - p_laser_height])
                p_laser_counter += 1
                # ↓ windows環境では起動しない可能性あり
                p_laser_sound = mixer.Sound("./resources/se/p_laser.mp3")
                p_laser_sound.play()

            if event.key == K_t and scene == 2:
                castle_hp_list = [castle_hp_init] * 4
                p_laser_counter = 0
                p_hit_enemy_counter = 0
                p_lasers = []
                enemies = []
                e_lasers = []
                p_x, p_y = (200,400)
                scene = 0

            if event.key == K_r and scene == 2:
                start_time = pygame.time.get_ticks()
                castle_hp_list = [castle_hp_init] * 4
                p_laser_counter = 0
                p_hit_enemy_counter = 0
                p_lasers = []
                enemies = []
                e_lasers = []
                p_x, p_y = (200,400)
                scene = 1

    # 9 - player の動作
    pressed_key = pygame.key.get_pressed()
    if pressed_key[K_LEFT] and scene == 1:
        if p_x > 0:
            p_x -= p_v
    if pressed_key[K_RIGHT] and scene == 1:
        if p_x < WIDTH - p_width:
            p_x += p_v
    if pressed_key[K_UP] and scene == 1:
        if p_y > timer_height:
            p_y -= p_v
    if pressed_key[K_DOWN] and scene == 1:
        if p_y < HEIGHT - p_height:
            p_y += p_v