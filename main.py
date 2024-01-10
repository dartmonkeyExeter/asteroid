import pygame

pygame.init()
win = pygame.display.set_mode((500, 500))
fps = 60
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

new_player = player(200, 212.5, 206.25, 200, 200, 230)

running = True
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            new_player.yvel = -1
    win.fill((0, 0, 0))

    new_player.p1y += new_player.yvel
    new_player.p2y += new_player.yvel
    new_player.p3y += new_player.yvel
    new_player.p1x += new_player.xvel
    new_player.p2x += new_player.xvel
    new_player.p3x += new_player.xvel

    pygame.draw.polygon(win, (255, 255, 255), ((new_player.p1x, new_player.p1y),
                                                (new_player.p2x, new_player.p2y), 
                                                (new_player.p3x, new_player.p3y)), 2)

    
    pygame.display.update()

