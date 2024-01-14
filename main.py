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
    def __init__(self, position, velocity, size_modifier):
        self.position = pygame.math.Vector2(position)
        self.init_pos = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(velocity)
        self.max_speed = 5.0
        self.base_radius = 0
        self.size_modifier = size_modifier
        self.angle = 0
        self.points = []
        self.generate_shape()

    def generate_shape(self):
        num_points = math.ceil(12 / self.size_modifier)
        self.base_radius = random.randint(10,20) / self.size_modifier
        irregularity = 7.5 / self.size_modifier # Adjust the irregularity factor

        for i in range(num_points):
            angle = math.radians(360 * i / num_points)
            radius = self.base_radius + random.uniform(-irregularity, irregularity)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            self.points.append(pygame.math.Vector2(x, y))
        
        self.points = [self.position + point.rotate(-self.angle) for point in self.points]
    
    def bullet_collision(self, bullet_list, asteroid_list):
        for i in bullet_list:
            if self.position.distance_to(i.position) < self.base_radius + 1 and self.size_modifier == 1:
                bullet_list.remove(i)
                asteroid_list.remove(self)
                asteroid_list.append(Asteroid(self.position + pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)), (random.uniform(-1, 0), random.uniform(-0.5, 0.5)), self.size_modifier * 2))
                asteroid_list.append(Asteroid(self.position + pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)), (random.uniform(0, 1), random.uniform(-0.5, 0.5)), self.size_modifier * 2))
            elif self.position.distance_to(i.position) < self.base_radius + 1:
                bullet_list.remove(i)
                asteroid_list.remove(self)
    def player_collision(self, player):
        if self.position.distance_to(player.position) < self.base_radius - 1:
            print("Collision")
    
    def out_of_bounds(self, asteroid_list):
        if self.position.x > 600:
            asteroid_list.remove(self)
        elif self.position.x < -100:
            self.position.x = 500
        if self.position.y > 500:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = 500

asteroids = []
bullets = []

def asteroid_spawner():
    # Determine a random side of the screen (left, right, top, or bottom)
    side = random.choice(["left", "right", "top", "bottom"])
    
    if side == "left":
        position = (random.randint(-50, -25), random.randint(0, 500))
    elif side == "right":
        position = (random.randint(525, 550), random.randint(0, 500))
    elif side == "top":
        position = (random.randint(0, 500), random.randint(-50, -25))
    elif side == "bottom":
        position = (random.randint(0, 500), random.randint(525, 550))
    
    asteroids.append(Asteroid(position, (0, 0), 1))
    
    to_player = pygame.math.Vector2(new_player.position - asteroids[-1].position)
    asteroids[-1].velocity = to_player.normalize() * random.uniform(0.5, 1.5)


for i in range(2):
    asteroid_spawner()

timer = 0

running = True

previous_velocity = pygame.math.Vector2(0, 1)

while running:
    clock.tick(fps)
    timer += 0.01
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

    if len(asteroids) < 15 and timer > 1:
        asteroid_spawner()
        timer = 0

    for ast in asteroids:
        ast.position += ast.velocity
        for i in range(len(ast.points)):
            ast.points[i] += ast.velocity
        pygame.draw.polygon(win, (255, 255, 255), ast.points, 1)
        ast.velocity.scale_to_length(min(ast.velocity.length(), ast.max_speed))
        ast.bullet_collision(bullets, asteroids)
        ast.player_collision(new_player)
        ast.out_of_bounds(asteroids)

    pygame.display.update()

pygame.quit()
