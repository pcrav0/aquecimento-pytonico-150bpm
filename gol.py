import copy
import math
import os
from time import sleep

import pygame

blocks = 80
grid = [[False for x in range(blocks)] for y in range(blocks)]
# grid = []
# for y in range(blocks):
#     grid.append([])
#     for x in range(blocks):
#         grid[y].append(False)


# pygame setup
pygame.init()
clock = pygame.time.Clock()

width_factor = 16
height_factor = 9

screen = pygame.display.set_mode((blocks*width_factor, blocks*height_factor))

width = screen.get_width()
height = screen.get_height()

running = True
pause = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_w:
                pause = not pause
            elif event.key == pygame.K_e:
                breakpoint()

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            pos = math.floor(pos[0] / width_factor), math.floor(pos[1] / height_factor)
            grid[pos[1]][pos[0]] = not grid[pos[1]][pos[0]]

    screen.fill('black')

    for y in range(blocks):
        for x in range(blocks):
            pos_xa = x*width_factor
            pos_ya = y*height_factor

            pos_xb = (x + 1)*width_factor
            pos_yb = (y + 1)*height_factor

            if grid[y][x]:
                pygame.draw.rect(
                    screen,
                    'red',
                    pygame.Rect(pos_xa, pos_ya, pos_xb, pos_yb)
                )
            else:
                pygame.draw.rect(
                    screen,
                    'black',
                    pygame.Rect(pos_xa, pos_ya, pos_xb, pos_yb)
                )

            # pygame.draw.line(
            #     screen,
            #     'grey',
            #     (pos_xa, pos_ya),
            #     (pos_xb, pos_ya),
            # )
            # pygame.draw.line(
            #     screen,
            #     'grey',
            #     (pos_xa, pos_ya),
            #     (pos_xa, pos_yb),
            # )

    # update
    if not pause:
        back_grid = copy.deepcopy(grid)

        for y in range(blocks):
            for x in range(blocks):
                alive_count = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx == 0 and dy == 0:
                            continue
                        cell = grid[(y+dy) % blocks][(x+dx) % blocks]
                        if cell:
                            alive_count += 1

                if grid[y][x]:
                    if alive_count < 2:
                        back_grid[y][x] = False
                    elif alive_count == 2 or alive_count == 3:
                        back_grid[y][x] = True
                    elif alive_count > 3:
                        back_grid[y][x] = False
                elif alive_count == 3:
                        back_grid[y][x] = True

        grid = back_grid

    pygame.display.flip()

    clock.tick(60)
    sleep(0.1)

pygame.quit()
