import pygame
import math
import random

# Параметры экрана
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
worm_color = (247, 163, 163)  # Цвет червя
head_color = (255, 255, 255)  # Цвет головы червя (белый)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симуляция движения червя")

# Параметры червя
SEGMENT_SIZE = 15
NUM_SEGMENTS = 20
worm_segments = [(WIDTH // 2, HEIGHT // 2) for _ in range(NUM_SEGMENTS)]
angle = 0  # Начальный угол поворота
speed = 3  # Скорость движения
angle_change = 0  # Поворот направления

# Максимальный угол поворота
MAX_TURN_ANGLE = math.radians(5)  # 5 градусов для плавности

running = True
while running:
    screen.fill(WHITE)

    # События Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Случайное изменение направления
    angle_change += random.uniform(-0.1, 0.1)  # Плавные изменения направления

    # Обновление позиции головы червя
    head_x, head_y = worm_segments[0]
    new_x = head_x + speed * math.cos(angle + angle_change)
    new_y = head_y + speed * math.sin(angle + angle_change)

    # Проверка на столкновение со стенами
    if new_x < SEGMENT_SIZE // 2:  # Столкновение с левой стеной
        new_x = SEGMENT_SIZE // 2
        angle_change += random.uniform(-math.pi / 2, math.pi / 2)  # Поворот в случайную сторону
    elif new_x > WIDTH - SEGMENT_SIZE // 2:  # Столкновение с правой стеной
        new_x = WIDTH - SEGMENT_SIZE // 2
        angle_change += random.uniform(-math.pi / 2, math.pi / 2)  # Поворот в случайную сторону

    if new_y < SEGMENT_SIZE // 2:  # Столкновение с верхней стеной
        new_y = SEGMENT_SIZE // 2
        angle_change += random.uniform(-math.pi / 2, math.pi / 2)  # Поворот в случайную сторону
    elif new_y > HEIGHT - SEGMENT_SIZE // 2:  # Столкновение с нижней стеной
        new_y = HEIGHT - SEGMENT_SIZE // 2
        angle_change += random.uniform(-math.pi / 2, math.pi / 2)  # Поворот в случайную сторону

    worm_segments[0] = (new_x, new_y)

    # Обновление позиции сегментов червя
    for i in range(1, NUM_SEGMENTS):
        prev_x, prev_y = worm_segments[i - 1]
        curr_x, curr_y = worm_segments[i]

        # Постепенное следование каждого сегмента за предыдущим
        dx = prev_x - curr_x
        dy = prev_y - curr_y
        distance = math.hypot(dx, dy)

        if distance > SEGMENT_SIZE:  # Двигаем сегмент ближе к предыдущему
            # Пропорциональное перемещение для плавного следования
            curr_x += (dx / distance) * (speed * 0.5)  # Меньшая скорость для плавности
            curr_y += (dy / distance) * (speed * 0.5)
            worm_segments[i] = (curr_x, curr_y)

    # Отрисовка червя
    for i, segment in enumerate(worm_segments):
        color = head_color if i == 0 else worm_color  # Задаем цвет для головы и тела
        pygame.draw.circle(screen, color, (int(segment[0]), int(segment[1])), SEGMENT_SIZE // 2)

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
