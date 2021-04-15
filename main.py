import pygame
from pygame.locals import *
import time
import random
SIZE = 44


class Rick:
    def __init__(self, parent_screen):
        self.rick = pygame.image.load(
            "resources/rickandmorty/rick.png").convert()
        self.parent_screen = parent_screen
        self.block_x = SIZE*3
        self.block_y = SIZE*3

    def move(self):
        self.block_x = random.randint(0, 10)*SIZE
        self.block_y = random.randint(0, 10)*SIZE

    def draw(self):
        self.parent_screen.blit(
            self.rick, (self.block_x, self.block_y))
        pygame.display.flip()


class Morty:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load(
            "resources/rickandmorty/morty.png").convert()
        self.block_x = [SIZE]*length
        self.block_y = [SIZE]*length
        self.direction = 'down'

    def increace_length(self):
        self.length += 1
        self.block_x.append(-1)
        self.block_y.append(-1)

    def draw(self):
        self.parent_screen.fill((255, 255, 255))
        for i in range(self.length):
            self.parent_screen.blit(
                self.block, (self.block_x[i], self.block_y[i]))
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
        for i in range(self.length-1, 0, -1):
            self.block_x[i] = self.block_x[i-1]
            self.block_y[i] = self.block_y[i-1]
        if self.direction == 'up':
            self.block_y[0] -= SIZE
        if self.direction == 'down':
            self.block_y[0] += SIZE
        if self.direction == 'left':
            self.block_x[0] -= SIZE
        if self.direction == 'right':
            self.block_x[0] += SIZE
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Crazy Morty')
        self.surface = pygame.display.set_mode(size=(1500, 1000))
        self.surface.fill((255, 255, 255))
        self.beginning = pygame.mixer.music.load(
            "resources/rickandmorty/rickandmorty_beginning.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.1)
        self.morty = Morty(self.surface, 1)
        self.morty.draw()
        self.rick = Rick(self.surface)
        self.rick.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2+SIZE:
            if y1 >= y2 and y1 < y2+SIZE:
                return True
        return False

    def play(self):
        self.morty.walk()
        self.rick.draw()
        self.display_score()
        pygame.display.flip()
        if self.is_collision(self.morty.block_x[0], self.morty.block_y[0], self.rick.block_x, self.rick.block_y):
            self.morty.increace_length()
            self.rick.move()

    def display_score(self):
        font = pygame.font.SysFont('Get Schwifty', 30)
        score = font.render(
            f"Score: {self.morty.length}", True, (0, 0, 0))
        self.surface.blit(score, (1300, 20))

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
            self.play()
            time.sleep(0.3)


if __name__ == '__main__':
    game = Game()
    game.run()
