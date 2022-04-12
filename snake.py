
import sys
import random
import pygame
from pygame.math import Vector2

class Snake:
    def __init__(self) -> None:
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = Vector2(1,0)

    def draw(self):
        for block in self.body:
            rect = pygame.Rect(block.x * cell_size,
                               block.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, pygame.Color('pink'), rect)

    def move(self):
        body_copy = self.body[:-1]
        body_copy.insert(0,body_copy[0] + self.direction)
        self.body = body_copy[:]

class Fruit:
    def __init__(self) -> None:
        
        self.pos = Vector2(random.randint(0, cell_number - 1),
                           random.randint(0, cell_number - 1))

    def draw(self):
        rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, pygame.Color('purple'), rect)

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode(
    (cell_size * cell_number, cell_size * cell_number))
screen.fill((87,100,87))
clock = pygame.time.Clock()
fruit = Fruit()
snake = Snake()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            snake.move()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.direction = Vector2(0,-1)
            elif event.key == pygame.K_DOWN:
                snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_LEFT:
                snake.direction = Vector2(-1, 0)    
            elif event.key == pygame.K_RIGHT:
                snake.direction = Vector2(1, 0)
                
    screen.fill((87, 100, 87))
    fruit.draw()
    snake.draw()
    pygame.display.update()
    clock.tick(60)
