import pygame
import math

# Инициализация Pygame
pygame.init()

# Определение констант
WIDTH = 800
HEIGHT = 600
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 120
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
DELTA_ANGLE = FOV / NUM_RAYS
PLAYER_POS = (400, 300)
PLAYER_ANGLE = 0
PLAYER_SPEED = 5
ZOMBIE_SPEED = 2
ZOMBIE_HEALTH = 3
ZOMBIE_DAMAGE = 1
BULLET_SPEED = 10
BULLET_DAMAGE = 1
MAX_BULLETS = 10

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Shooter")

# Загрузка изображений
player_img = pygame.image.load("player.png").convert_alpha()
zombie_img = pygame.image.load("zombie.png").convert_alpha()
bullet_img = pygame.image.load("bullet.png").convert_alpha()

# Создание групп спрайтов
player_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

# Создание классов
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = PLAYER_POS
        self.angle = PLAYER_ANGLE

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle += math.radians(5)
        if keys[pygame.K_RIGHT]:
            self.angle -= math.radians(5)
        if keys[pygame.K_UP]:
            dx = PLAYER_SPEED * math.cos(self.angle)
            dy = PLAYER_SPEED * math.sin(self.angle)
            self.rect.move_ip(dx, dy)
        if keys[pygame.K_DOWN]:
            dx = -PLAYER_SPEED * math.cos(self.angle)
            dy = -PLAYER_SPEED * math.sin(self.angle)
            self.rect.move_ip(dx, dy)

class Zombie(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = zombie_img
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.health = ZOMBIE_HEALTH

    def update(self):
        dx = PLAYER_POS[0] - self.rect.centerx
        dy = PLAYER_POS[1] - self.rect.centery
        dist = math.hypot(dx, dy)
        dx = dx / dist * ZOMBIE_SPEED
        dy = dy / dist * ZOMBIE_SPEED
        self.rect.move_ip(dx, dy)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.angle = angle
        self.damage = BULLET_DAMAGE

    def update(self):
        dx = BULLET_SPEED * math.cos(self.angle)
        dy = BULLET_SPEED * math.sin(self.angle)
        self.rect.move_ip(dx, dy)

# Создание объектов
player = Player()
player_group.add(player)

for i in range(5):
    zombie = Zombie((i * 150 + 100, i * 100 + 100))
    zombie_group.add(zombie)

# Основной игровой цикл
while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if len(bullet_group) < MAX_BULLETS:
                bullet = Bullet(player.rect.center, player.angle)
                bullet_group.add(bullet)

    # Обновление объектов
    player.update()
    zombie_group.update()
    bullet_group.update()

    # Отрисовка стен
    for i in range(NUM_RAYS):
        angle = player.angle - HALF_FOV + i * DELTA_ANGLE
        sin_angle = math.sin(angle)
        cos_angle = math.cos(angle)
        for j in range(1, int(DIST)):
            x = int(player.rect.centerx + j * cos_angle)
            y = int(player.rect.centery + j * sin_angle)
            if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
                break
            if wall_map[y][x] == 1:
                height = HEIGHT / (2 * j * math.cos(angle - player.angle))
                color = (255, 255, 255)
                pygame.draw.line(screen, color, (i, HEIGHT / 2 - height), (i, HEIGHT / 2 + height))

    # Отрисовка объектов
    screen.fill((0, 0, 0))
    player_group.draw(screen)
    zombie_group.draw(screen)
    bullet_group.draw(screen)

    # Обработка столкновений
    for zombie in zombie_group:
        if pygame.sprite.collide_rect(player, zombie):
            player.health -= ZOMBIE_DAMAGE
            if player.health <= 0:
                pygame.quit()
                sys.exit()
        for bullet in bullet_group:
            if pygame.sprite.collide_rect(zombie, bullet):
                zombie.health -= bullet.damage
                bullet_group.remove(bullet)
                if zombie.health <= 0:
                    zombie_group.remove(zombie)

    # Обновление экрана
    pygame.display.flip()