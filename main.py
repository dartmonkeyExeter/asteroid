import pygame
import math
import random

pygame.init()
win = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
fps = 75
clock = pygame.time.Clock()
my_font = pygame.font.SysFont('Roboto', 30)

class Player:
    def __init__(self, position, angle):
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = 0.25
        self.deceleration = 0.05
        self.max_speed = 5.0
        self.angle = angle

new_player = Player((200, 200), 270)
previous_velocity = pygame.math.Vector2(0, 1)
triangle_base = 40
triangle_size = 20  # Adjust the size of the triangle
score = 0

class Bullet:
    def __init__(self, position, velocity):
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(velocity)
        self.min_speed = 5.0
    
    def out_of_bounds(self, bullet_list):
        if self.position.x > 500:
            bullet_list.remove(self)
        elif self.position.x < 0:
            bullet_list.remove(self)
        if self.position.y > 500:
            bullet_list.remove(self)
        elif self.position.y < 0:
            bullet_list.remove(self)

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
        self.irregularity = 7.5 / self.size_modifier # Adjust the irregularity factor

        for i in range(num_points):
            angle = math.radians(360 * i / num_points)
            radius = self.base_radius + random.uniform(0, self.irregularity)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            self.points.append(pygame.math.Vector2(x, y))
        
        self.points = [self.position + point.rotate(-self.angle) for point in self.points]
    
    def bullet_collision(self, bullet_list, asteroid_list, score):
        for i in bullet_list:
            if self.position.distance_to(i.position) <= self.base_radius + 1 and self.size_modifier < 4:
                bullet_list.remove(i)
                asteroid_list.remove(self)
                asteroid_list.append(Asteroid(self.position + pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)), (random.uniform(-1, 0), random.uniform(-0.5, 0.5)), self.size_modifier * 2))
                asteroid_list.append(Asteroid(self.position + pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)), (random.uniform(0, 1), random.uniform(-0.5, 0.5)), self.size_modifier * 2))
                if self.size_modifier == 1:
                    score += 250
                elif self.size_modifier == 2:
                    score += 100
            elif self.position.distance_to(i.position) <= self.base_radius + 1:
                bullet_list.remove(i)
                asteroid_list.remove(self)
                score += 25
        return score
    def player_collision(self, player, score, prev):
        if self.position.distance_to(player.position) <= self.base_radius + triangle_base / 2 - 1.5:
            player.position = pygame.math.Vector2(250, 250)
            player.velocity = pygame.math.Vector2(0, 0)
            player.angle = 270
            prev = pygame.math.Vector2(0, 1)
            asteroids.clear()
            bullets.clear()
            score = 0
        return score, prev
    
    def out_of_bounds(self, asteroid_list):
        if self.position.x > 550:
            asteroid_list.remove(self)
        elif self.position.x < -50:
            asteroid_list.remove(self)
        if self.position.y > 500:
            asteroid_list.remove(self)
        elif self.position.y < 0:
            asteroid_list.remove(self)

asteroids = []
bullets = []
score = 0

def asteroid_spawner(asteroids_list):
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
    
    asteroids_list.append(Asteroid(position, (0, 0), 1))
    
    to_player = pygame.math.Vector2(new_player.position - asteroids_list[-1].position)
    asteroids_list[-1].velocity = to_player.normalize() * random.uniform(0.5, 1.5)
    return asteroids_list

timer = 0

running = True

while running:
    clock.tick(fps)
    print(clock.get_fps())
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

    if timer > 0.5 and len(asteroids) < 15:
        asteroids = asteroid_spawner(asteroids)
        timer = 0

    pygame.draw.polygon(win, (255, 255, 255), (player_rotated_point1, player_rotated_point2, player_rotated_point3), 1)

    for bullet in bullets:
        bullet.position += bullet.velocity
        bullet.out_of_bounds(bullets)
        pygame.draw.circle(win, (255, 255, 255), (int(bullet.position.x), int(bullet.position.y)), 1)

    for ast in asteroids:
        ast.position += ast.velocity
        for i in range(len(ast.points)):
            ast.points[i] += ast.velocity
        pygame.draw.polygon(win, (255, 255, 255), ast.points, 1)
        ast.velocity.scale_to_length(min(ast.velocity.length(), ast.max_speed))
        score = ast.bullet_collision(bullets, asteroids, score)
        score, previous_velocity = ast.player_collision(new_player, score, previous_velocity)
        ast.out_of_bounds(asteroids)

    points_dis = my_font.render(f'{str(score)}', False, (255, 255, 255))
    win.blit(points_dis, (50,10))

    pygame.display.update()

pygame.quit()
