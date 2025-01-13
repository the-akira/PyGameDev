import pygame, csv, sys

SCREEN_SIZE = pygame.Rect((0, 0, 800, 640))
INITIAL_POS = (45, 45)
ROWS, COLS = 40, 60
TILE_SIZE = 32
FPS = 60

screen = pygame.display.set_mode(SCREEN_SIZE.size)

wall = pygame.image.load('sprites/wall.png').convert_alpha()
wall_scaled = pygame.transform.scale(wall, (TILE_SIZE,TILE_SIZE)).convert_alpha()
floor = pygame.image.load('sprites/floor.png').convert_alpha()
floor_scaled = pygame.transform.scale(floor, (TILE_SIZE,TILE_SIZE)).convert_alpha()
dungeon = pygame.image.load('images/dungeon.png').convert_alpha()
dungeon_scaled = pygame.transform.scale(dungeon,
    (SCREEN_SIZE.width,SCREEN_SIZE.height)).convert_alpha()

floors = pygame.sprite.Group()
platforms = pygame.sprite.Group()
orc_group = pygame.sprite.Group()
beholder_group = pygame.sprite.Group()
skeleton_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()
necromancer_group = pygame.sprite.Group()

pygame.mixer.init()
music = pygame.mixer.Sound('sounds/musics/Dragon_Level_David_Fesliyan.wav')
music.set_volume(0.1)
firecast = pygame.mixer.Sound('sounds/effects/firecast.wav')
firecast.set_volume(0.7)

class CameraLayeredUpdates(pygame.sprite.LayeredUpdates):
    def __init__(self, target, world_size):
        super().__init__()
        self.target = target
        self.cam = pygame.Vector2(0, 0)
        self.world_size = world_size
        if self.target:
            self.add(target, layer=1)

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.centerx + SCREEN_SIZE.width/2
            y = -self.target.rect.centery + SCREEN_SIZE.height/2
            self.cam += (pygame.Vector2((x, y)) - self.cam) * 0.05
            self.cam.x = max(-(self.world_size.width-SCREEN_SIZE.width), min(0, self.cam.x))
            self.cam.y = max(-(self.world_size.height-SCREEN_SIZE.height), min(0, self.cam.y))

    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        init_rect = self._init_rect
        visible_sprites = [
            sprite for sprite in self.sprites()
            if sprite.rect.colliderect(pygame.Rect(
                -self.cam.x, -self.cam.y, SCREEN_SIZE.width, SCREEN_SIZE.height))
        ]
        for sprite in visible_sprites:
            rec = spritedict[sprite]
            newrect = surface_blit(sprite.image, sprite.rect.move(self.cam))
            if rec is init_rect:
                dirty_append(newrect)
            else:
                if newrect.colliderect(rec):
                    dirty_append(newrect.union(rec))
                else:
                    dirty_append(newrect)
                    dirty_append(rec)
            spritedict[sprite] = newrect
        return dirty

