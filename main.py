import pygame
import math
import random

pygame.init()
win = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
pygame.display.set_caption("ASTEROIDS")
fps = 75
clock = pygame.time.Clock()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

asteroids = []
bullets = []
saucers = []

score = 0

class Player:
    def __init__(self, position, angle):
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = 0.25
        self.deceleration = 0.05
        self.max_speed = 5.0
        self.angle = angle
    
    def bullet_collision(self, saucer_list, score):
        for saucer in saucer_list:
            for bullet in saucer.self_bullets:
                if self.position.distance_to(bullet.position) <= 18 and bullet.player_bullet == False:
                    saucer.self_bullets.remove(bullet)
                    saucers.clear()
                    bullets.clear()
                    asteroids.clear()
                    self.position = pygame.math.Vector2(250, 250)
                    self.velocity = pygame.math.Vector2(0, 0)
                    self.angle = 270
                    score = 0
        return score

new_player = Player((200, 200), 270)
previous_velocity = pygame.math.Vector2(0, 1)
triangle_base = 40
triangle_size = 20  # Adjust the size of the triangle
score = 0

class Bullet:
    def __init__(self, position, velocity, player_bullet):
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(velocity)
        self.min_speed = 5.0
        self.player_bullet = player_bullet

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
            if self.position.distance_to(i.position) <= self.base_radius + 1 and self.size_modifier < 4 and i.player_bullet:
                bullet_list.remove(i)
                asteroid_list.remove(self)
                asteroid_list.append(Asteroid(self.position + pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)), (random.uniform(-1, 0), random.uniform(-0.5, 0.5)), self.size_modifier * 2))
                asteroid_list.append(Asteroid(self.position + pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)), (random.uniform(0, 1), random.uniform(-0.5, 0.5)), self.size_modifier * 2))
                if self.size_modifier == 1:
                    score += 250
                elif self.size_modifier == 2:
                    score += 100
            elif self.position.distance_to(i.position) <= self.base_radius + 1 and i.player_bullet:
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
            saucers.clear()
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

class Saucer:
    def __init__(self, position, velocity):
        self.size = random.choice([12, 16])
        self.position = position
        self.velocity = velocity
        self.time_to_switch = 0
        self.bullet_timer = 0
        self.self_bullets = []

    def switch_direction(self):
        self.velocity = pygame.math.Vector2(self.velocity.x, -self.velocity.y)
        self.time_to_switch = 0
    
    def shoot(self, player):
        new_bullet = Bullet(self.position, previous_velocity, False)
        to_player = pygame.math.Vector2(player.position - self.position)
        new_bullet.velocity = (to_player.normalize() * random.uniform(2, 2.5)) + (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
        self.self_bullets.append(new_bullet)
    
    def out_of_bounds(self):
        if self.position.x > 550:
            saucers.remove(self)
        elif self.position.x < -50:
            saucers.remove(self)
        if self.position.y > 500:
            saucers.remove(self)
        elif self.position.y < 0:
            saucers.remove(self)

    def bullet_out_of_bounds(self):
        for i in self.self_bullets:
            if i.position.x > 550:
                self.self_bullets.remove(i)
            elif i.position.x < -50:
                self.self_bullets.remove(i)
            if i.position.y > 500:
                self.self_bullets.remove(i)
            elif i.position.y < 0:
                self.self_bullets.remove(i)

    def bullet_amount(self):
        if len(self.self_bullets) > 4:
            self.self_bullets.pop(0)
    
    def bullet_collision(self, bullet_list, saucer_list, score):
        for i in bullet_list:
            if self.position.distance_to(i.position) <= self.size + 1 and i.player_bullet:
                bullet_list.remove(i)
                saucer_list.remove(self)
                score += 500
        return score

def asteroid_spawner(asteroids_list):
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

def saucer_spawner(saucer_list):
    side = random.choice(["left", "right"])

    if side == "left":
        position = (random.randint(-50, -25), random.randint(0, 500))
    elif side == "right":
        position = (random.randint(525, 550), random.randint(0, 500))

    saucer_list.append(Saucer(pygame.math.Vector2(position), (0,0)))

    to_player = pygame.math.Vector2(new_player.position - saucer_list[-1].position)
    saucer_list[-1].velocity = to_player.normalize() * random.uniform(1.25, 1.5)
    return saucer_list

timer = 0
timer2 = 0

running = True

while running:
    clock.tick(fps)
    timer += 0.01
    timer2 += 0.01
    new_player.angle = new_player.angle % 360
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            nose_position = new_player.position + pygame.math.Vector2(triangle_base / 2, 0).rotate(-new_player.angle)

            new_bullet = Bullet(nose_position, previous_velocity, True)
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

    if timer > 0.5 and len(asteroids) < 1:
        asteroids = asteroid_spawner(asteroids)
        timer = 0

    if len(saucers) < 1 and timer2 > 1:
        saucers = saucer_spawner(saucers)
        timer2 = 0

    new_player.bullet_collision(saucers, score)

    pygame.draw.polygon(win, (255, 255, 255), (player_rotated_point1, player_rotated_point2, player_rotated_point3), 1)

    for bullet in bullets:
        bullet.position += bullet.velocity
        bullet.out_of_bounds(bullets)
        pygame.draw.circle(win, (255, 255, 255), (int(bullet.position.x), int(bullet.position.y)), 1)

    for saucer in saucers:
        saucer.out_of_bounds()
        saucer.bullet_out_of_bounds()
        saucer.bullet_amount()
        score = saucer.bullet_collision(bullets, saucers, score)
        if saucer.time_to_switch > 1.5 + random.uniform(-0.5, 0.5):
            saucer.switch_direction()
        if saucer.bullet_timer > 1 + random.uniform(-0.5, 0.5):
            saucer.shoot(new_player)
            saucer.bullet_timer = 0
        for i in saucer.self_bullets:
            i.position += i.velocity
            pygame.draw.circle(win, (255, 255, 255), (int(i.position.x), int(i.position.y)), 1)
        saucer.bullet_timer += 0.01
        saucer.time_to_switch += 0.01
        saucer.position += saucer.velocity
        pygame.draw.circle(win, (255, 255, 255), (int(saucer.position.x), int(saucer.position.y)), saucer.size, 1)


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
