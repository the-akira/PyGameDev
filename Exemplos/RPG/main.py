import pygame, csv, sys, math

SCREEN_SIZE = pygame.Rect((0, 0, 800, 640))
FIREBALL_SPEED = 10
SCROLL_THRESH = 250
INITIAL_POS = (50, 50)
ROWS, COLS = 50, 150
TILE_SIZE = 32
FPS = 60

screen = pygame.display.set_mode(SCREEN_SIZE.size)

wall = pygame.image.load('sprites/wall.png').convert_alpha()
wall_scaled = pygame.transform.scale(wall, (TILE_SIZE,TILE_SIZE)).convert_alpha()
floor = pygame.image.load('sprites/floor.png').convert_alpha()
floor_scaled = pygame.transform.scale(floor, (TILE_SIZE,TILE_SIZE)).convert_alpha()

class Weapon:
    def __init__(self, fireball_image):
        self.image = fireball_image
        self.angle = 0 
        self.fireball_image = fireball_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()

    def update(self, player, scroll_x, scroll_y):
        fireball = None
        shot_cooldown = 300
        self.rect.center = player.rect.center
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)

        if x_dist > SCROLL_THRESH:
            self.angle = math.degrees(math.atan2(y_dist + scroll_y, x_dist + scroll_x))
        else:
            self.angle = math.degrees(math.atan2(y_dist + scroll_y, x_dist - scroll_x))

        if pygame.mouse.get_pressed()[0] and not self.fired and \
           (pygame.time.get_ticks() - self.last_shot) >= shot_cooldown:
            fireball = Fireball(
                self.fireball_image, 
                self.rect.centerx + scroll_x, 
                self.rect.centery + scroll_y, 
                self.angle
            )
            self.fired = True
            self.last_shot = pygame.time.get_ticks()
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False
        return fireball

class Fireball(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle 
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dx = math.cos(math.radians(self.angle)) * FIREBALL_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * FIREBALL_SPEED)
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        fireball_lifetime = 333

        if (pygame.time.get_ticks() - self.last_shot) >= fireball_lifetime:
            self.kill()

        if self.rect.right < 0 or self.rect.left > SCREEN_SIZE.width \
            or self.rect.bottom < 0 or self.rect.top > SCREEN_SIZE.height:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), 
            self.rect.centery - int(self.image.get_height()/2)))

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

    def update(self):
        pressed = pygame.key.get_pressed()
        left = pressed[pygame.K_LEFT] or pressed[pygame.K_a]
        right = pressed[pygame.K_RIGHT] or pressed[pygame.K_d]
        up = pressed[pygame.K_UP] or pressed[pygame.K_w]
        down = pressed[pygame.K_DOWN] or pressed[pygame.K_s]

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

    fireball_image = pygame.image.load("sprites/fireball.png").convert_alpha()
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

    weapon = Weapon(fireball_image)
    floors = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    fireball_group = pygame.sprite.Group()
    player = Player(platforms, INITIAL_POS)
    level_width  = len(world_data[0]) * TILE_SIZE
    level_height = len(world_data) * TILE_SIZE
    entities = CameraLayeredUpdates(player, pygame.Rect(0, 0, level_width, level_height))

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
            fireball = weapon.update(player, entities.cam.x, entities.cam.y)
            if fireball:
                fireball_group.add(fireball)
            for fireball in fireball_group:
                fireball.update()
                fireball.draw(screen)
                
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    try:
        main()
    except:
        sys.exit()