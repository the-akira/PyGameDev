from character import Character
from weapon import Weapon
from button import Button
from world import World
from constants import *
from items import Item
import pygame
import csv

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")
clock = pygame.time.Clock()
level = 1
start_game = False
pause_game = False
start_intro = True
screen_scroll = [0, 0]

moving_left = False
moving_right = False
moving_up = False
moving_down = False

font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)

music = pygame.mixer.Sound('assets/audio/music.wav')
music.set_volume(0.25)
music.play(-1, 0, 5000)

shot_fx = pygame.mixer.Sound('assets/audio/arrow_shot.mp3')
shot_fx.set_volume(0.4)

hit_fx = pygame.mixer.Sound('assets/audio/arrow_hit.wav')
hit_fx.set_volume(0.4)

coin_fx = pygame.mixer.Sound('assets/audio/coin.wav')
coin_fx.set_volume(0.4)

heal_fx = pygame.mixer.Sound('assets/audio/heal.wav')
heal_fx.set_volume(0.4)

def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w* scale, h * scale))

restart_img = pygame.image.load("assets/images/buttons/button_restart.png").convert_alpha()
restart_img = scale_img(restart_img, BUTTON_SCALE)

start_img = pygame.image.load("assets/images/buttons/button_start.png").convert_alpha()
start_img = scale_img(start_img, BUTTON_SCALE)

exit_img = pygame.image.load("assets/images/buttons/button_exit.png").convert_alpha()
exit_img = scale_img(exit_img, BUTTON_SCALE)

resume_img = pygame.image.load("assets/images/buttons/button_resume.png").convert_alpha()
resume_img = scale_img(resume_img, BUTTON_SCALE)

heart_empty = pygame.image.load("assets/images/items/heart_empty.png").convert_alpha()
heart_empty = scale_img(heart_empty, ITEM_SCALE)

heart_half = pygame.image.load("assets/images/items/heart_half.png").convert_alpha()
heart_half = scale_img(heart_half, ITEM_SCALE)

heart_full = pygame.image.load("assets/images/items/heart_full.png").convert_alpha()
heart_full = scale_img(heart_full, ITEM_SCALE)

coin_images = []
for x in range(4):
    img = scale_img(
        pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(),
        ITEM_SCALE
    )
    coin_images.append(img)

red_potion = scale_img(
    pygame.image.load(f"assets/images/items/potion_red.png").convert_alpha(), 
    POTION_SCALE
)
item_images = []
item_images.append(coin_images)
item_images.append(red_potion)

bow = pygame.image.load("assets/images/weapons/bow.png").convert_alpha()
bow_image = scale_img(bow, WEAPON_SCALE)

arrow = pygame.image.load("assets/images/weapons/arrow.png").convert_alpha()
arrow_image = scale_img(arrow, WEAPON_SCALE)

fireball = pygame.image.load("assets/images/weapons/fireball.png").convert_alpha()
fireball_image = scale_img(fireball, FIREBALL_SCALE)

tile_list = []
for x in range(TILE_TYPES):
    tile_image = pygame.image.load(f"assets/images/tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
    tile_list.append(tile_image)

mob_animations = []
mob_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon"]
animation_types = ["idle", "run"]
for mob in mob_types:
    animation_list = []
    for animation in animation_types:
        temp_list = []
        for i in range(4):
            img = pygame.image.load(
                f"assets/images/characters/{mob}/{animation}/{i}.png"
            ).convert_alpha()
            img = scale_img(img, SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def draw_info():
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 50))
    pygame.draw.line(screen, WHITE, (0, 50), (SCREEN_WIDTH, 50))
    half_heart_drawn = False
    for i in range(5):
        if player.health >= ((i + 1) * 20):
            screen.blit(heart_full, (10 + i * 50, 0))
        elif (player.health % 20 > 0) and not half_heart_drawn:
            screen.blit(heart_half, (10 + i * 50, 0))
            half_heart_drawn = True
        else:
            screen.blit(heart_empty, (10 + i * 50, 0))
    draw_text("LEVEL: " + str(level), font, WHITE, SCREEN_WIDTH / 2, 15)
    draw_text(f"X{player.score}", font, WHITE, SCREEN_WIDTH - 100, 15)

