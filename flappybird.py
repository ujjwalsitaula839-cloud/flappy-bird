import pygame
from pygame.locals import *
import random
from scores import create_table, save_score, get_high_score

pygame.init()

clock = pygame.time.Clock()
frame_rate = 60
win_width = 820
win_height = 936
screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Flappy Bird')

ground_offset = 0
scroll_velocity = 3
ground_pos_x = 0
pipe_space = 200
pipe_interval = 1500
last_pipe_time = pygame.time.get_ticks() - pipe_interval
player_lives = 3
game_has_ended = False
start_time = pygame.time.get_ticks()
min_pipe_spacing = 300
player_score = 0

create_table()
top_score = get_high_score()

bg_image = pygame.image.load('img/backG.png')
ground_image = pygame.image.load('img/ground.png')
pipe_image = pygame.image.load('img/pipe.png')

font = pygame.font.SysFont('Bauhaus 93', 60)
white_color = (255, 255, 255)

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    bird.rect.center = (100, int(win_height / 2 - 100))
    bird.vel = 0
    return pygame.time.get_ticks() - pipe_interval

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [pygame.image.load(f'img/bird{n}.png') for n in range(1, 4)]
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = 0

    def update(self):
        self.vel += 0.5
        if self.vel > 6:
            self.vel = 6
        self.rect.y += int(self.vel)

        if self.rect.bottom >= win_height - ground_image.get_height():
            self.rect.bottom = win_height - ground_image.get_height()
            self.vel = 0

        if pygame.mouse.get_pressed()[0] == 1:
            self.vel = -8

        self.counter += 1
        if self.counter > 5:
            self.counter = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, orientation):
        super().__init__()
        self.image = pipe_image.copy()
        self.rect = self.image.get_rect()
        self.orientation = orientation
        self.scored = False

        if orientation == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - int(pipe_space / 2))
        else:
            self.rect.topleft = (x, y + int(pipe_space / 2))

    def update(self):
        self.rect.x -= scroll_velocity
        if self.rect.right < bird.rect.left and not self.scored and self.orientation == -1:
            global player_score
            player_score += 1
            self.scored = True
        if self.rect.right < 0:
            self.kill()

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
bird = Bird(100, int(win_height / 2 - 100))
bird_group.add(bird)

running = True
while running:
    clock.tick(frame_rate)
    screen.blit(bg_image, (0, 0))

    if not game_has_ended:
        pipe_group.draw(screen)

        ground_pos_x -= scroll_velocity
        if ground_pos_x <= -ground_image.get_width():
            ground_pos_x = 0
        ground_pos_y = win_height - ground_image.get_height()
        screen.blit(ground_image, (ground_pos_x, ground_pos_y))
        screen.blit(ground_image, (ground_pos_x + ground_image.get_width(), ground_pos_y))

        bird_group.draw(screen)

        time_now = pygame.time.get_ticks()
        if time_now - start_time < 2000:
            draw_text('Get Ready!', font, white_color, int(win_width / 2 - 140), int(win_height / 2 - 200))
        else:
            if time_now - last_pipe_time > pipe_interval:
                height_offset = random.randint(-100, 100)
                bottom_pipe = Pipe(win_width, int(win_height / 2) + height_offset, -1)
                top_pipe = Pipe(win_width, int(win_height / 2) + height_offset, 1)

                allow_pipe = all(abs(p.rect.x - win_width) >= min_pipe_spacing for p in pipe_group)

                if allow_pipe:
                    pipe_group.add(bottom_pipe)
                    pipe_group.add(top_pipe)
                    last_pipe_time = time_now

            bird_group.update()
            pipe_group.update()

            if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
                player_lives -= 1
                if player_lives <= 0:
                    game_has_ended = True
                    if player_score > top_score:
                        save_score(player_score)
                        top_score = player_score
                else:
                    last_pipe_time = reset_game()
                    start_time = pygame.time.get_ticks()

        draw_text(f'Lives: {player_lives}', font, white_color, 10, 10)
        draw_text(f'Score: {player_score}', font, white_color, int(win_width / 2 - 100), 10)
        draw_text(f'High Score: {top_score}', font, white_color, int(win_width / 2 - 100), 60)

    if game_has_ended:
        if player_lives <= 0:
            draw_text('GAME OVER', font, white_color, int(win_width / 2 - 140), int(win_height / 2 - 150))
            draw_text(f'Score: {player_score}', font, white_color, int(win_width / 2 - 140), int(win_height / 2 - 50))
            draw_text(f'High Score: {top_score}', font, white_color, int(win_width / 2 - 140), int(win_height / 2 + 50))
            draw_text('Press X to Exit', font, white_color, int(win_width / 2 - 140), int(win_height / 2 + 150))
        else:
            draw_text('Press X to Exit', font, white_color, int(win_width / 2 - 140), int(win_height / 2 + 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and player_lives > 0:
                game_has_ended = False
                player_score = 0
                last_pipe_time = reset_game()
            if event.key == pygame.K_x:
                running = False

    pygame.display.update()

pygame.quit()
