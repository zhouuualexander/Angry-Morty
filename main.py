import pygame
from pygame.locals import *


def draw_block():
    surface.fill((255, 255, 255))
    surface.blit(block, (block_x, block_y))
    pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    surface = pygame.display.set_mode(size=(1000, 800))
    surface.fill((255, 255, 255))
    beginning = pygame.mixer.music.load(
        "resources/rickandmorty/rickandmorty_beginning.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.1)
    block = pygame.image.load("resources/rickandmorty/morty.png").convert()
    block_x = 200
    block_y = 100
    surface.blit(block, (block_x, block_y))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_RIGHT:
                    block_x += 10
                    draw_block()
                if event.key == K_LEFT:
                    block_x -= 10
                    draw_block()
                if event.key == K_UP:
                    block_y -= 10
                    draw_block()
                if event.key == K_DOWN:
                    block_y += 10
                    draw_block()

            elif event.type == QUIT:
                running = False
