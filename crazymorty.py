import pygame
from pygame.locals import *
import time
import random
SIZE = 44


class Rick:
    """Object Rick
    """

    def __init__(self, parent_screen):
        """Initialize Object Rick and set the first position on the screen
        Args:
            parent_screen (surface): pygame surface(the screen)
        """
        # load image of Rick
        self.rick = pygame.image.load(
            "resources/rickandmorty/rick.png").convert()
        # Initialize parent_screen
        self.parent_screen = parent_screen
        # Set the position of Rick
        self.block_x = SIZE*3
        self.block_y = SIZE*3

    def move(self):
        """Move Rick to a random position when Morty ate a Rick
        """
        # Set the position of Rick randomly
        self.block_x = random.randint(0, 10)*SIZE
        self.block_y = random.randint(0, 10)*SIZE

    def draw(self):
        """Draw a Rick on the screen
        """
        # Set Rick on the screen with position
        self.parent_screen.blit(
            self.rick, (self.block_x, self.block_y))
        # Update the screen
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
        pygame.mixer.init()
        self.surface.fill((255, 255, 255))
        self.play_background_music()
        self.morty = Morty(self.surface, 1)
        self.morty.draw()
        self.rick = Rick(self.surface)
        self.rick.draw()
        
        try:
            self.f = open("best_score.txt", "r")
            self.best_score = int(self.f.read())
            self.f.close()
        except:
            self.f = open("best_score.txt", "w")
            self.f.write('0')
            self.best_score = 0
            self.f.close()


    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2+SIZE:
            if y1 >= y2 and y1 < y2+SIZE:
                return True
        return False

    def play_background_music(self):
        pygame.mixer.music.load(
            "resources/rickandmorty/rickandmorty_beginning.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.1)

    def play(self):
        if self.morty.length-1 > self.best_score:
                self.best_score = self.morty.length-1
                
        self.morty.walk()
        self.rick.draw()
        self.display_score()
        pygame.display.flip()
        # Morty killing Rick
        if self.is_collision(self.morty.block_x[0], self.morty.block_y[0], self.rick.block_x, self.rick.block_y):
            rick_sounds = str(random.randint(1, 13))
            self.play_rick_sound(rick_sounds)
            self.morty.increace_length()
            self.rick.move()
            
        # Morty killing himself
        for i in range(3, self.morty.length):
            if self.is_collision(self.morty.block_x[0], self.morty.block_y[0], self.morty.block_x[i], self.morty.block_y[i]):
                self.play_sound("LOSE")
                raise "game over"
        # Rick colliding with the boundries of the window
        if not (0 <= self.morty.block_x[0] <= 1500 and 0 <= self.morty.block_y[0] <= 1000):
            self.play_sound('LOSE')
            print("???")
            raise "Hit the boundry error"
    def pause(self):
        self.surface.fill((255, 255, 255))
        font = pygame.font.Font('resources/font/rick_and_morty.ttf',30)
        line1 = font.render(
            f"Pause for a second and press Enter to continue", True, (
                0, 0, 0))
        self.surface.blit(line1, (500, 400))
        
        pygame.display.flip()

        pygame.mixer.music.pause()

    def display_score(self):
        font = pygame.font.Font('resources/font/rick_and_morty.ttf',30)
        numberRicks = self.morty.length-1
        if numberRicks>1:
            score = font.render(
                f"Morty killed: {numberRicks} Ricks", True, (0, 0, 0))
            self.surface.blit(score, (1100, 20))
        score = font.render(
                f"Morty killed: {numberRicks} Rick", True, (0, 0, 0))
        self.surface.blit(score, (1100, 20))

        best = font.render(
                f"Best killed {self.best_score} ", True, (0,0,0)
        )
        self.surface.blit(best, (1100, 70))
        
        



    def play_rick_sound(self,sound):
        sound = pygame.mixer.Sound(f"resources/rick_sounds/{sound}.mp3")
        pygame.mixer.Sound.play(sound)
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/rickandmorty/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def show_game_over(self):
        if self.morty.length-1 > self.best_score:
            self.best_score = self.morty.length-1
        f = open("best_score.txt", "w")
        f.write(str(self.best_score))
        f.close()

        self.surface.fill((255, 255, 255))
        font = pygame.font.Font('resources/font/rick_and_morty.ttf',30)
        line1 = font.render(
            f"Wubba Lubba Dub-Dub!!! You just killed {self.morty.length-1} Rick", True, (
                0, 0, 0))
        self.surface.blit(line1, (500, 400))
        line2 = font.render(
            "To kill Rick again press Enter. To give up press Escape!", True, (
                0, 0, 0)
        )
        self.surface.blit(line2, (450, 450))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.morty = Morty(self.surface, 1)
        self.rick = Rick(self.surface)

    def run(self):
        
        # print(self.f.read())
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.pause()
                        self.play_sound("PAUSE")
                        pause = True
                    if event.key == K_ESCAPE:
                        self.play_sound("GIVEUP")
                        time.sleep(5)
                        running = False
                    if event.key == K_RETURN:
                        self.play_sound("KILL")
                        time.sleep(2)
                        pygame.mixer.music.unpause()
                        pause = False
                    if event.key == K_RIGHT or event.key == K_d:
                        self.morty.move_right()
                    if event.key == K_LEFT or event.key == K_a:
                        self.morty.move_left()
                    if event.key == K_UP or event.key == K_w:
                        self.morty.move_up()
                    if event.key == K_DOWN or event.key == K_s:
                        self.morty.move_down()

                elif event.type == QUIT:
                    self.play_sound("QUIT")
                    time.sleep(4)
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                time.sleep(5)
                self.play_sound("GAMEOVER")
                pause = True
                self.reset()
            time.sleep(0.3)


if __name__ == '__main__':
    game = Game()
    game.run()
