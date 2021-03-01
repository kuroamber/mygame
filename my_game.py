# -*- coding: utf-8 -*-
# Что тут есть: умеренно анимированные спрайты, фоны, музыка
# Какой-никакой левел-ап
# Возможность перезапуска игры
#
#
# Регина Ростовцева
import pygame
import random
import sys

WIDTH = 900
HEIGHT = 600
FPS = 30
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VARIANTS = 'rrrrrrrggp'
VARIANTSG = 'rrrrrrrpp'
VARIANTSP = 'rrrrrrrggg'
VARIANTSGP = 'r' #это не звуки, которые издает зомби, это варианты цвета мозгов

#тут создаются мозги
class Brains(pygame.sprite.Sprite):
    def __init__(self, min_speed, max_speed, variant):
        self.max_speed = max_speed
        self.min_speed = min_speed
        self.type = random.choice(variant)
        pygame.sprite.Sprite.__init__(self)
        if self.type == 'r':
            self.image = brain_red
        elif self.type == 'g':
            self.image = brain_green
        elif self.type == 'p':
            self.image = brain_purple
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        #спаунятся где-то в верхней половине экрана
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(0, 300)
        #скорость у мозгов постоянная
        self.speed_y = random.randrange(min_speed, self.max_speed)
        self.speed_x = random.randrange(-3, 3)

    def update(self):
        #двигаем мозги
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        #тут дописать, чтобы отталкивались от стен
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speed_x = -self.speed_x
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed_y = -self.speed_y

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == 5:
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion
                self.rect = self.image.get_rect()
                self.rect.center = center