def reset_level():
    damage_text_group.empty()
    arrow_group.empty()
    item_group.empty()
    fireball_group.empty()

    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(str(damage), True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

class ScreenFade:
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color 
        self.speed = speed 
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(
                screen, self.color, 
                (0 - self.fade_counter, 0, SCREEN_WIDTH//2, SCREEN_HEIGHT)
            )
            pygame.draw.rect(
                screen, self.color, 
                (SCREEN_WIDTH//2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            )
            pygame.draw.rect(
                screen, self.color, 
                (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT//2)
            )
            pygame.draw.rect(
                screen, self.color, 
                (0, SCREEN_HEIGHT//2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT)
            )
        elif self.direction == 2:
            pygame.draw.rect(screen, self.color, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True
        return fade_complete

world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

with open(f"levels/level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
world.process_data(world_data, tile_list, item_images, mob_animations)

player = world.player
bow = Weapon(bow_image, arrow_image)

enemy_list = world.character_list

damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()

score_coin = Item(SCREEN_WIDTH - 115, 23, 0, coin_images, True)
item_group.add(score_coin)

for item in world.item_list:
    item_group.add(item)

intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)

restart_button = Button(
    SCREEN_WIDTH//2 - 185, 
    SCREEN_HEIGHT//2 - 50, 
    restart_img
)
start_button = Button(
    SCREEN_WIDTH//2 - 155, 
    SCREEN_HEIGHT//2 - 150, 
    start_img
)
exit_button = Button(
    SCREEN_WIDTH//2 - 120, 
    SCREEN_HEIGHT//2 + 50, 
    exit_img
)
resume_button = Button(
    SCREEN_WIDTH//2 - 185, 
    SCREEN_HEIGHT//2 - 150, 
    resume_img
)

running = True
while running:
    clock.tick(FPS)

    if not start_game:
        screen.fill(MENU_BG)
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            running = False
    else:
        if pause_game:
            screen.fill(MENU_BG)
            resume_button.draw(screen)
            if resume_button.draw(screen):
                pause_game = False
            if exit_button.draw(screen):
                running = False
        else:
            screen.fill(BACKGROUND)

            if player.alive:

                dx, dy = 0, 0
                if moving_left:
                    dx = -SPEED
                if moving_right:
                    dx = SPEED
                if moving_up:
                    dy = -SPEED
                if moving_down:
                    dy = SPEED

                screen_scroll, level_complete = player.move(
                    dx, 
                    dy, 
                    world.obstacle_tiles, 
                    world.exit_tile
                )

                world.update(screen_scroll)
                for enemy in enemy_list:
                    fireball = enemy.ai(
                        player, 
                        world.obstacle_tiles, 
                        screen_scroll, 
                        fireball_image
                    )
                    if fireball:
                        fireball_group.add(fireball)
                    if enemy.alive:
                        enemy.update()
                player.update()
                arrow = bow.update(player)
                if arrow:
                    shot_fx.play()
                    arrow_group.add(arrow)
                for arrow in arrow_group:
                    damage, damage_pos = arrow.update(
                        screen_scroll, 
                        world.obstacle_tiles, 
                        enemy_list
                    )
                    if damage:
                        damage_text = DamageText(
                            damage_pos.centerx, 
                            damage_pos.y, 
                            damage, 
                            RED
                        )
                        damage_text_group.add(damage_text)
                        hit_fx.play()
                damage_text_group.update()
                fireball_group.update(screen_scroll, player)
                item_group.update(screen_scroll, player, coin_fx, heal_fx)

            world.draw(screen)
            for enemy in enemy_list:
                enemy.draw(screen)
            player.draw(screen)
            bow.draw(screen)
            for arrow in arrow_group:
                arrow.draw(screen)
            for fireball in fireball_group:
                fireball.draw(screen)
            damage_text_group.draw(screen)
            item_group.draw(screen)
            draw_info()
            score_coin.draw(screen)

            if level_complete:
                start_intro = True
                level += 1
                world_data = reset_level()

                with open(f"levels/level{level}_data.csv", newline="") as csvfile:
                    reader = csv.reader(csvfile, delimiter=",")
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)

                world = World()
                world.process_data(world_data, tile_list, item_images, mob_animations)
                temp_hp = player.health
                temp_score = player.score
                player = world.player
                player.health = temp_hp
                player.score = temp_score
                enemy_list = world.character_list
                score_coin = Item(SCREEN_WIDTH - 115, 23, 0, coin_images, True)
                item_group.add(score_coin)
                for item in world.item_list:
                    item_group.add(item)

            if start_intro:
                if intro_fade.fade():
                    start_intro = False
                    intro_fade.fade_counter = 0

            if not player.alive:
                if death_fade.fade():
                    if restart_button.draw(screen):
                        death_fade.fade_counter = 0
                        start_intro = True
                        world_data = reset_level()

                        with open(f"levels/level{level}_data.csv", newline="") as csvfile:
                            reader = csv.reader(csvfile, delimiter=",")
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)

                        world = World()
                        world.process_data(world_data, tile_list, item_images, mob_animations)
                        temp_score = player.score
                        player = world.player
                        player.score = temp_score
                        enemy_list = world.character_list
                        score_coin = Item(SCREEN_WIDTH - 115, 23, 0, coin_images, True)
                        item_group.add(score_coin)
                        for item in world.item_list:
                            item_group.add(item)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
            if event.key == pygame.K_ESCAPE:
                pause_game = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False

    pygame.display.update()

pygame.quit()