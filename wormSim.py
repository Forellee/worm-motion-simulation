import pygame
import math
import random

# Параметры экрана
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)


# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симуляция движения червя")

# Параметры червя
SEGMENT_SIZE = 15
NUM_SEGMENTS = 20
worm_segments = [(WIDTH // 2, HEIGHT // 2) for _ in range(NUM_SEGMENTS)]
angle = 0  # Начальный угол поворота
speed = 2  # Скорость движения
angle_change = 0  # Поворот направления


# Функция для случайного поворота
def random_turn():
    return random.uniform(-0.2, 0.2)  # Случайный угол поворота


running = True
while running:
    screen.fill(WHITE)

    # События Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Случайное изменение направления
    angle_change += random_turn()

    # Обновление позиции головы червя
    x, y = worm_segments[0]
    new_x = x + speed * math.cos(angle + angle_change)
    new_y = y + speed * math.sin(angle + angle_change)

    # Проверка на столкновение со стенами
    if new_x < SEGMENT_SIZE // 2 or new_x > WIDTH - SEGMENT_SIZE // 2:
        angle_change = -angle_change + random_turn()  # Изменение направления на противоположное
        new_x = x  # Оставляем червя на текущей позиции
    if new_y < SEGMENT_SIZE // 2 or new_y > HEIGHT - SEGMENT_SIZE // 2:
        angle_change = -angle_change + random_turn()
        new_y = y

    worm_segments[0] = (new_x, new_y)

    # Обновление позиции сегментов червя
    for i in range(1, NUM_SEGMENTS):
        prev_x, prev_y = worm_segments[i - 1]
        curr_x, curr_y = worm_segments[i]

        # Постепенное следование каждого сегмента за предыдущим
        dx = prev_x - curr_x
        dy = prev_y - curr_y
        distance = math.hypot(dx, dy)
        if distance > SEGMENT_SIZE:
            curr_x += (dx / distance) * speed
            curr_y += (dy / distance) * speed
            worm_segments[i] = (curr_x, curr_y)

    # Отрисовка червя
    for segment in worm_segments:
        pygame.draw.circle(screen, worm_color, (int(segment[0]), int(segment[1])), SEGMENT_SIZE // 2)

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