def cast_fireball(x, y, key, time):
    firecast.play()
    fireball = Fireball(x, y, key)
    fireball_group.add(fireball)
    return time

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, key):
        pygame.sprite.Sprite.__init__(self)
        self.image_right = pygame.image.load('sprites/fireballright.png').convert_alpha()
        self.image_top = pygame.image.load('sprites/fireballtop.png').convert_alpha()
        self.last_shot = pygame.time.get_ticks()
        self.key = key
        if self.key == 'i' or self.key == 'k':
            self.rect = self.image_top.get_rect()
        elif self.key == 'j' or self.key == 'l':
            self.rect = self.image_right.get_rect()
        self.rect.center = [x, y]
        self.flip = False
        self.horizontal = False
        self.speed = 8.5

    def update(self, enemies, platforms):
        if self.key == 'i':
            self.rect.y -= self.speed
        if self.key == 'k':
            self.rect.y += self.speed
        if self.key == 'j':
            self.rect.x -= self.speed
            self.flip = True
            self.horizontal = True
        if self.key == 'l':
            self.rect.x += self.speed
            self.flip = False
            self.horizontal = True

        for skeleton in enemies["skeletons"]:
            if skeleton.rect.colliderect(self.rect):
                self.kill()
                skeleton.health -= 10
                if skeleton.health <= 0:
                    enemies["skeletons"].remove(skeleton)

        for beholder in enemies["beholders"]:
            if beholder.rect.colliderect(self.rect):
                self.kill()
                beholder.health -= 10
                if beholder.health <= 0:
                    enemies["beholders"].remove(beholder)

        for necromancer in enemies["necromancers"]:
            if necromancer.rect.colliderect(self.rect):
                self.kill()
                necromancer.health -= 10
                if necromancer.health <= 0:
                    enemies["necromancers"].remove(necromancer)

        for orc in enemies["orcs"]:
            if orc.rect.colliderect(self.rect):
                self.kill()
                orc.health -= 10
                if orc.health <= 0:
                    enemies["orcs"].remove(orc)

        for platform in platforms:
            if platform.rect.colliderect(self.rect):
                self.kill()

        fireball_lifetime = 600
        if (pygame.time.get_ticks() - self.last_shot) >= fireball_lifetime:
            self.kill()

    def draw(self, surface, scroll_x, scroll_y):
        if self.horizontal:
            surface.blit(pygame.transform.flip(self.image_right, self.flip, False),
                (self.rect.x + scroll_x, self.rect.y + scroll_y))
        elif self.key == 'i':
            surface.blit(self.image_top, (self.rect.x + scroll_x, self.rect.y + scroll_y))
        elif self.key == 'k':
            surface.blit(pygame.transform.rotate(self.image_top, 180),
                (self.rect.x + scroll_x, self.rect.y + scroll_y))

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)

class Player(Entity):
    def __init__(self, platforms, pos, *groups):
        super().__init__(pos)
        img = pygame.image.load('sprites/wizard.png').convert_alpha()
        self.image = pygame.transform.scale(img, (55,65)).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.vel = pygame.Vector2((0, 0))
        self.platforms = platforms
        self.last_shot = pygame.time.get_ticks()
        self.speed = 4.33

    def update(self):
        pressed = pygame.key.get_pressed()
        left = pressed[pygame.K_LEFT] or pressed[pygame.K_a]
        right = pressed[pygame.K_RIGHT] or pressed[pygame.K_d]
        up = pressed[pygame.K_UP] or pressed[pygame.K_w]
        down = pressed[pygame.K_DOWN] or pressed[pygame.K_s]
        cooldown = 500

        if left:
            self.vel.x = -self.speed
        if right:
            self.vel.x = self.speed
        if up:
            self.vel.y = -self.speed
        if down:
            self.vel.y = self.speed
        if not(left or right):
            self.vel.x = 0
        if not(up or down):
            self.vel.y = 0

        time_now = pygame.time.get_ticks()
        if pressed[pygame.K_k] and time_now - self.last_shot > cooldown:
            self.last_shot = cast_fireball(self.rect.centerx, self.rect.bottom, 'k', time_now)
        if pressed[pygame.K_i] and time_now - self.last_shot > cooldown:
            self.last_shot = cast_fireball(self.rect.centerx, self.rect.top, 'i', time_now)
        if pressed[pygame.K_j] and time_now - self.last_shot > cooldown:
            self.last_shot = cast_fireball(self.rect.centerx, self.rect.centery, 'j', time_now)
        if pressed[pygame.K_l] and time_now - self.last_shot > cooldown:
            self.last_shot = cast_fireball(self.rect.centerx, self.rect.centery, 'l', time_now)

        nearby_platforms = get_nearby_platforms(platforms, self.rect.center, radius=100)

        self.rect.left += self.vel.x
        self.collide(self.vel.x, 0, nearby_platforms)
        self.rect.top += self.vel.y
        self.collide(0, self.vel.y, nearby_platforms)

    def collide(self, xvel, yvel, platforms):
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if xvel > 0:
                    self.rect.right = platform.rect.left
                if xvel < 0:
                    self.rect.left = platform.rect.right
                if yvel > 0:
                    self.rect.bottom = platform.rect.top
                if yvel < 0:
                    self.rect.top = platform.rect.bottom

