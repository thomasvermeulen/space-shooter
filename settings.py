import pygame
pygame.init()

S_WIDTH = 600 # Display breedte
S_HEIGHT = 700 # Display hoogte
FPS = 60

screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
clock = pygame.time.Clock()

icon = pygame.image.load('assets/char_assets/spaceship_icon.png') 
bg = pygame.image.load('assets/background.png') 
bg = pygame.transform.scale(bg, (S_WIDTH, S_HEIGHT))
font = pygame.font.Font('assets/Symtext.ttf', 30)
font1 = pygame.font.Font('assets/Symtext.ttf', 60)

pygame.display.set_caption('Shooter')
pygame.display.set_icon(icon)

player_img = pygame.image.load('assets/char_assets/ship.png')
player_img = pygame.transform.scale(player_img, (50, 50))
bullet_img = pygame.image.load('assets/char_assets/bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (50, 50))
alien_img = [pygame.image.load(f'assets/enemy_assets/enemy{i}.png') for i in range (1,4)]
alien_bullet_img = pygame.image.load('assets/enemy_assets/bullet.png')
heart_img = pygame.image.load('assets/char_assets/heart.png')
heart_img = pygame.transform.scale(heart_img, (50, 50))

bullet_sound = pygame.mixer.Sound('sounds/laser.mp3')
explosion_sound = pygame.mixer.Sound('sounds/explosion.mp3')
player_hit_sound = pygame.mixer.Sound('sounds/player_hit.mp3')
gameover_sound = pygame.mixer.Sound('sounds/game_over.mp3')
gameover_sound.set_volume(3.0)

x = 0
y = 0
width = 50
height = 50
vel = 5
score = 0

aliens = []
bullets = []
alien_bullets = []
bullet_counter = 0
alien_bullet_cooldown = 1000

alien_last_shot = pygame.time.get_ticks()

alien_rows = 5
alien_cols = 5
