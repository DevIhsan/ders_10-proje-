import pygame
import random

# Ekran boyutları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.bottom = SCREEN_HEIGHT
        self.speed_y = 0

    def update(self):
        self.speed_y += 0.5
        self.rect.y += self.speed_y
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.speed_y = 0

    def jump(self):
        if self.rect.bottom == SCREEN_HEIGHT:
            self.speed_y = -10

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = SCREEN_WIDTH
        self.rect.bottom = SCREEN_HEIGHT - 50 - random.randint(0, 200)  # Engellerin daha aşağıda başlaması için rastgele bir yükseklik ekledik
        self.speed_x = -5

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
            self.rect.bottom = SCREEN_HEIGHT - 50 - random.randint(0, 200)  # Yeni engel oluşturulduğunda yükseklik rastgele olarak değişir

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dinozor Kaçış Oyunu")

all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

dinosaur = Dinosaur()
all_sprites.add(dinosaur)

clock = pygame.time.Clock()
obstacle_spawn_timer = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dinosaur.jump()

    all_sprites.update()

    obstacle_spawn_timer += 1
    if obstacle_spawn_timer == 60:  # 1 saniyede bir engel oluştur
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)
        obstacle_spawn_timer = 0

    # Dinozorun engellerle çarpışıp çarpmadığını kontrol et
    hits = pygame.sprite.spritecollide(dinosaur, obstacles, False)
    if hits:
        running = False

    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
