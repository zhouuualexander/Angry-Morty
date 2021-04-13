import pygame
from pygame.locals import *
import time


class Morty:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.block = pygame.image.load(
            "resources/rickandmorty/morty.png").convert()
        self.block_x = 200
        self.block_y = 100
        self.direction = None

    def draw(self):
        self.parent_screen.fill((255, 255, 255))
        self.parent_screen.blit(self.block, (self.block_x, self.block_y))
        pygame.display.flip()

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):
        if self.direction == 'up':
            self.block_y -= 10
        if self.direction == 'down':
            self.block_y += 10
        if self.direction == 'left':
            self.block_x -= 10
        if self.direction == 'right':
            self.block_x += 10
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(size=(1000, 800))
        self.surface.fill((255, 255, 255))
        self.beginning = pygame.mixer.music.load(
            "resources/rickandmorty/rickandmorty_beginning.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.1)
        self.morty = Morty(self.surface)
        self.morty.draw()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RIGHT:
                        self.morty.move_right()
                    if event.key == K_LEFT:
                        self.morty.move_left()
                    if event.key == K_UP:
                        self.morty.move_up()
                    if event.key == K_DOWN:
                        self.morty.move_down()

                elif event.type == QUIT:
                    running = False
            self.morty.walk()
            time.sleep(0.2)


if __name__ == '__main__':
    game = Game()
    game.run()
