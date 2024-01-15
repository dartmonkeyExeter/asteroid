import pygame
import math
import random

pygame.init()
win = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("ASTEROIDS")
fps = 75
clock = pygame.time.Clock()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

asteroids = []
bullets = []
saucers = []
saucer_bullets = []

score = 0

class Player:
    def __init__(self, position, angle):
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = 0.25
        self.deceleration = 0.05
        self.max_speed = 5.0
        self.angle = angle
    
    def bullet_collision(self, saucer_list, score, bullets):
        for saucer in saucer_list:
            for bullet in bullets:
                if self.position.distance_to(bullet.position) <= 17 and bullet.player_bullet == False:
                    bullets.remove(bullet)
                    saucers.clear()
                    bullets.clear()
                    asteroids.clear()
                    self.position = pygame.math.Vector2(pygame.display.get_surface().get_width() / 2, pygame.display.get_surface().get_height() / 2)
                    self.velocity = pygame.math.Vector2(0, 0)
                    self.angle = 270
                    score = 0
        return score

new_player = Player(pygame.math.Vector2(pygame.display.get_surface().get_width() / 2, pygame.display.get_surface().get_height() / 2), 270)
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
        if self.position.x > pygame.display.get_surface().get_width():
            bullet_list.remove(self)
        elif self.position.x < 0:
            bullet_list.remove(self)
        if self.position.y > pygame.display.get_surface().get_height():
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
    
    def bullet_collision(self, bullet_list, asteroid_list, score, saucer_bullets):
        for i in bullet_list:
            if self.position.distance_to(i.position) <= self.base_radius + 1 and self.size_modifier < 4:
                bullet_list.remove(i)
                asteroid_list.remove(self)
                for i in range(self.size_modifier):
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
        for i in saucer_bullets:
            if self.position.distance_to(i.position) <= self.base_radius + 1 and self.size_modifier < 4:
                saucer_bullets.remove(i)
                asteroid_list.remove(self)
                for i in range(self.size_modifier):
                    asteroid_list.append(Asteroid(self.position + pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)), (random.uniform(-1, 0), random.uniform(-0.5, 0.5)), self.size_modifier * 2))
                    asteroid_list.append(Asteroid(self.position + pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)), (random.uniform(0, 1), random.uniform(-0.5, 0.5)), self.size_modifier * 2))
            elif self.position.distance_to(i.position) <= self.base_radius + 1:
                saucer_bullets.remove(i)
                asteroid_list.remove(self)
        
        return score
    
    def player_collision(self, player, score, prev):
        if self.position.distance_to(player.position) <= self.base_radius + triangle_base / 2 - 1.5:
            player.position = pygame.math.Vector2(pygame.display.get_surface().get_width() / 2, pygame.display.get_surface().get_height() / 2)
            player.velocity = pygame.math.Vector2(0, 0)
            player.angle = 270
            prev = pygame.math.Vector2(0, 1)
            asteroids.clear()
            saucers.clear()
            bullets.clear()
            score = 0
        return score, prev
    
    def saucer_collision(self, saucer_list, asteroid_list):
        for i in saucer_list:
            if self.position.distance_to(i.position) <= self.base_radius + i.size and self.size_modifier < 4:
                saucer_list.remove(i)
                asteroid_list.remove(self)
                for i in range(self.size_modifier):
                    asteroid_list.append(Asteroid(self.position + pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)), (random.uniform(-1, 0), random.uniform(-0.5, 0.5)), self.size_modifier * 2))
                    asteroid_list.append(Asteroid(self.position + pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)), (random.uniform(0, 1), random.uniform(-0.5, 0.5)), self.size_modifier * 2))
            elif self.position.distance_to(i.position) <= self.base_radius + i.size:
                asteroid_list.remove(self)
                saucer_list.remove(i)

    def out_of_bounds(self, asteroid_list):
        if self.position.x > pygame.display.get_surface().get_width() + 50:
            asteroid_list.remove(self)
        elif self.position.x < -50:
            asteroid_list.remove(self)
        if self.position.y > pygame.display.get_surface().get_height() + 50:
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

    def switch_direction(self):
        self.velocity = pygame.math.Vector2(self.velocity.x, -self.velocity.y)
        self.time_to_switch = 0
    
    def shoot(self, player, bullets):
        new_bullet = Bullet(self.position, previous_velocity, False)
        to_player = pygame.math.Vector2(player.position - self.position)
        new_bullet.velocity = (to_player.normalize() * random.uniform(2, 2.5)) + (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
        bullets.append(new_bullet)
    
    def out_of_bounds(self):
        if self.position.x > pygame.display.get_surface().get_width() + 50:
            saucers.remove(self)
        elif self.position.x < -50:
            saucers.remove(self)
        if self.position.y > pygame.display.get_surface().get_height() + 50:
            saucers.remove(self)
        elif self.position.y < 0:
            saucers.remove(self)

    def bullet_out_of_bounds(self, bullets):
        for i in bullets:
            if i.position.x > pygame.display.get_surface().get_width():
                bullets.remove(i)
            elif i.position.x < 0:
                bullets.remove(i)
            if i.position.y > pygame.display.get_surface().get_height():
                bullets.remove(i)
            elif i.position.y < 0:
                bullets.remove(i)

    def bullet_amount(self, bullets):
        if len(bullets) > 4:
            bullets.pop(0)
    
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
        position = (random.randint(pygame.display.get_surface().get_width() - 50, pygame.display.get_surface().get_width() - 25), random.randint(0, pygame.display.get_surface().get_height()))
    elif side == "right":
        position = (random.randint(pygame.display.get_surface().get_width() + 25, pygame.display.get_surface().get_width() + 50), random.randint(0, pygame.display.get_surface().get_height()))
    elif side == "top":
        position = (random.randint(0, pygame.display.get_surface().get_width()), random.randint(-50, -25))
    elif side == "bottom":
        position = (random.randint(0, pygame.display.get_surface().get_width()), random.randint(pygame.display.get_surface().get_height() + 25, pygame.display.get_surface().get_height() + 50))
    
    asteroids_list.append(Asteroid(position, (0, 0), 1))
    
    to_player = pygame.math.Vector2(new_player.position - asteroids_list[-1].position)
    asteroids_list[-1].velocity = to_player.normalize() * random.uniform(0.5, 1.5)
    return asteroids_list

def saucer_spawner(saucer_list):
    side = random.choice(["left", "right"])

    if side == "left":
        position = (random.randint(pygame.display.get_surface().get_width()-50, pygame.display.get_surface().get_width()-25), random.randint(0, pygame.display.get_surface().get_height()))
    elif side == "right":
        position = (random.randint(pygame.display.get_surface().get_width()+25, pygame.display.get_surface().get_width()+50), random.randint(0, pygame.display.get_surface().get_height()))

    saucer_list.append(Saucer(pygame.math.Vector2(position), (0,0)))

    to_player = pygame.math.Vector2(new_player.position - saucer_list[-1].position)
    saucer_list[-1].velocity = to_player.normalize() * random.uniform(1.25, 1.5)
    return saucer_list

timer = 0
timer2 = 0

running = True

while running:
    clock.tick(fps)
    print(clock.get_fps())
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

    if new_player.position.x > pygame.display.get_surface().get_width():
        new_player.position.x = 0
    elif new_player.position.x < 0:
        new_player.position.x = pygame.display.get_surface().get_width()
    if new_player.position.y > pygame.display.get_surface().get_height():
        new_player.position.y = 0
    elif new_player.position.y < 0:
        new_player.position.y = pygame.display.get_surface().get_height()

    if len(bullets) > 8:
        bullets.pop(0)

    if timer > 0.5 and len(asteroids) < 15:
        asteroids = asteroid_spawner(asteroids)
        timer = 0

    if len(saucers) < 2 and timer2 > 15:
        saucers = saucer_spawner(saucers)
        timer2 = 0

    score = new_player.bullet_collision(saucers, score, saucer_bullets)

    pygame.draw.polygon(win, (255, 255, 255), (player_rotated_point1, player_rotated_point2, player_rotated_point3), 1)

    for bullet in bullets:
        bullet.position += bullet.velocity
        bullet.out_of_bounds(bullets)
        pygame.draw.circle(win, (255, 255, 255), (int(bullet.position.x), int(bullet.position.y)), 1)

    for saucer in saucers:
        saucer.out_of_bounds()
        saucer.bullet_out_of_bounds(saucer_bullets)
        saucer.bullet_amount(saucer_bullets)
        score = saucer.bullet_collision(bullets, saucers, score)
        if saucer.time_to_switch > 1.5 + random.uniform(-0.5, 0.5):
            saucer.switch_direction()
        if saucer.bullet_timer > 1 + random.uniform(-0.5, 0.5):
            saucer.shoot(new_player, saucer_bullets)
            saucer.bullet_timer = 0
        for i in saucer_bullets:
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
        score = ast.bullet_collision(bullets, asteroids, score, saucer_bullets)
        ast.saucer_collision(saucers, asteroids)
        score, previous_velocity = ast.player_collision(new_player, score, previous_velocity)
        ast.out_of_bounds(asteroids)



    points_dis = my_font.render(f'{str(score)}', False, (255, 255, 255))
    win.blit(points_dis, (50,10))

    pygame.display.update()

pygame.quit()