class Skeleton(Entity):
    def __init__(self, platforms, pos, *groups):
        super().__init__(pos)
        img = pygame.image.load('sprites/skeleton.png').convert_alpha()
        self.image = pygame.transform.scale(img, (55,65)).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.health = 30

    def draw(self, surface, scroll_x, scroll_y):
        surface.blit(self.image, (self.rect.x + scroll_x, self.rect.y + scroll_y))

    def update(self, platforms):
        nearby_platforms = get_nearby_platforms(platforms, self.rect.center, radius=100)
        self.rect.x += 1
        self.collide(nearby_platforms)

    def collide(self, platforms):
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collisions:
            if self.rect.x < platform.rect.x:
                self.rect.right = platform.rect.left

class Necromancer(Entity):
    def __init__(self, platforms, pos, *groups):
        super().__init__(pos)
        img = pygame.image.load('sprites/necromancer.png').convert_alpha()
        self.image = pygame.transform.scale(img, (55,75)).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.health = 60

    def draw(self, surface, scroll_x, scroll_y):
        surface.blit(self.image, (self.rect.x + scroll_x, self.rect.y + scroll_y))

    def update(self, platforms):
        nearby_platforms = get_nearby_platforms(platforms, self.rect.center, radius=100)
        self.rect.y -= 1
        self.collide(nearby_platforms)

    def collide(self, platforms):
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collisions:
            if self.rect.x < platform.rect.x:
                self.rect.top = platform.rect.bottom

class Beholder(Entity):
    def __init__(self, platforms, pos, *groups):
        super().__init__(pos)
        img = pygame.image.load('sprites/beholder.png').convert_alpha()
        self.image = pygame.transform.scale(img, (70,75)).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.health = 80

    def draw(self, surface, scroll_x, scroll_y):
        surface.blit(self.image, (self.rect.x + scroll_x, self.rect.y + scroll_y))

class Orc(Entity):
    def __init__(self, platforms, pos, *groups):
        super().__init__(pos)
        img = pygame.image.load('sprites/orc.png').convert_alpha()
        self.image = pygame.transform.scale(img, (85,75)).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.health = 40

    def draw(self, surface, scroll_x, scroll_y):
        surface.blit(self.image, (self.rect.x + scroll_x, self.rect.y + scroll_y))

    def update(self, platforms):
        nearby_platforms = get_nearby_platforms(platforms, self.rect.center, radius=100)
        self.rect.x -= 1
        self.collide(nearby_platforms)

    def collide(self, platforms):
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collisions:
            if self.rect.x > platform.rect.x:
                self.rect.left = platform.rect.right

class Wall(Entity):
    def __init__(self, pos, *groups):
        super().__init__(pos, *groups)
        self.image = wall_scaled

class Floor(Entity):
    def __init__(self, pos, *groups):
        super().__init__(pos, *groups)   
        self.image = floor_scaled

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.clicked = False

    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)
        return action

def get_visible_entities(entities, camera, screen_size):
    visible_rect = pygame.Rect(-camera.x, -camera.y, screen_size.width, screen_size.height)
    return [entity for entity in entities if entity.rect.colliderect(visible_rect)]

def get_nearby_platforms(platforms, position, radius):
    nearby_rect = pygame.Rect(
        position[0] - radius,
        position[1] - radius,
        radius * 2,
        radius * 2
    )
    return [platform for platform in platforms if platform.rect.colliderect(nearby_rect)]

