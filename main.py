import pygame
import math

pygame.init()
win = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
fps = 30
clock = pygame.time.Clock()

class player:
    def __init__(self, p1x, p2x, p3x, p1y, p2y, p3y):
        self.p1x = p1x
        self.p2x = p2x
        self.p3x = p3x
        self.p1y = p1y
        self.p2y = p2y
        self.p3y = p3y
        self.yvel = 0
        self.xvel = 0
        self.angle = 0

new_player = player(200, 212.5, 206.25, 200, 200, 230)

radius = new_player.p3y - new_player.p1y

running = True
while running:
    clock.tick(fps)
    new_player.angle = new_player.angle % 360
    print(new_player.angle)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        
    win.fill((0, 0, 0))
    point_to_rotate_by = (new_player.p1x + ((new_player.p2x - new_player.p1x) / 2), new_player.p1y)
    angle = 0
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        new_player.p1y -= 5
        new_player.p2y -= 5
        new_player.p3y -= 5
    
    if keys[pygame.K_a]:
        angle += 2.5
        new_player.angle += 2.5

    if keys[pygame.K_d]:
        angle -= 2.5
        new_player.angle -= 2.5

    if angle > 0:
        angle -= 2.5
    
    new_player.p1x = (new_player.p1x - point_to_rotate_by[0]) * math.cos(math.radians(angle)) - (new_player.p1y - point_to_rotate_by[1]) * math.sin(math.radians(angle)) + point_to_rotate_by[0]
    new_player.p1y = (new_player.p1x - point_to_rotate_by[0]) * math.sin(math.radians(angle)) + (new_player.p1y - point_to_rotate_by[1]) * math.cos(math.radians(angle)) + point_to_rotate_by[1]
    new_player.p2x = (new_player.p2x - point_to_rotate_by[0]) * math.cos(math.radians(angle)) - (new_player.p2y - point_to_rotate_by[1]) * math.sin(math.radians(angle)) + point_to_rotate_by[0]
    new_player.p2y = (new_player.p2x - point_to_rotate_by[0]) * math.sin(math.radians(angle)) + (new_player.p2y - point_to_rotate_by[1]) * math.cos(math.radians(angle)) + point_to_rotate_by[1]
    new_player.p3x = (new_player.p3x - point_to_rotate_by[0]) * math.cos(math.radians(angle)) - (new_player.p3y - point_to_rotate_by[1]) * math.sin(math.radians(angle)) + point_to_rotate_by[0]
    new_player.p3y = (new_player.p3x - point_to_rotate_by[0]) * math.sin(math.radians(angle)) + (new_player.p3y - point_to_rotate_by[1]) * math.cos(math.radians(angle)) + point_to_rotate_by[1]

    pygame.draw.polygon(win, (255, 255, 255), ((new_player.p1x, new_player.p1y),
                                                (new_player.p2x, new_player.p2y), 
                                                (new_player.p3x, new_player.p3y)), 2)

    
    pygame.display.update()

