import pygame, random, time
from settings import *

pygame.init()

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.vel = 6
        self.rect = (self.x, self.y, self.width, self.height)
        self.health = 1
        self.alive = True
        self.hitbox = pygame.Rect(self.rect)
    
    def draw(self, window):
        if self.health > 0:
            window.blit(player_img, (self.x, self.y))
            self.rect = (self.x, self.y, self.width, self.height)
            self.hitbox = pygame.Rect(self.rect)

player = Player(round(S_WIDTH / 2) - 20, S_HEIGHT - 100)

class PlayerBullet():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 10
        self.width = 10
        self.vel = 3
        self.rect = (self.x, self.y, self.width, self.height)
        self.bullet_hitbox = pygame.Rect(self.rect)
    
    def draw(self, window):
        self.y -= self.vel
        window.blit(bullet_img, (self.x, self.y))
        self.rect = (self.x, self.y, self.width, self.height)
        self.bullet_hitbox = pygame.Rect(self.rect)

class Aliens():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 50
        self.width = 50
        self.image = alien_img[random.randint(0, 2)]
        self.rect = (self.x, self.y, self.width, self.height)
        self.move_counter = 0
        self.direction = 1
        self.rect = (self.x, self.y, self.width, self.height)
        self.alien_hitbox = pygame.Rect(self.rect)
    
    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        self.x += self.direction
        self.move_counter += 1
        if abs(self.move_counter) > 100:
            self.direction *= -1
            self.move_counter *= self.direction
        self.rect = (self.x, self.y, self.width, self.height)
        self.alien_hitbox = pygame.Rect(self.rect)

class AlienBullet():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 10
        self.width = 10
        self.vel = 7
        self.rect = (self.x, self.y, self.width, self.height)
        self.alien_bullet_hitbox = pygame.Rect(self.rect)
    
    def draw(self, window):
        self.y += self.vel
        window.blit(alien_bullet_img, (self.x, self.y))
        self.rect = (self.x, self.y, self.width, self.height)
        self.alien_bullet_hitbox = pygame.Rect(self.rect)

for row in range(alien_rows):
    for col in range(alien_cols):
        aliens.append((Aliens(100 + col * 85, 100 + row * 75)))

def GameOver():
    text = font1.render('Game Over', 1, 'red')
    screen.blit(text, (110, 500))
    pygame.display.flip()

def Won():
    text = font1.render('You win!', 1, 'green')
    screen.blit(text, (150, 350))
    pygame.display.flip()

def Draw():
    screen.blit(bg, (0, 0))
    player.draw(screen)
    score_text = font.render('Score: ' + str(score), 1, 'white')
    screen.blit(score_text, (10, 5))
    if player.health == 3:
        screen.blit(heart_img, (540, 10))
        screen.blit(heart_img, (490, 10))
        screen.blit(heart_img, (440, 10))
    if player.health == 2:
        screen.blit(heart_img, (540, 10))
        screen.blit(heart_img, (490, 10))
    if player.health == 1:
        screen.blit(heart_img, (540, 10))
    
    for alien in aliens:
        alien.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for alien_bullet in alien_bullets:
        alien_bullet.draw(screen)
    pygame.display.flip()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    current_time = pygame.time.get_ticks()
    if current_time - alien_last_shot > alien_bullet_cooldown and len(alien_bullets) < 5 and len(aliens) > 0:
        shooting_alien = random.choice(aliens)
        alien_bullet = AlienBullet(shooting_alien.x + 25, shooting_alien.y + 50)
        alien_bullets.append(alien_bullet)
        alien_last_shot = current_time
    
    for alien_bullet in alien_bullets:
        if alien_bullet.y > S_HEIGHT:
            alien_bullets.remove(alien_bullet)
    
    for alien_bullet in alien_bullets:
        if player.hitbox.colliderect(alien_bullet.alien_bullet_hitbox) and player.health > 0:
            pygame.mixer.Sound.play(player_hit_sound)
            player.health -= 1
            alien_bullets.remove(alien_bullet)
    
    for alien in aliens:
        for bullet in bullets:
            if alien.alien_hitbox.colliderect(bullet.bullet_hitbox):
                pygame.mixer.Sound.play(explosion_sound)
                score += 1
                bullets.remove(bullet)
                aliens.remove(alien)
    
    if player.health == 0:
        GameOver()
        pygame.mixer.Sound.play(gameover_sound)
        time.sleep(5)
        run = False

    if bullet_counter > 0:
        bullet_counter += 1
    if bullet_counter > 10:
        bullet_counter = 0
    for bullet in bullets:
        if bullet.y > 0:
            bullet.y -= bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
        
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player.vel
    elif keys[pygame.K_RIGHT] and player.x < S_WIDTH - player.width:
        player.x += player.vel
    
    if keys[pygame.K_SPACE] and bullet_counter == 0:
        if len(bullets) < 3 :
            bullets.append(PlayerBullet(player.x, player.y))
            pygame.mixer.Sound.play(bullet_sound)

        bullet_counter = 1
    
    if score == 25:
        Won()
        time.sleep(5)
        run = False
    
    clock.tick(FPS)
    Draw()