def main():
    pygame.init()
    pygame.display.set_caption("RPG Simulation")
    clock = pygame.time.Clock()
    main_menu = True
    paused = False

    restart_img = pygame.image.load('buttons/restart_btn.png').convert_alpha()
    restart_button = Button(SCREEN_SIZE.width // 2 - 60, SCREEN_SIZE.height // 2 - 50, restart_img)
    start_img = pygame.image.load('buttons/start_btn.png').convert_alpha()
    start_button = Button(SCREEN_SIZE.width // 2 - 60, SCREEN_SIZE.height // 2 - 60, start_img)
    exit_img = pygame.image.load('buttons/exit_btn.png').convert_alpha()
    exit_button = Button(SCREEN_SIZE.width // 2 - 60, SCREEN_SIZE.height // 2 - 10, exit_img)

    world_data = []
    for row in range(ROWS):
        r = [-1] * COLS
        world_data.append(r)

    with open('map/mapa.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x,row in enumerate(reader):
            for y,tile in enumerate(row):
                world_data[x][y] = tile

    player = Player(platforms, INITIAL_POS)
    level_width  = len(world_data[0]) * TILE_SIZE
    level_height = len(world_data) * TILE_SIZE
    entities = CameraLayeredUpdates(player, pygame.Rect(0, 0, level_width, level_height))

    skeletons = [
        Skeleton(platforms, (280,200)),
        Skeleton(platforms, (250,350)),
        Skeleton(platforms, (200,850)),
        Skeleton(platforms, (300,600))
    ]
    for skeleton in skeletons:
        skeleton_group.add(skeleton)

    necromancers = [
        Necromancer(platforms, (250,480)),
        Necromancer(platforms, (500,300))
    ]
    for necromancer in necromancers:
        necromancer_group.add(necromancer)

    orcs = [
        Orc(platforms, (650,200)),
    ]
    for orc in orcs:
        orc_group.add(orc)

    beholders = [
        Beholder(platforms, (560,600)),
    ]
    for beholder in beholders:
        beholder_group.add(beholder)

    enemies = {
        "orcs": orcs,
        "skeletons": skeletons,
        "beholders": beholders,
        "necromancers": necromancers
    }

    x = y = 0
    for row in world_data:
        for col in row:
            if col == "0":
                Wall((x, y), platforms, entities)
            if col == "-1":
                Floor((x, y), floors, entities)
            x += TILE_SIZE
        y += TILE_SIZE
        x = 0

    while True:
        if main_menu or paused:
            music.play(loops=-1)
            screen.blit(dungeon_scaled, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not main_menu:
                paused = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                main_menu = False

        if main_menu and not paused:
            if exit_button.draw(screen):
                sys.exit()
            if start_button.draw(screen):
                main_menu = False

        if paused and not main_menu:
            if exit_button.draw(screen):
                sys.exit()
            if restart_button.draw(screen):
                paused = False

        if not paused and not main_menu:
            music.stop()
            entities.update()
            entities.draw(screen)

            visible_skeletons = get_visible_entities(skeletons, entities.cam, SCREEN_SIZE)
            visible_necromancers = get_visible_entities(necromancers, entities.cam, SCREEN_SIZE)
            visible_orcs = get_visible_entities(orcs, entities.cam, SCREEN_SIZE)
            visible_beholders = get_visible_entities(beholders, entities.cam, SCREEN_SIZE)

            for skeleton in visible_skeletons:
                skeleton.draw(screen, entities.cam.x, entities.cam.y)
            skeleton_group.update(platforms)
            for necromancer in visible_necromancers:
                necromancer.draw(screen, entities.cam.x, entities.cam.y)
            necromancer_group.update(platforms)
            for orc in visible_orcs:
                orc.draw(screen, entities.cam.x, entities.cam.y)
            orc_group.update(platforms)
            for beholder in visible_beholders:
                beholder.draw(screen, entities.cam.x, entities.cam.y)
            fireball_group.update(enemies, platforms)
            for fireball in fireball_group:
                fireball.draw(screen, entities.cam.x, entities.cam.y)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    try:
        main()
    except:
        sys.exit()