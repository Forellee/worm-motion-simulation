import pygame
import math
import random

# Параметры экрана
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
worm_color = (247, 163, 163)  # Цвет тела червя
head_color = (255, 255, 255)  # Цвет головы червя (белый)
organ_color = (255, 0, 0)  # Цвет органов внутри червя

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симуляция движения червя")

# Параметры червя
SEGMENT_SIZE = 15
NUM_SEGMENTS = 50  # Увеличено количество сегментов для большей реалистичности
worm_segments = [(WIDTH // 2, HEIGHT // 2) for _ in range(NUM_SEGMENTS)]
angle = 0  # Начальный угол поворота
speed = 3  # Скорость движения
angle_change = 0  # Поворот направления

# Максимальный угол поворота
MAX_TURN_ANGLE = math.radians(5)  # 5 градусов для плавности

# Функция для сглаживания координат
def smooth_move(current, target, smoothing_factor=0.1):
    return current + (target - current) * smoothing_factor

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

        # Сглаживаем движение каждого сегмента
        worm_segments[i] = (
            smooth_move(curr_x, prev_x, 0.1),
            smooth_move(curr_y, prev_y, 0.1)
        )

    # Отрисовка червя с полым телом
    for i, segment in enumerate(worm_segments):
        # Отрисовка тела червя
        pygame.draw.circle(screen, worm_color, (int(segment[0]), int(segment[1])), SEGMENT_SIZE // 2)

        # Отрисовка органов внутри червя
        if i == 0:  # Организуем органы только в голове
            pygame.draw.circle(screen, organ_color, (int(segment[0]), int(segment[1])), SEGMENT_SIZE // 4)  # Орган в голове
        else:
            # Положение для органов в теле
            organ_x = segment[0] + random.uniform(-SEGMENT_SIZE // 8, SEGMENT_SIZE // 8)
            organ_y = segment[1] + random.uniform(-SEGMENT_SIZE // 8, SEGMENT_SIZE // 8)
            pygame.draw.circle(screen, organ_color, (int(organ_x), int(organ_y)), SEGMENT_SIZE // 4)  # Орган в теле

    # Отрисовка головы
    pygame.draw.circle(screen, head_color, (int(worm_segments[0][0]), int(worm_segments[0][1])), SEGMENT_SIZE // 2)

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
