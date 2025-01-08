import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_WIDTH = 50
PIPE_GAP = 160

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Класс для птицы
class Bird:
    def __init__(self):
        bird_image = pygame.image.load("C:/Users/Пользователь/Desktop/fb/bird.png")
        self.bird_image = pygame.transform.scale(bird_image, (60, 40))
        self.x = 50
        self.y = HEIGHT // 2
        self.width = 40
        self.height = 40
        self.velocity = 0
        self.angle = 0

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def get_angle(self):
        # Сглаживающий коэффициент для плавного изменения угла
        smoothing_factor = 0.08  # Чем меньше значение, тем плавнее изменение угла

        # Вычисление угла касательной на основе вертикальной скорости
        if self.velocity == 0:
            target_angle = 0  # Если вертикальная скорость нулевая, угол горизонтальный
        else:
            target_angle = math.degrees(math.atan(self.velocity / 1))  # Угол относительно горизонтали

        # Плавное сглаживание угла
        self.angle = self.angle * (1 - smoothing_factor) + target_angle * smoothing_factor
        self.angle = max(min(self.angle, 30), -30)

        return self.angle

    def draw(self):
        self.get_angle()
        rotated_bird = pygame.transform.rotate(self.bird_image, -self.angle)

        # Получаем прямоугольник, который описывает изображение с учётом поворота
        bird_rect = rotated_bird.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))

        # Отображаем птицу с учётом поворота
        screen.blit(rotated_bird, bird_rect.topleft)
        # pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

# Класс для труб
class Pipe:
    def __init__(self):
        pipe_image = pygame.image.load("pipe1.png")  # Замените на путь к вашему изображению
        self.pipe_image = pygame.transform.scale(pipe_image, (60, 400))
        self.x = WIDTH
        self.height = random.randint(100, HEIGHT - PIPE_GAP - 100)
        self.top = self.height
        self.bottom = self.height + PIPE_GAP
        self.width = PIPE_WIDTH
        self.passed = False

    def move(self):
        self.x -= 5

    def draw(self):
        flipped_pipe = pygame.transform.flip(self.pipe_image, False, True)  # Переворачиваем по вертикали
        screen.blit(flipped_pipe, (self.x, self.bottom - HEIGHT + 40))
        # pygame.draw.rect(screen, BLUE, (self.x, 0, self.width, self.top))
        screen.blit(self.pipe_image, (self.x, self.bottom))
        screen.blit(self.pipe_image, (self.x, self.bottom))
        # pygame.draw.rect(screen, BLUE, (self.x, self.bottom, self.width, HEIGHT - self.bottom))

# Функция для проверки столкновений
def check_collisions(bird, pipes):
    if bird.y > 525:
        return True
    for pipe in pipes:
        if pipe.x < bird.x + bird.width and pipe.x + pipe.width > bird.x:
            if bird.y < pipe.top or bird.y + bird.height > pipe.bottom:
                return True
    return False



# Основная функция игры
def main():
    bird = Bird()
    pipes = []
    clock = pygame.time.Clock()
    score_moment = 0, False
    score = 0
    record = 0
    running = True
    pause = True
    background = pygame.image.load("background.png")
    ground = pygame.image.load("ground.png")
    font = pygame.font.SysFont("Comic Sans", 24)




    while running:
        clock.tick(FPS)
        screen.fill(WHITE)
        screen.blit(background, (-2, -2))

        if not pause:

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.jump()
                    if event.key == pygame.K_p:
                        pause = True
                        score_moment = score, True


            # Перемещение птицы
            bird.move()

            # Генерация и перемещение труб
            if len(pipes) == 0 or pipes[-1].x < WIDTH - 280:
                pipes.append(Pipe())

            for pipe in pipes[:]:
                pipe.move()
                if pipe.x + pipe.width < 0:
                    pipes.remove(pipe)
                if not pipe.passed and pipe.x + pipe.width < bird.x:
                    pipe.passed = True
                    score += 1
                pipe.draw()

            # Проверка на столкновение
            if check_collisions(bird, pipes):
                pause = True
                score_moment = score, True
                bird = Bird()
                pipes = []
                score = 0


            # Отображение птицы и счета
            # print(bird.get_angle())
            bird.draw()
            # pygame.draw.rect(screen, WHITE, (10, 10, 50, 30))
            # font = pygame.font.SysFont("HarryPotterKudos Light", 24)
            text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(text, (20, 10))

            if record < score:
                record = score
            text = font.render(f"Record: {record}", True, BLACK)
            screen.blit(text, (20, 32))
            screen.blit(ground, (-2, 525))

            # Обновление экрана
            pygame.display.flip()

        else:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                        pause = False
                        score_moment = 0, True


            # Отображение птицы и счета
            bird.draw()
            for pipe in pipes[:]:
                pipe.draw()

            # font = pygame.font.SysFont("HarryPotterKudos Light", 24)
            text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(text, (20, 10))

            text = font.render(f"Record: {record}", True, BLACK)
            screen.blit(text, (20, 32))

            if score_moment[1]:
                text = font.render(f"Last score: {score_moment[0]}", True, BLACK)
                screen.blit(text, (20, 54))

            text = font.render("press SPACE or p", True, BLACK)
            screen.blit(text, (100, 200))
            text = font.render("to start game", True, BLACK)
            screen.blit(text, (120, 220))

            screen.blit(ground, (-2, 525))

            # Обновление экрана
            pygame.display.flip()

    # Завершение игры
    pygame.quit()

# Запуск игры
if __name__ == "__main__":
    main()
