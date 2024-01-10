import pygame
import math
import random

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
triangle_base = 40
triangle_size = 20  # Adjust the size of the triangle

class Bullet:
    def __init__(self, position, velocity):
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(velocity)
        self.min_speed = 5.0

class Asteroid:
    def __init__(self, position, velocity):
        self.position = pygame.math.Vector2(position)
        self.init_pos = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(velocity)
        self.max_speed = 5.0
        self.angle = 0
        self.points = []
        self.generate_shape()

    def generate_shape(self):
        num_points = 12
        base_radius = random.randint(10,20)
        irregularity = 7.5  # Adjust the irregularity factor

        for i in range(num_points):
            angle = math.radians(360 * i / num_points)
            radius = base_radius + random.uniform(-irregularity, irregularity)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            self.points.append(pygame.math.Vector2(x, y))
        
        self.points = [self.position + point.rotate(-self.angle) for point in self.points]
        

test_asteroid = Asteroid((100, 100),  (random.uniform(-5, 5), random.uniform(-5, 5))) 

bullets = []

running = True

previous_velocity = pygame.math.Vector2(0, 1)

while running:
    clock.tick(fps)
    new_player.angle = new_player.angle % 360
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
    
    player_rotated_point1 = new_player.position + pygame.math.Vector2(triangle_base / 2, 0).rotate(-new_player.angle)
    player_rotated_point2 = new_player.position + pygame.math.Vector2(triangle_size / 2, 0).rotate(-new_player.angle + 120)
    player_rotated_point3 = new_player.position + pygame.math.Vector2(triangle_size / 2, 0).rotate(-new_player.angle - 120)


    test_asteroid.position.x += test_asteroid.velocity.x
    test_asteroid.position.y += test_asteroid.velocity.y
    test_asteroid.velocity.scale_to_length(min(test_asteroid.velocity.length(), test_asteroid.max_speed))

    for i in range(len(test_asteroid.points)):
        test_asteroid.points[i] += test_asteroid.velocityaw

    pygame.draw.polygon(win, (255, 255, 255), test_asteroid.points, 1)

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

    pygame.draw.polygon(win, (255, 255, 255), (player_rotated_point1, player_rotated_point2, player_rotated_point3), 1)

    for bullet in bullets:
        bullet.position += bullet.velocity
        pygame.draw.circle(win, (255, 255, 255), (int(bullet.position.x), int(bullet.position.y)), 1)

    pygame.display.update()

pygame.quit()
