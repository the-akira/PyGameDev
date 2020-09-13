from pygame import *
import pygame

SCREEN_SIZE = pygame.Rect((0, 0, 800, 640))
INITIAL_POS = (35, 700)
BACKGROUND_BLUE = (104, 136, 247)
GRAVITY = pygame.Vector2((0, 0.29))
TILE_SIZE = 32

class CameraLayeredUpdates(pygame.sprite.LayeredUpdates):
    def __init__(self, target, world_size):
        super().__init__()
        self.target = target
        self.cam = pygame.Vector2(0, 0)
        self.world_size = world_size
        if self.target:
            self.add(target)

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + SCREEN_SIZE.width/2
            y = -self.target.rect.center[1] + SCREEN_SIZE.height/2
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
    def __init__(self, color, pos, *groups):
        super().__init__(*groups)
        self.image = Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

class Player(Entity):
    def __init__(self, platforms, pos, *groups):
        super().__init__(Color("#0000FF"), pos)
        self.image_load = pygame.image.load('mario.png').convert_alpha()
        self.image = pygame.transform.scale(self.image_load, (55,65))
        self.rect = self.image.get_rect(topleft=pos)
        self.vel = pygame.Vector2((0, 0))
        self.onGround = False
        self.platforms = platforms
        self.speed = 6
        self.jump_strength = 9

    def update(self):
        pressed = pygame.key.get_pressed()
        up = pressed[K_UP]
        left = pressed[K_LEFT]
        right = pressed[K_RIGHT]
        running = pressed[K_SPACE]

        if up:
            # only jump if on the ground
            if self.onGround: self.vel.y = -self.jump_strength
        if left:
            self.vel.x = -self.speed
        if right:
            self.vel.x = self.speed
        if running:
            self.vel.x *= 1.3
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.vel += GRAVITY
            # max falling speed
            if self.vel.y > 100: self.vel.y = 100
        if not(left or right):
            self.vel.x = 0
        # increment in x direction
        self.rect.left += self.vel.x
        # do x-axis collisions
        self.collide(self.vel.x, 0, self.platforms)
        # increment in y direction
        self.rect.top += self.vel.y
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.vel.y, self.platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom

class Platform(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#BE521C"), pos, *groups)
        self.image_load = pygame.image.load('brick.png').convert_alpha()
        self.image = pygame.transform.scale(self.image_load, (32,32))

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE.size)
    pygame.display.set_caption("Mario")
    timer = pygame.time.Clock()

    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                                       P",
        "P                                                       P",
        "P                                                       P",
        "P                    PPPPPPPPPPP                        P",
        "P                                                       P",
        "P                                            PPPPP      P",
        "P                                                       P",
        "P    PPPPPPPP                                           P",
        "P                                                     PPP",
        "P                          PPPPPPP                      P",
        "P                 PPPPPP                                P",
        "P                                                       P",
        "P         PPPPPPP                                PP     P",
        "P                                               P       P",
        "P                     PPPPPP          PPPPPPPPPP        P",
        "P                                                       P",
        "P   PPPPPPPPPPP                                         P",
        "P                                                       P",
        "P                 PPPPPPPPPPP      PPP        PPPPPPPPPPP",
        "P                                                       P",
        "P                                                       P",
        "P                                                       P",
        "P                                                       P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]

    platforms = pygame.sprite.Group()
    player = Player(platforms, INITIAL_POS)
    level_width  = len(level[0])*TILE_SIZE
    level_height = len(level)*TILE_SIZE
    entities = CameraLayeredUpdates(player, pygame.Rect(0, 0, level_width, level_height))

    # build the level
    x = y = 0
    for row in level:
        for col in row:
            if col == "P":
                Platform((x, y), platforms, entities)
            x += TILE_SIZE
        y += TILE_SIZE
        x = 0

    while True:
        for e in pygame.event.get():
            if e.type == QUIT: 
                return
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                return

        entities.update()
        screen.fill(BACKGROUND_BLUE)
        entities.draw(screen)
        pygame.display.update()
        timer.tick(60)

if __name__ == "__main__":
    main()