#тут создается зомби-игрок
class Zombie(pygame.sprite.Sprite):
    #создаем зомби и размещаем его где-то в нижней части поля, потому что мозги появляются наверху
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img1
        self.vid = 0 #эта переменная нужна для смены анимации зомби
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 750)
        self.rect.y = 500
        self.lifes = 3
        self.mask = pygame.mask.from_surface(self.image)

    # тут обновляем зомби с учетом движения и довольно всрато меняем его анимацию
    def update(self):
        #меняем анимацию
        if self.vid <= 5:
            self.image = player_img2
            self.image.set_colorkey(WHITE)
            self.vid += 1
        elif self.vid < 10:
            self.image = player_img1
            self.vid += 1
        else:
            self.vid = 0
        #двигаем зомби стрелками
        self.speed_x = 0
        self.speed_y = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        if keystate[pygame.K_UP]:
            self.speed_y = -5
        if keystate[pygame.K_DOWN]:
            self.speed_y = 5
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        #за пределы экрана зомби не выходит
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# отрисовываем тексты
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE, BLUE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_start_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Ходи по полю и управляй зомби с помощью стрелок", 22, WIDTH // 2, 10)
    draw_text(screen, "Зеленые мозги отнимают жизнь. Фиолетовые взрываются", 22, WIDTH // 2, 50)
    draw_text(screen, "Нажми любую клавишу, чтобы начать", 22, WIDTH // 2, 90)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def draw_gameover(text):
    screen.blit(background, background_rect)
    f2.write(str(SCORE) + '\n')
    f2.close()
    draw_text(screen, 'Игра окончена', 22, WIDTH // 2, 20)
    draw_text(screen, text, 22, WIDTH // 2, 60)
    draw_text(screen, 'Твои очки:' + str(SCORE), 22, WIDTH // 2, 100)
    draw_text(screen, 'Лучшие результаты: ', 22, WIDTH // 2, 140)
    place = 140
    res = view_champions()
    for elem in res:
        draw_text(screen, str(elem), 22, WIDTH // 2, place + 40)
        place += 40
    draw_text(screen, 'Нажми пробел, чтобы сыграть снова ', 22, WIDTH // 2, 400)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    screen.blit(background, background_rect)
                    waiting = False

def add_brain(m):
    if m.type == 'r':
        red_brains.add(m)
    elif m.type == 'g':
        green_brains.add(m)
    else:
        purple_brains.add(m)
    brains.add(m)

def view_champions():
    f = open("files/champions.txt")
    lines = f.readlines()
    all_champ = [int(elem) for elem in lines]
    all_champ.sort(reverse=True)
    res = all_champ[0:5]
    f.close()
    return res


f2 = open("files/champions.txt", 'a')
pause = 3000  # пауза между появлением мозгов
pygame.init()
pygame.mixer.init()
explo = pygame.mixer.Sound('files/explosion.wav')
up = pygame.mixer.Sound('files/up.wav')
green_hit = pygame.mixer.Sound('files/hit.wav')
getbrain = pygame.mixer.Sound('files/getbrain.wav')
pygame.mixer.music.load('files/theme.ogg')
pygame.mixer.music.set_volume(0.2)
pygame.time.set_timer(pygame.USEREVENT, pause) #пауза
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Зомби в зимнем лесу собирает мозги! Избегай зеленых! Фиолетовые взрываются!")
font_name = pygame.font.match_font('Verdana')
player_img1 = pygame.image.load('files/zombie_action1.png').convert_alpha()
player_img2 = pygame.image.load('files/zombie_action2.png').convert_alpha()
background = pygame.image.load('files/background.png').convert() #https://opengameart.org/content/backgrounds-3
brain_red = pygame.image.load('files/redbrain.png').convert_alpha()
brain_green = pygame.image.load('files/greenbrain.png').convert_alpha()
brain_purple = pygame.image.load('files/purplebrain.png').convert_alpha()
explosion = pygame.image.load('files/expl_image.png').convert_alpha()
background_rect = background.get_rect()
screen.blit(background, background_rect)
pygame.display.update()
clock = pygame.time.Clock()
game_over = False
start_screen = True
running = True
pygame.mixer.music.play(loops=-1)
while running:
    if start_screen:
        SCORE = 0  # счет
        LIFES = 3  # если успею, перенести в класс игрока
        max_brains = 10  # максимум мозгов на поле
        kol_brains = 0  # количество мозгов на поле
        min_speed = 1 #минимально возможная скорость на старте
        max_speed = 5  # максимально возможная скорость на старте
        total_hits = 0 #количество столкновений
        add_score = 1 #сколько добавляется за каждое столкновение
        all_sprites = pygame.sprite.Group()
        brains = pygame.sprite.Group()
        red_brains = pygame.sprite.Group()
        green_brains = pygame.sprite.Group()
        purple_brains = pygame.sprite.Group()
        player = Zombie()
        all_sprites.add(player)
        draw_start_screen()
        start_screen = False
    if game_over:
        game_over = False
        start_screen = True
        draw_gameover(text)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.USEREVENT:
            if len(green_brains) < 2 and len(purple_brains) < 2:
                m = Brains(min_speed, max_speed, VARIANTS)
                add_brain(m)
            elif len(green_brains) < 2:
                m = Brains(min_speed, max_speed, VARIANTSP)
                add_brain(m)
            elif len(purple_brains) < 2:
                m = Brains(min_speed, max_speed, VARIANTSG)
                add_brain(m)
            else:
                m = Brains(min_speed, max_speed, VARIANTSGP)
                add_brain(m)
            all_sprites.add(m)
    all_sprites.update()
    if len(red_brains) > 10:
        text = 'Слишком много несъеденных мозгов'
        player.kill()
        game_over = True
    hits = pygame.sprite.spritecollide(player, brains, True)
    for hit in hits:
        if hit.type == 'r':
            getbrain.play()
            total_hits += 1
            SCORE = SCORE + add_score
            if total_hits % 10 == 0: # за каждые 10 собранных - левел-ап
                up.play()
                min_speed += 1 # мозги стали быстрее
                max_speed += 1 #
                pause -= 20 # появляются чаще
                add_score += 1 # дают больше очков
        elif hit.type == 'g':
            green_hit.play()
            x_heart = 750
            y_heart = 20
            if LIFES > 0:
                LIFES -= 1
            else:
                text = 'Кончились жизни'
                player.kill()
                game_over = True
        else:
            explo.play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if LIFES > 0:
                LIFES -= 1
                SCORE = SCORE + len(brains) * add_score
            else:
                text = 'Кончились жизни'
                player.kill()
                game_over = True
            brains = pygame.sprite.Group()
            red_brains = pygame.sprite.Group()
            green_brains = pygame.sprite.Group()
            purple_brains = pygame.sprite.Group()
            for elem in all_sprites:
                if isinstance(elem, Brains):
                    all_sprites.remove(elem)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(SCORE), 18, WIDTH//2, 20)
    draw_text(screen, 'Жизней в запасе: ' + str(LIFES), 18, 750, 20)
    pygame.display.flip()
pygame.quit()