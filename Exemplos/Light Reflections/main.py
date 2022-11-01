from math import atan2, degrees, pi
import pygame

pygame.init()
SIZE = (WIDTH, HEIGHT) = 1280, 720
display = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Light Reflections")
BACKGROUND_COLOR = (0,0,0)
RECTANGLE_COLOR = (66,166,46)
TEXT_COLOR = (210,210,210)
FPS = 60

vec = pygame.math.Vector2
distance = vec(0,-2000)

reflect = False
reflections = 5
objects = [] # Lista de retângulos
objects.append(pygame.Rect(0,0,120,110))

rays = 10 # número de raios da origem
draw = False # flag para desenhar objetos
rotation = False  
rot = 0

font = pygame.font.SysFont('square721cn',40)
font2 = pygame.font.SysFont('square721cn',24)
clock = pygame.time.Clock()

def Light(origin,direction,bounces,objects,c=False):
    origin = origin # Coordenadas de início de linha
    direction = vec(direction) # Vetor especificando a direção do raio
    end = origin # Coordenadas de fim de linha 
    bounces = bounces
    colour = [(50,50,50),(50,50,50),(100,100,100),(150,150,150),(200,200,200),(255,255,255)]
    colour = colour[bounces] # A cor do raio depende de quantas vezes ele foi refletido
    hit = False # hit flag

    while True:
        end += direction.normalize() * 50 # Incremente o raio pouco a pouco para detectar colisões
        for obj in objects:      
            clipped_line = obj.clipline(origin,end) # Checar por colisão
            if clipped_line and bounces != 0: # Limite para reflexões
                start1 = clipped_line[0]
                hit_start = list(start1) # Coordenadas de onde o raio atinge
                end = hit_start # O fim do raio é onde ele atinge
                if hit_start[0] >= obj.right - 1: # Reflexão com base em onde o raio atingiu
                    direction[0] *= -1
                    end[0] += 1
                elif hit_start[0] <= obj.left:
                    direction[0] *= -1
                    end[0] -= 1
                elif hit_start[1] <= obj.top:
                    direction[1] *= -1
                    end[1] -= 1
                elif hit_start[1] >= obj.bottom - 1:
                    direction[1] *= -1
                    end[1] += 1
                hit = True    
                break
        if hit or (end).length() > 2000: # Comprimento máximo para o raio
            break

    pygame.draw.line(display,colour,origin,end,bounces) # Desenhar o raio

    if hit and reflect:
        bounces -= 1
        Light(hit_start,direction,bounces,objects) # Crie um novo raio começando de onde o raio pai atingiu
    else:
        return

while True:
    clock.tick(FPS)
    display.fill(BACKGROUND_COLOR)
    clock_fps = clock.get_fps()
    fps_text = font.render(str(int(clock_fps)),False,TEXT_COLOR)
    rays_text = font2.render("RAYS= "+str(rays),False,TEXT_COLOR)
    rotate_text = font2.render("ROTATE",False,TEXT_COLOR)
    reflect_text = font2.render("REFLECT",False,TEXT_COLOR)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                reflect = not reflect
            elif event.button == 3: 
                draw = True
                startpos = list(pygame.mouse.get_pos()) # Posição do mouse para desenhar objetos
            elif event.button == 4:
                if rays > 1:
                    rays -= 1
            elif event.button == 5:
                if rays < 360:
                    rays += 1
        elif event.type == pygame.MOUSEBUTTONUP:
            if draw:
                draw = False # Parar de desenhar
                objects.append(pygame.Rect(topleft[0],topleft[1],xdist,ydist))  
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                objects = [pygame.Rect(0,0,120,110)]
            elif event.key == pygame.K_SPACE:
                rotation = not rotation
            
    if draw:
        topleft = list(startpos) # Criando e desenhando objetos
        curpos = list(pygame.mouse.get_pos())
        xdist = abs(curpos[0]-topleft[0])
        ydist = abs(curpos[1]-topleft[1])
        if curpos[0] < topleft[0]:
            if curpos[1] < topleft[1]:
                topleft = curpos
            else:
                topleft[0] -= xdist
        elif curpos[1] < topleft[1]:
            topleft[1] -= ydist
        pygame.draw.rect(display,RECTANGLE_COLOR,(topleft[0],topleft[1],xdist,ydist),4)

    if objects:
        for obj in objects[1:]:
            pygame.draw.rect(display,RECTANGLE_COLOR,obj,4) # Apresentando objetos

    origin = pygame.mouse.get_pos() # Coordenadas das fontes de luz

    angle = 0
    for k in range(rays):   
        angle += 360/rays
        nline = distance.rotate(angle+rot) # Rotação do raio de origem
        Light(origin,nline,5,objects,True) # Criando raios de origem

    if rotation:
        rot += 0.2
    else:
        pygame.draw.line(display,TEXT_COLOR,(5,95),(72,95),5) # Rotação da UI tachada

    display.blit(fps_text,(7,5))
    display.blit(rays_text,(7,40))
    display.blit(reflect_text,(7,60))
    display.blit(rotate_text,(7,80))

    if not reflect:
        pygame.draw.line(display,TEXT_COLOR,(5,75),(80,75),5) # Reflexão da UI tachada

    pygame.display.update()