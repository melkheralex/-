import os
import sys
import pygame

pygame.init()
WIN_WIDTH = 800
WIN_HEIGHT = 600
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Моя игра")

# Автоматический поиск файла car с любым расширением (.png, .jpg, .jpeg)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
car_img = None

for ext in [".jpg", ".png", ".jpeg", ".webp"]:
    path = os.path.join(BASE_DIR, f"car{ext}")
    if os.path.exists(path):
        car_img = pygame.image.load(path).convert_alpha() if ext == ".png" else pygame.image.load(path).convert()
        print(f"Загружен файл: {path}")
        break

if car_img is None:
    print("Файл car не найден! Используется красная заглушка.")
    car_img = pygame.Surface((100, 50))
    car_img.fill((255, 0, 0))

CAR_WIDTH = 100
CAR_HEIGHT = 50
car_img = pygame.transform.scale(car_img, (CAR_WIDTH, CAR_HEIGHT))

x = 350
y = 250
speed = 5
clock = pygame.time.Clock()

run = True
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and x > 0:
        x -= speed
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and x < WIN_WIDTH - CAR_WIDTH:
        x += speed
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and y > 0:
        y -= speed
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and y < WIN_HEIGHT - CAR_HEIGHT:
        y += speed

    win.fill((50, 50, 50))
    win.blit(car_img, (x, y))
    pygame.display.update()

pygame.quit()
sys.exit()