import pygame
import random
import sys


pygame.init()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

CELL_SIZE = 20
GRID_WIDTH = 32
GRID_HEIGHT = 24
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH  # 640
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT  # 480

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

FPS = 10

class GameObject:
    
    
    def __init__(self, position=None, body_color=None):
        if position is None:
            position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.position = position
        self.body_color = body_color
    
    def draw(self, surface):
       
        if self.body_color is None:
            return
        rect = pygame.Rect(
            self.position[0],
            self.position[1],
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)

class Apple(GameObject):
 
    
    def __init__(self):
        super().__init__()
        self.body_color = RED
        self.randomize_position()
    
    def randomize_position(self):
    
        random_x = random.randint(0, GRID_WIDTH - 1) * CELL_SIZE
        random_y = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
        self.position = (random_x, random_y)

class Snake(GameObject):
   
    
    def __init__(self):
        super().__init__()
        self.body_color = GREEN
        start_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [start_pos]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.length = 1
    
    def get_head_position(self):

        return self.positions[0]
    
    def update_direction(self):
       
        if self.next_direction:
            if (self.next_direction[0] * -1, self.next_direction[1] * -1) != self.direction:
                self.direction = self.next_direction
    
    def move(self):
    
        head_x, head_y = self.get_head_position()
        new_x = (head_x + self.direction[0] * CELL_SIZE) % SCREEN_WIDTH
        new_y = (head_y + self.direction[1] * CELL_SIZE) % SCREEN_HEIGHT
        new_position = (new_x, new_y)
        
        if new_position in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.positions.pop()
    
    def reset(self):
    
        start_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [start_pos]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = RIGHT
    
    def draw(self, surface):
      
        for position in self.positions:
            rect = pygame.Rect(position[0], position[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)

def handle_keys(snake):
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT

def main():
   
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Изгиб Питона')
    
    clock = pygame.time.Clock()
    
    snake = Snake()
    apple = Apple()
    
    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()
        
        screen.fill(BLACK)
        apple.draw(screen)
        snake.draw(screen)
        
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
