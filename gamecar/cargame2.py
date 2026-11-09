import os
import sys
import random
import pygame

pygame.init()
WIN_WIDTH = 800
WIN_HEIGHT = 600
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Моя игра: Прыжок и Машины")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ЗАГРУЗКА ИЗОБРАЖЕНИЯ ИГРОКА
player_path = os.path.join(BASE_DIR, "car.png")
if os.path.exists(player_path):
    player_img = pygame.image.load(player_path).convert_alpha()
    player_img = pygame.transform.scale(player_img, (100, 50))
else:
    player_img = pygame.Surface((100, 50), pygame.SRCALPHA)
    pygame.draw.rect(player_img, (46, 204, 113), (0, 0, 100, 50), border_radius=8)

# ЗАГРУЗКА ИЗОБРАЖЕНИЯ ВРАГА
enemy_path = os.path.join(BASE_DIR, "enemy.png")
if os.path.exists(enemy_path):
    enemy_img = pygame.image.load(enemy_path).convert_alpha()
    enemy_img = pygame.transform.scale(enemy_img, (90, 45))
else:
    enemy_img = pygame.Surface((90, 45), pygame.SRCALPHA)
    pygame.draw.rect(enemy_img, (231, 76, 60), (0, 0, 90, 45), border_radius=8)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5

        self.is_jumping = False
        self.jump_velocity = 0
        self.gravity = 0.8
        self.jump_power = -14
        self.ground_y = y

    def update(self):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WIN_WIDTH:
            self.rect.x += self.speed

        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = self.jump_power
            self.ground_y = self.rect.y

        if not self.is_jumping:
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 0:
                self.rect.y -= self.speed
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < WIN_HEIGHT:
                self.rect.y += self.speed

        if self.is_jumping:
            self.rect.y += self.jump_velocity
            self.jump_velocity += self.gravity

            if self.rect.y >= self.ground_y:
                self.rect.y = self.ground_y
                self.is_jumping = False
            elif self.rect.top <= 0:
                self.rect.top = 0
                self.jump_velocity = 0


class EnemyCar(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.reset_pos()

    def reset_pos(self):
        self.rect.x = random.randint(WIN_WIDTH, WIN_WIDTH + 400)
        self.rect.y = random.randint(50, WIN_HEIGHT - self.rect.height - 50)
        self.speed_x = random.randint(5, 9)

    def update(self):
        self.rect.x -= self.speed_x

        if self.rect.right < 0:
            self.reset_pos()


def main():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)

    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    player = Player(100, WIN_HEIGHT - 100, player_img)
    all_sprites.add(player)

    for _ in range(4):
        obs = EnemyCar(enemy_img)
        all_sprites.add(obs)
        obstacles.add(obs)

    score = 0

    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        all_sprites.update()
        score += 1

        if pygame.sprite.spritecollide(player, obstacles, False):
            print(f"Столкновение! Итоговый счёт: {score // 10}")
            player.rect.topleft = (100, WIN_HEIGHT - 100)
            player.is_jumping = False
            score = 0

        win.fill((50, 50, 50))
        all_sprites.draw(win)

        score_surface = font.render(f"Очки: {score // 10}", True, (255, 255, 255))
        win.blit(score_surface, (10, 10))

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()