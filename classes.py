import pygame
from functions import *
from config import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Classes
class Crosshair(object):
    '''
    Creates a movable croshair.
    '''
    def __init__(self, coordinates: tuple = (0, 0)):
        self.x, self.y = coordinates
        self.width = 2
        self.height = 8
        self.middle_space_x = 3
        self.middle_space_y = 7
        self.color = LIGHT_GRAY

    def draw_self(self):
        # Draw top, bottom, left and right lines 
        pygame.draw.rect(screen, self.color, (self.x, self.y - self.middle_space_y, self.width, self.height))

        pygame.draw.rect(screen, self.color, (self.x, self.y + self.middle_space_y, self.width, self.height))

        pygame.draw.rect(screen, self.color, (self.x - self.middle_space_y - self.middle_space_x, self.y + self.middle_space_x, self.height, self.width))

        pygame.draw.rect(screen, self.color, (self.x + self.middle_space_y - self.middle_space_x, self.y + self.middle_space_x, self.height, self.width))

    def movement(self, coordinates: tuple):
        self.x, self.y = coordinates


class Dot(object):
    '''
    Base entity texture.
    '''
    def __init__(self, coordinates: tuple = (0, 0), radius: int = 0, color: int = BLACK):
        self.x, self.y = coordinates
        self.r = radius
        self.color = color

    def draw_self(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)


class Player(Dot):
    '''
    Child of Dot. Is the playable character.
    '''
    def __init__(self, coordinates: tuple = (0, 0), radius: int = 0, color: int = BLACK):
        super().__init__(coordinates, radius, color)
        # ! Who said stolen code ;)
        # Base speed factors
        self.speed = 1.3
        self.vx = 0
        self.vy = 0
        self.friction = 0.13
    
    def movement(self, key):
        if key[pygame.K_w]:
            self.vy -= self.speed
        if key[pygame.K_s]:
            self.vy += self.speed
        if key[pygame.K_a]:
            self.vx -= self.speed
        if key[pygame.K_d]:
            self.vx += self.speed

        # Apply friction.
        self.vx *= (1 - self.friction)
        self.vy *= (1 - self.friction)

        # Update position based on velocity.
        new_x = self.x + self.vx
        new_y = self.y + self.vy

        # Check if new position is outside the screen.
        if new_x < self.r:
            new_x = self.r
            self.vx = 0

        elif new_x > SCREEN_WIDTH - self.r:
            new_x = SCREEN_WIDTH - self.r
            self.vx = 0

        if new_y < self.r:
            new_y = self.r
            self.vy = 0

        elif new_y > SCREEN_HEIGHT - self.r:
            new_y = SCREEN_HEIGHT - self.r
            self.vy = 0

        # Set new coordinates.
        self.x = new_x
        self.y = new_y


class Bullet(object):
    '''
    Creates a shootable bullet.
    '''
    def __init__(self, coordinates: tuple = (0, 0), target_coordinates: tuple = (0, 0)):
        self.x, self.y = coordinates
        self.tx, self.ty = target_coordinates
        self.width = 5
        self.height = self.width
        self.color = YELLOW
        self.spawn_angle = calculate_angle(coordinates, target_coordinates)  # Different from bullet_angle for some reason.
        self.speed = 5
        self.bullet_angle = math.atan2(self.ty - self.y, self.tx - self.x)

        # Spawn a new bullet.
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.set_colorkey((0, 0, 0))
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()

        # Rotate the bullet.
        old_center = self.rect.center
        self.new = pygame.transform.rotate(self.surface, self.spawn_angle)
        self.rect = self.new.get_rect()
        self.rect.center = old_center

    def update(self):
        # Move bullet based on its rotation.
        self.x += math.cos(self.bullet_angle) * self.speed
        self.y += math.sin(self.bullet_angle) * self.speed

    def draw_self(self):
        # Redraw bullet.
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
        self.rect.center = (self.x, self.y)

        screen.blit(self.new, self.rect)


class Enemy_walker(Dot):
    '''
    Creates a walker enemy.
    '''
    def __init__(self, coordinates: tuple = (0, 0)):
        super().__init__(coordinates)
        self.r = 10
        self.color = RED
        self.speed = 1.3

    def movement(self, player_coordinates):
        x, y = player_coordinates
        dx = x - self.x
        dy = y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        self.x += dx / distance * self.speed * 2.3
        self.y += dy / distance * self.speed * 2.3


class Enemy_class1(Dot):
    '''
    Creates a class 1 enemy.
    '''
    def __init__(self, coordinates: tuple, spawnDirections: list):
        super().__init__(coordinates)
        self.r = 10
        self.color = PURPLE
        self.speed = 1
        self.vx = 1
        self.vy = 0
        self.spawnDirection = spawnDirections

    def movement(self):
        self.x += self.speed * self.vx
        self.y += self.speed * self.vy
        
        if self.x > 0 and self.x < SCREEN_WIDTH and self.y > 0 and self.y < SCREEN_HEIGHT:
            pixelColor = screen.get_at((self.x, self.y))
        else:
            pixelColor = (0, 0, 0)

        if pixelColor == GO_UP_COLOR:
            self.vy == 1

        if pixelColor == 0:  #go down
            self.vy == -1

        if pixelColor == GO_UP_COLOR:  # go left
            self.vx == 0

        if pixelColor == GO_UP_COLOR:  # go right
            self.vx == -0