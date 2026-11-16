import pygame, sys, os, random, math, array

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SteelBallRunGame")
clock, FPS = pygame.time.Clock(), 60

if os.path.exists("sound.mp3"):
    pygame.mixer.music.load("sound.mp3")
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(-1)

hoof_sound = pygame.mixer.Sound("gal.mp3") if os.path.exists("gal.mp3") else None

def make_sound(freq_func, duration):
    sr = 22050
    buf = array.array('h')
    for i in range(int(sr * duration)):
        t = i / sr
        val = int(freq_func(t) * 15000 * (1 - t / duration))
        buf.append(val);
        buf.append(val)
    return pygame.mixer.Sound(buf)

snd_coin = make_sound(lambda t: math.sin(2 * math.pi * 987.77 * t), 0.12)
snd_shoot = make_sound(lambda t: math.sin(2 * math.pi * (600 * (1 - t / 0.08)) * t), 0.08)

try:
    font = pygame.font.SysFont("Arial", 28, bold=True)
except:
    font = pygame.font.Font(None, 28)

score, money, x, y, direction, anim_frame = 0, 0, 400, 300, 1, 0.0
base_speed, boost_speed, was_moving = 5, 9, False
SPR_W, SPR_H = 180, 135

player_bullets, enemy_bullets, enemies, coins = [], [], [], []

def load_img(name, w, h):
    if os.path.exists(name):
        img = pygame.image.load(name).convert_alpha()
        return pygame.transform.scale(img, (w, h))
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.ellipse(surf, (178, 34, 34), (10, 30, w - 20, h - 60))
    return surf

frames = [load_img(f"{i}.png", SPR_W, SPR_H) for i in range(1, 17)]

class Coin:
    def __init__(self, cx, cy):
        self.x, self.y, self.offset = cx, cy, random.random() * 6.28

    def draw(self, surf, fc):
        dy = int(math.sin(fc * 0.1 + self.offset) * 3)
        pygame.draw.circle(surf, (218, 165, 32), (int(self.x), int(self.y + dy)), 12)
        pygame.draw.circle(surf, (255, 215, 0), (int(self.x), int(self.y + dy)), 10)
        surf.blit(font.render("$", True, (139, 69, 19)), (self.x - 5, self.y + dy - 10))

