
import sys
import random
from threading import Timer
import pygame
from pygame.math import Vector2

v_up = Vector2(0, -1)
v_down = Vector2(0, 1)
v_left = Vector2(-1, 0)
v_right = Vector2(1, 0)

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))

class Snake:
    snake_head_img = pygame.image.load('head.png').convert_alpha()
    snake_head_img = pygame.transform.scale(snake_head_img, (cell_size, cell_size))
    snake_head_img_left = pygame.transform.rotate(snake_head_img, 270)
    snake_head_img_right = pygame.transform.rotate(snake_head_img, 90)
    snake_head_img_down = pygame.transform.rotate(snake_head_img, 180)
    snake_head_img_arr = [snake_head_img, snake_head_img_down,
                        snake_head_img_left, snake_head_img_right]
    snake_body_img = pygame.image.load('body.png').convert_alpha()
    snake_body_img = pygame.transform.scale(snake_body_img, (cell_size, cell_size))
    snake_body_img_left = pygame.transform.rotate(snake_body_img, 270)
    snake_body_img_right = pygame.transform.rotate(snake_body_img, 90)
    snake_body_img_down = pygame.transform.rotate(snake_body_img, 180)
    snake_body_img_arr = [snake_body_img, snake_body_img_down,
                        snake_body_img_left, snake_body_img_right]
    snake_tail_img = pygame.image.load('tail.png').convert_alpha()
    snake_tail_img = pygame.transform.scale(snake_tail_img, (cell_size, cell_size))
    snake_tail_img_left = pygame.transform.rotate(snake_tail_img, 270)
    snake_tail_img_right = pygame.transform.rotate(snake_tail_img, 90)
    snake_tail_img_down = pygame.transform.rotate(snake_tail_img, 180)
    snake_tail_img_arr = [snake_tail_img, snake_tail_img_down,
                        snake_tail_img_left, snake_tail_img_right]
    snake_body_corner = pygame.transform.scale(pygame.image.load(
        'body_corner.png').convert_alpha(), (cell_size, cell_size))
    snake_body_corner_arr = [snake_body_corner,
                            pygame.transform.rotate(snake_body_corner, 90), pygame.transform.rotate(snake_body_corner, 180), pygame.transform.rotate(snake_body_corner, 270)]
    def __init__(self) -> None:
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = v_left
        self.new_block = False
        self.last_mapped_dirction = 0

    def draw(self):
        for index, block in enumerate(self.body):
            rect = pygame.Rect(block.x * cell_size,
                               block.y * cell_size, cell_size, cell_size)
            # pygame.draw.rect(screen, pygame.Color('pink'), rect)
            direction = Vector2 
            if index == len(self.body) - 1:
                direction = self.body[index-1] - self.body[index]
            else:
                direction = self.body[index] - self.body[index + 1]
                
            mappedDirction = 0
            if direction == v_up:
                mappedDirction = 0
            elif direction == v_down:
                mappedDirction = 1
            elif direction == v_left:
                mappedDirction = 3
            elif direction == v_right:
                mappedDirction = 2
            else:
                #there's still something wrong if over-boundary
                mappedDirction = self.last_mapped_dirction

            if index == 0:
                screen.blit(self.snake_head_img_arr[mappedDirction],rect)
                self.last_mapped_dirction = mappedDirction
            elif index == len(self.body) - 1:
                screen.blit(self.snake_tail_img_arr[mappedDirction], rect)
                self.last_mapped_dirction = mappedDirction
            else:
                prev = self.body[index - 1] - self.body[index]
                next = self.body[index + 1] - self.body[index]
                if prev.x == next.x or prev.y == next.y:
                    screen.blit(self.snake_body_img_arr[mappedDirction], rect)
                else:
                    if prev.x == -1 and next.y == -1 or prev.y == -1 and next.x == -1:
                        screen.blit(self.snake_body_corner_arr[2], rect)
                    elif prev.x == -1 and next.y == 1 or prev.y == 1 and next.x == -1:
                        screen.blit(self.snake_body_corner_arr[3], rect)
                    elif prev.x == 1 and next.y == -1 or prev.y == -1 and next.x == 1:
                        screen.blit(self.snake_body_corner_arr[1], rect)
                    elif prev.x == 1 and next.y == 1 or prev.y == 1 and next.x == 1:
                        screen.blit(self.snake_body_corner_arr[0], rect)
                    else:
                        pass
                # screen.blit(snake_body_img_arr[mappedDirction], rect)
            

    def move(self):
        if self.new_block :
            body_copy = self.body[:]
            self.new_block = False
        else :
            body_copy = self.body[:-1]
        body_copy.insert(0,body_copy[0] + self.direction)
        self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True

