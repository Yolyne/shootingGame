import pygame
import random

# 初期設定
WIDTH = 800
HEIGHT = 600
FPS = 60

# 色の定義
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 弾の発射間隔（ミリ秒）
SHOOT_DELAY = 100
PLAYER_XSPEED = 10
PLAYER_YSPEED = 10

# Pygameの初期化とウィンドウの作成
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("アクションゲーム")
clock = pygame.time.Clock()

# キャラクターのクラス
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.last_shot_time = 0  # 最後の弾の発射時刻

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -PLAYER_XSPEED
        if keystate[pygame.K_RIGHT]:
            self.speedx = PLAYER_XSPEED
        self.rect.x += self.speedx
        if keystate[pygame.K_UP]:
            self.speedy = -PLAYER_YSPEED
        if keystate[pygame.K_DOWN]:
            self.speedy = PLAYER_YSPEED
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

        # スペースキーが押されている間は弾を発射
        if keystate[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > SHOOT_DELAY:
                self.shoot()
                self.last_shot_time = current_time

    def shoot(self):
        if score > 50:
            bullet = [
                Bullet(self.rect.centerx, self.rect.top),
                Bullet(self.rect.left, self.rect.top),
                Bullet(self.rect.right, self.rect.top),
            ]
        else:
            bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def kill(self):
        self.rect.x = -100
        all_sprites.add(self)  # プレイヤーを再度スプライトグループに追加


# 障害物のクラス
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = 1 + score*0.02
        # self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = 1 + score*0.02
            # self.speedy = random.randrange(1, 8)


# 弾のクラス
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


score = 0
score_font = pygame.font.Font(None, 36)


def draw_score():
    score_text = score_font.render("Score: " + str(score), True, WHITE)
    score_rect = score_text.get_rect()
    score_rect.topright = (WIDTH - 10, 10)
    screen.blit(score_text, score_rect)


# スプライトグループの作成
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# プレイヤーオブジェクトの作成
player = Player()
all_sprites.add(player)

# リトライボタンのフォントとテキストの設定
font = pygame.font.Font(None, 36)
retry_text = font.render("Retry", True, WHITE)
retry_rect = retry_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))

# ゲームループ
running = True
game_over = False
show_retry = False
paused = False  # ゲームが一時停止中かどうかのフラグ
while running:
    if game_over:
        score = 0
        if not show_retry:
            screen.fill((0, 0, 0))
            game_over_text = font.render("Game Over", True, WHITE)
            game_over_rect = game_over_text.get_rect(
                center=(WIDTH / 2, HEIGHT / 2 - 50)
            )
            screen.blit(game_over_text, game_over_rect)
            screen.blit(retry_text, retry_rect)
            pygame.display.flip()
            show_retry = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if retry_rect.collidepoint(event.pos):
                    all_sprites.empty()
                    obstacles.empty()
                    bullets.empty()
                    player = Player()
                    all_sprites.add(player)
                    game_over = False
                    show_retry = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    all_sprites.empty()
                    obstacles.empty()
                    bullets.empty()
                    player = Player()
                    all_sprites.add(player)
                    game_over = False
                    show_retry = False

    elif paused:
        all_sprites.draw(screen)
        s = pygame.Surface((WIDTH, HEIGHT))
        s.fill((0,0,0))
        s.set_alpha(180)  # this fills the entire surface
        screen.blit(s, (0,0))
        draw_score()
        paused_text = font.render("Paused", True, WHITE)
        paused_rect = paused_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(paused_text, paused_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_SPACE):
                    paused = False

    else:
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # 更新処理
        all_sprites.update()

        # 衝突判定（障害物とプレイヤー）
        hits = pygame.sprite.spritecollide(player, obstacles, False)
        if hits:
            player.kill()
            game_over = True

        # 衝突判定（弾と障害物）
        hits = pygame.sprite.groupcollide(bullets, obstacles, True, True)

        # スコアの更新
        score += len(hits)

        # 障害物生成
        while len(obstacles) < 8:
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)

        # 画面の描画
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        draw_score()

    # 画面更新
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
