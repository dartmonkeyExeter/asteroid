import pygame
import math

pygame.init()
win = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
fps = 60
clock = pygame.time.Clock()

class Player:
    def __init__(self, position, angle):
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = 0.25
        self.deceleration = 0.05
        self.max_speed = 5.0
        self.angle = angle

new_player = Player((200, 200), 270)

class Bullet:
    def __init__(self, position, velocity):
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(velocity)
        self.min_speed = 5.0

triangle_base = 40
triangle_size = 20  # Adjust the size of the triangle

bullets = []

running = True

previous_velocity = pygame.math.Vector2(0, 1)

while running:
    clock.tick(fps)
    new_player.angle = new_player.angle % 360
    print(new_player.angle)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            nose_position = new_player.position + pygame.math.Vector2(triangle_base / 2, 0).rotate(-new_player.angle)

            new_bullet = Bullet(nose_position, previous_velocity)
            new_bullet.velocity.y -= new_bullet.min_speed * math.sin(math.radians(new_player.angle))
            new_bullet.velocity.x += new_bullet.min_speed * math.cos(math.radians(new_player.angle))
            bullets.append(new_bullet)


    win.fill((0, 0, 0))
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        new_player.velocity.y -= new_player.acceleration * math.sin(math.radians(new_player.angle))
        new_player.velocity.x += new_player.acceleration * math.cos(math.radians(new_player.angle))
        
        # Cap the speed
        previous_velocity = new_player.velocity
        new_player.velocity.scale_to_length(min(new_player.velocity.length(), new_player.max_speed))
    else:
        # Deceleration when 'W' is not pressed
        new_player.velocity *= 1 - new_player.deceleration
    if keys[pygame.K_d]:
        new_player.angle += 2.5

    if keys[pygame.K_a]:
        new_player.angle -= 2.5
    
    new_player.position += new_player.velocity
    
    rotated_point1 = new_player.position + pygame.math.Vector2(triangle_base / 2, 0).rotate(-new_player.angle)
    rotated_point2 = new_player.position + pygame.math.Vector2(triangle_size / 2, 0).rotate(-new_player.angle + 120)
    rotated_point3 = new_player.position + pygame.math.Vector2(triangle_size / 2, 0).rotate(-new_player.angle - 120)

    if new_player.position.x > 500:
        new_player.position.x = 0
    elif new_player.position.x < 0:
        new_player.position.x = 500
    if new_player.position.y > 500:
        new_player.position.y = 0
    elif new_player.position.y < 0:
        new_player.position.y = 500

    if len(bullets) > 4:
        bullets.pop(0)

    pygame.draw.polygon(win, (255, 255, 255), (rotated_point1, rotated_point2, rotated_point3), 1)
    for bullet in bullets:
        bullet.position += bullet.velocity
        pygame.draw.circle(win, (255, 255, 255), (int(bullet.position.x), int(bullet.position.y)), 1)

    pygame.display.update()

pygame.quit()