class Horse1:
    def __init__(self):
        self.respawn()
        self.img = load_img("horse1.png", SPR_W, SPR_H)

    def respawn(self):
        self.x, self.y = random.randint(150, WIDTH - 150), random.randint(150, HEIGHT - 150)
        self.dx, self.dy = random.choice([-3, 3]), random.choice([-2, 2])
        self.timer, self.state, self.respawn_t = random.randint(30, 90), "alive", 0

    def update(self, px, py):
        if self.state == "respawning":
            self.respawn_t -= 1
            if self.respawn_t <= 0: self.respawn()
            return None
        self.x += self.dx;
        self.y += self.dy
        if self.x < SPR_W // 2 or self.x > WIDTH - SPR_W // 2: self.dx *= -1
        if self.y < SPR_H // 2 + 100 or self.y > HEIGHT - SPR_H // 2: self.dy *= -1
        self.timer -= 1
        if self.timer <= 0:
            self.timer = random.randint(60, 120)
            angle = math.atan2(py - self.y, px - self.x)
            return {'x': self.x, 'y': self.y, 'dx': math.cos(angle) * 5, 'dy': math.sin(angle) * 5}
        return None

    def draw(self, surf):
        if self.state == "alive":
            img = pygame.transform.flip(self.img, True, False) if self.dx < 0 else self.img
            surf.blit(img, (int(self.x - SPR_W // 2), int(self.y - SPR_H // 2)))

class Horse2:
    def __init__(self):
        self.active, self.x, self.y, self.dx = False, 0, 0, 0
        self.timer, self.img = random.randint(300, 600), load_img("horse2.png", SPR_W, SPR_H)

    def update(self):
        if not self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active, self.y = True, random.choice([100, HEIGHT - 100])
                self.x, self.dx = (-100, 7) if random.choice([True, False]) else (WIDTH + 100, -7)
        else:
            self.x += self.dx
            if self.x < -150 or self.x > WIDTH + 150:
                self.active, self.timer = False, random.randint(400, 800)

    def draw(self, surf):
        if self.active:
            img = pygame.transform.flip(self.img, True, False) if self.dx < 0 else self.img
            surf.blit(img, (int(self.x - SPR_W // 2), int(self.y - SPR_H // 2)))

for _ in range(3): enemies.append(Horse1())
horse2 = Horse2()

def draw_desert(surf):
    surf.fill((255, 215, 0))
    pygame.draw.rect(surf, (255, 140, 0), (0, 0, WIDTH, 250))
    pygame.draw.circle(surf, (255, 255, 224), (650, 100), 50)
    pygame.draw.ellipse(surf, (218, 165, 32), (-100, 180, 1000, 300))
    pygame.draw.ellipse(surf, (238, 203, 173), (200, 320, 700, 400))

running, fc = True, 0
while running:
    fc += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player_bullets.append({'x': x, 'y': y, 'dx': 15 * direction})
            snd_shoot.play()

    keys = pygame.key.get_pressed()
    speed = boost_speed if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) else base_speed
    dx = speed * ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a]))
    dy = speed * ((keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w]))

    if dx != 0: direction = 1 if dx > 0 else -1
    x = max(SPR_W // 2, min(WIDTH - SPR_W // 2, x + dx))
    y = max(SPR_H // 2 + 100, min(HEIGHT - SPR_H // 2, y + dy))

    is_moving = (dx != 0 or dy != 0)
    if is_moving:
        anim_frame += 0.5 if speed == boost_speed else 0.3
        if not was_moving and hoof_sound: hoof_sound.play(loops=-1)
    else:
        anim_frame = 0
        if was_moving and hoof_sound: hoof_sound.stop()
    was_moving = is_moving

    for b in player_bullets[:]:
        b['x'] += b['dx']
        if not (0 <= b['x'] <= WIDTH): player_bullets.remove(b)

    for en in enemies:
        eb = en.update(x, y)
        if eb: enemy_bullets.append(eb)

    for eb in enemy_bullets[:]:
        eb['x'] += eb['dx'];
        eb['y'] += eb['dy']
        if not (0 <= eb['x'] <= WIDTH and 0 <= eb['y'] <= HEIGHT): enemy_bullets.remove(eb)

    horse2.update()

    for b in player_bullets[:]:
        for en in enemies:
            if en.state == "alive" and abs(b['x'] - en.x) < 40 and abs(b['y'] - en.y) < 30:
                if b in player_bullets: player_bullets.remove(b)
                score += 1
                coins.append(Coin(en.x, en.y))
                en.state, en.respawn_t = "respawning", 180
                break

    for c in coins[:]:
        if math.hypot(x - c.x, y - c.y) < 45:
            money += 10;
            coins.remove(c);
            snd_coin.play()

    draw_desert(screen)
    for c in coins: c.draw(screen, fc)
    for en in enemies: en.draw(screen)
    horse2.draw(screen)

    for b in player_bullets:
        pygame.draw.circle(screen, (0, 100, 0), (int(b['x']), int(b['y'])), 8)
        pygame.draw.circle(screen, (50, 205, 50), (int(b['x']), int(b['y'])), 6)
    for eb in enemy_bullets:
        pygame.draw.circle(screen, (139, 0, 0), (int(eb['x']), int(eb['y'])), 5)

    cur_img = frames[int(anim_frame) % len(frames)]
    if direction == -1: cur_img = pygame.transform.flip(cur_img, True, False)
    screen.blit(cur_img, (int(x - SPR_W // 2), int(y - SPR_H // 2)))

    for text, pos in [(f"Убийств: {score}", (20, 15)), (f"Деньги: ${money}", (20, 45))]:
        screen.blit(font.render(text, True, (0, 0, 0)), (pos[0] + 2, pos[1] + 2))
        screen.blit(font.render(text, True, (255, 255, 255) if pos[1] == 15 else (255, 215, 0)), pos)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()