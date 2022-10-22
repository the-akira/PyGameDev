import pygame, csv, sys

SCREEN_SIZE = pygame.Rect((0, 0, 800, 640))
INITIAL_POS = (50, 50)
ROWS, COLS = 50, 150
TILE_SIZE = 32
FPS = 60

screen = pygame.display.set_mode(SCREEN_SIZE.size)

wall = pygame.image.load('sprites/wall.png').convert_alpha()
wall_scaled = pygame.transform.scale(wall, (TILE_SIZE,TILE_SIZE)).convert_alpha()
floor = pygame.image.load('sprites/floor.png').convert_alpha()
floor_scaled = pygame.transform.scale(floor, (TILE_SIZE,TILE_SIZE)).convert_alpha()

floors = pygame.sprite.Group()
platforms = pygame.sprite.Group()
orc_group = pygame.sprite.Group()
beholder_group = pygame.sprite.Group()
skeleton_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()
necromancer_group = pygame.sprite.Group()

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
        for sprite in self.sprites():
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

def cast_fireball(centerx, centery, key, time):
    fireball = Fireball(centerx, centery, key)
    fireball_group.add(fireball)
    return time

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, key):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/fireball.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_shot = pygame.time.get_ticks()
        self.key = key
        self.flip = False
        self.speed = 8.5

    def update(self, enemies, platforms):
        if self.key == 'i':
            self.rect.y -= self.speed
        if self.key == 'k':
            self.rect.y += self.speed
        if self.key == 'j':
            self.rect.x -= self.speed
            self.flip = True
        if self.key == 'l':
            self.rect.x += self.speed
            self.flip = False

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
        surface.blit(pygame.transform.flip(self.image, self.flip, False), 
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
        self.speed = 3.85
        self.last_shot = pygame.time.get_ticks()

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
            self.last_shot = cast_fireball(self.rect.centerx, self.rect.centery, 'k', time_now)
        if pressed[pygame.K_i] and time_now - self.last_shot > cooldown:
            self.last_shot = cast_fireball(self.rect.centerx, self.rect.centery, 'i', time_now)
        if pressed[pygame.K_j] and time_now - self.last_shot > cooldown:
            self.last_shot = cast_fireball(self.rect.centerx, self.rect.centery, 'j', time_now)
        if pressed[pygame.K_l] and time_now - self.last_shot > cooldown:
            self.last_shot = cast_fireball(self.rect.centerx, self.rect.centery, 'l', time_now)

        self.rect.left += self.vel.x
        self.collide(self.vel.x, 0, self.platforms)
        self.rect.top += self.vel.y
        self.collide(0, self.vel.y, self.platforms)

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
        self.rect.x += 1
        self.collide(1, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if xvel > 0:
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
        self.rect.y -= 1
        self.collide(0, -1, platforms)

    def collide(self, xvel, yvel, platforms):
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if yvel < 0:
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
        self.rect.x -= 1
        self.collide(-1, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if xvel < 0:
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

    with open('map/map.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x,row in enumerate(reader):
            for y,tile in enumerate(row):
                world_data[x][y] = tile

    player = Player(platforms, INITIAL_POS)
    level_width  = len(world_data[0]) * TILE_SIZE
    level_height = len(world_data) * TILE_SIZE
    entities = CameraLayeredUpdates(player, pygame.Rect(0, 0, level_width, level_height))

    skeletons = [
        Skeleton(platforms, (200,200)),
        Skeleton(platforms, (200,350)),
        Skeleton(platforms, (200,850)),
        Skeleton(platforms, (1250,330))
    ]
    for skeleton in skeletons:
        skeleton_group.add(skeleton)

    necromancers = [
        Necromancer(platforms, (2500,300)),
        Necromancer(platforms, (600,550)),
        Necromancer(platforms, (450,1210))
    ]
    for necromancer in necromancers:
        necromancer_group.add(necromancer)

    orcs = [
        Orc(platforms, (200,1480)),
        Orc(platforms, (3200,250)),
        Orc(platforms, (1000,600)),
    ]
    for orc in orcs:
        orc_group.add(orc)

    beholders = [
        Beholder(platforms, (2800,40)),
        Beholder(platforms, (2800,1400)),
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not main_menu:
                screen.fill(pygame.Color("Black"))
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
            entities.update()
            entities.draw(screen)
            for skeleton in skeletons:
                skeleton.draw(screen, entities.cam.x, entities.cam.y)
            skeleton_group.update(platforms)
            for necromancer in necromancers:
                necromancer.draw(screen, entities.cam.x, entities.cam.y)
            necromancer_group.update(platforms)
            for orc in orcs:
                orc.draw(screen, entities.cam.x, entities.cam.y)
            orc_group.update(platforms)
            for beholder in beholders:
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