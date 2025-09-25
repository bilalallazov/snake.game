import random
import pygame
import sys


# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 120, 255)

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()


def draw_grid():
    """Отрисовка сетки игрового поля."""
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))


class Snake:
    """Класс для представления змейки."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Сброс состояния змейки к начальному."""
        self.length = 1  # Исправлено: начинаем с длины 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.score = 0
        self.grow_pending = 2  # Расти на 2 сегмента в начале
    
    def get_head_position(self):
        """Получить позицию головы змейки."""
        return self.positions[0]
    
    def turn(self, point):
        """Изменение направления движения змейки."""
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        self.direction = point
    
    def move(self):
        """Движение змейки."""
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # Проверка столкновения с собой
        if new_position in self.positions[1:]:
            return False  # Игра окончена
        
        self.positions.insert(0, new_position)
        
        if self.grow_pending > 0:
            self.grow_pending -= 1
            self.length += 1
        else:
            self.positions.pop()
        
        return True
    
    def grow(self):
        """Увеличение длины змейки."""
        self.grow_pending += 1
        self.score += 10
    
    def draw(self, surface):
        """Отрисовка змейки."""
        for i, p in enumerate(self.positions):
            color = GREEN if i == 0 else BLUE  # Голова зеленого цвета, тело синего
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), 
                              (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (30, 30, 30), rect, 1)


class Food:
    """Класс для представления еды."""
    
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
    
    def randomize_position(self):
        """Случайное размещение еды на поле."""
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                         random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, surface):
        """Отрисовка еды."""
        rect = pygame.Rect((self.position[0] * GRID_SIZE, 
                           self.position[1] * GRID_SIZE), 
                          (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, (30, 30, 30), rect, 1)


def show_game_over(surface, score):
    """Отображение экрана завершения игры."""
    font = pygame.font.SysFont('Arial', 36)
    text = font.render(f'Игра окончена! Счет: {score}', True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    
    font_small = pygame.font.SysFont('Arial', 24)
    restart_text = font_small.render('Нажмите R для перезапуска', True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    
    surface.blit(text, text_rect)
    surface.blit(restart_text, restart_rect)


def main():

    snake = Snake()
    food = Food()
    game_over = False
    
    # Убедимся, что еда не появляется на змейке при старте
    while food.position in snake.positions:
        food.randomize_position()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    snake.reset()
                    food.randomize_position()
                    # Убедимся, что еда не появляется на змейке после рестарта
                    while food.position in snake.positions:
                        food.randomize_position()
                    game_over = False
                elif not game_over:
                    if event.key == pygame.K_UP:
                        snake.turn((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.turn((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.turn((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.turn((1, 0))
        
        if not game_over:
            # Движение змейки
            if not snake.move():
                game_over = True
            
            # Проверка съедания еды
            if snake.get_head_position() == food.position:
                snake.grow()
                food.randomize_position()
                # Убедимся, что еда не появляется на змейке
                while food.position in snake.positions:
                    food.randomize_position()
        
        # Отрисовка
        screen.fill(BLACK)
        draw_grid()
        snake.draw(screen)
        food.draw(screen)
        
        # Отображение счета
        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f'Счет: {snake.score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        if game_over:
            show_game_over(screen, snake.score)
        
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
