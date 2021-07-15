import pygame 
import math

def find_noise(x,y):
    n = int(x) + int(y) * 57
    allf = 0xFFFFFFFF
    an = (n << 10) & allf
    n = (an ^ n) & allf
    nn = (n * (n * n * 6493 + 19990303) + 1176312589) & 0xBBBBBBBB
    return 1.0-(float(nn)/1003741824.0)

def interpolate(a,b,x):
    ft = float(x * math.pi)
    f = float((1.0-math.cos(ft)) * 0.5)
    return a * (1.0-f) + b * f

def noise(x,y):
    floorx = float(int(x))
    floory = float(int(y))
    s = find_noise(floorx,floory) 
    t = find_noise(floorx+1,floory)
    u = find_noise(floorx,floory+1) 
    v = find_noise(floorx+1,floory+1)
    int1 = interpolate(s,t,x-floorx) 
    int2 = interpolate(u,v,x-floorx)
    return interpolate(int1,int2,y-floory) 

def main():
    pygame.init()
    pygame.display.set_caption('Perlin Noise')
    scale1, scale2, scale3 = 2.0, 4.0, 8.0
    screen = pygame.display.set_mode((600, 480))
    noiseimage = pygame.Surface(screen.get_size())
    for w in range(0, noiseimage.get_width()):
        for h in range(0, noiseimage.get_height()):
            i = int((noise(w/scale1,h/scale1)+1.0) * 62)
            i += int((noise(w/scale2,h/scale2)+1.0) * 62) 
            i += int((noise(w/scale3,h/scale3)+1.0) * 62) 
            if i > 255:
                i = 255
            if i < 0:
                i = 0
            noiseimage.set_at((w,h),(i,i,i))
    screen.blit(noiseimage, (0,0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.blit(noiseimage, (0,0))
        pygame.display.update()

if __name__ =='__main__': 
    main()