class Fruit:
    mushroom = pygame.image.load('mushroom.png').convert_alpha()
    mushroom = pygame.transform.scale(mushroom, (cell_size, cell_size))
    def __init__(self) -> None:
        
        self.pos = Vector2(random.randint(0, cell_number - 1),
                           random.randint(0, cell_number - 1))

    def draw(self):
        rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        
        pygame.draw.rect(screen, pygame.Color('purple'), rect)
        screen.blit(self.mushroom, rect)
        

class Main:
    
    def __init__(self) -> None:
        self.snake = Snake()
        self.fruit = Fruit()
        self.grass_random = random.randint(2, int(cell_number/5))
        self.grass_img = pygame.transform.scale(pygame.image.load('grass.png').convert_alpha(), (cell_size, cell_size))
        self.bgm = pygame.mixer.Sound('bgm.wav')
        self.biteSound = pygame.mixer.Sound('bite.wav')
        self.game_over_sound = pygame.mixer.Sound('fail.wav')
        self.game_over_flag = False
        self.bgm.play(-1,0)

    def restart(self):
        self.game_over_flag = False
        self.snake = Snake()
        self.fruit = Fruit()
        self.bgm.play(-1, 0)
        
    def game_over(self) -> None:
        self.game_over_flag = True
        self.bgm.stop()
        self.game_over_sound.play()
        Timer(5.0, self.restart).start()
        

    def update(self) -> None:
        if self.game_over_flag == True:
            return
        self.snake.move()
        self.check_failure()
        self.check_boundary()
        self.check_fruit()

    def draw(self) -> None:
        self.draw_grass()
        self.snake.draw()
        self.fruit.draw()
        self.draw_hud()
    def check_fruit(self) -> None:
        if self.fruit.pos == self.snake.body[0]:
            self.fruit = Fruit()
            self.snake.add_block()
            self.biteSound.play()
    def check_failure(self) -> None:
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    def check_boundary(self) -> None:
        head = self.snake.body[0]
        if head.x > cell_number -1:
            head.x = 0
        elif head.x < 0:
            head.x = cell_number-1
        if head.y > cell_number -1:
            head.y = 0
        elif head.y < 0:
            head.y = cell_number-1
        # print(head)
    def draw_grass(self) -> None:
        for row in range(cell_number):
            for col in range(cell_number):
                grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                if (row + col) % self.grass_random == 0:
                    screen.blit(self.grass_img, grass_rect)
    def draw_hud(self):
        score_text = str(len(self.snake.body) - 3)
        score_label = font.render(score_text, True, pygame.Color('white'))
        score_label_rect = score_label.get_rect(bottomright=(
            cell_size * cell_number - 20, cell_size * cell_number - 20))
        score_icon_rect = self.fruit.mushroom.get_rect(midright = (score_label_rect.left - 4, score_label_rect.centery))
        score_bg_rect = pygame.Rect(0,0,20,20)
        score_bg_rect.top = min(score_icon_rect.top, score_label_rect.top)
        score_bg_rect.left = min(score_icon_rect.left, score_label_rect.left)
        score_bg_rect.width = score_label_rect.right - score_icon_rect.left + 4
        score_bg_rect.height = score_icon_rect.bottom - score_icon_rect.top
        
        pygame.draw.rect(screen, pygame.Color('darkgrey'), score_bg_rect)
        screen.blit(score_label, score_label_rect)
        screen.blit(self.fruit.mushroom, score_icon_rect)

clock = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
font = pygame.font.SysFont(None, 48)
main_game = Main()
pygame.time.set_timer(SCREEN_UPDATE, 200-len(main_game.snake.body)*10)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                main_game.snake.direction = v_up
            elif event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                main_game.snake.direction = v_down
            elif event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                main_game.snake.direction = v_left
            elif event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                main_game.snake.direction = v_right

    screen.fill(pygame.Color('sandybrown'))
    main_game.draw()
    pygame.display.update()
    clock.tick(60)
