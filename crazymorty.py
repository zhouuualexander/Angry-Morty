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
        self.block_x = random.randint(3, 24)*SIZE+10
        self.block_y = random.randint(3, 17)*SIZE+10

    def move(self):
        """Move Rick to a random position when Morty ate a Rick
        """
        # Set the position of Rick randomly
        self.block_x = random.randint(3, 24)*SIZE+10
        self.block_y = random.randint(3, 17)*SIZE+10
        # self.block_x = 1066
        # self.block_y = 758
        return self.block_x, self.block_y

    def draw(self):
        """Draw a Rick on the screen
        """
        # Set Rick on the screen with position
        self.parent_screen.blit(
            self.rick, (self.block_x, self.block_y))
        # Update the screen
        # pygame.display.flip()


class Morty:
    def __init__(self, parent_screen, length):
        
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load(
            "resources/rickandmorty/morty.png").convert()
        self.block_x = [10*SIZE+10]*length
        self.block_y = [9*SIZE+10]*length

        self.direction = 'down'
        self.right = True
        self.left = True
        self.up = True
        self.down = True

    def increace_length(self):
        self.length += 1
        self.block_x.append(-1)
        self.block_y.append(-1)

    def draw(self):
        self.parent_screen.fill((255, 255, 255))
        pygame.draw.rect(self.parent_screen,(0,0,0),(0,132,1120,812),10)
       
        

        for i in range(self.length):
            self.parent_screen.blit(
                self.block, (self.block_x[i], self.block_y[i]))
        # pygame.display.flip()

    def move_up(self):
        self.direction = 'up'
        
        if self.length>1:
            self.right = True
            self.left = True
            self.up = True
            self.down = False
        


    def move_down(self):
        self.direction = 'down'
        
        if self.length>1:
            self.right = True
            self.left = True
            self.up = False
            self.down = True
        

    def move_left(self):
        self.direction = 'left'
        
        if self.length>1:
            self.right = False
            self.left = True
            self.up = True
            self.down = True
       

    def move_right(self):
        self.direction = 'right'
        
        if self.length>1:
            self.right = True
            self.left = False
            self.up = True
            self.down = True
        

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.block_x[i] = self.block_x[i-1]
            self.block_y[i] = self.block_y[i-1]
        if self.direction == 'up':
            if self.length>1:
                self.down = False
            self.block_y[0] -= SIZE
        if self.direction == 'down':
            if self.length>1:
                self.up = False
            self.block_y[0] += SIZE
        if self.direction == 'left':
            if self.length>1:
                self.right = False
            self.block_x[0] -= SIZE
        if self.direction == 'right':
            if self.length>1:
                self.left = False
            self.block_x[0] += SIZE
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Crazy Morty')
        self.surface = pygame.display.set_mode(size=(1120, 812))
        pygame.mixer.init()
        self.speed_level = 1
        self.speed = 0.3
        self.firstpageImg = pygame.image.load("resources/img/Startpage.jpeg")
        
        self.surface.fill((255, 255, 255))
        self.play_background_music()
        self.morty = Morty(self.surface, 1)
        self.morty.draw()
        self.rick = Rick(self.surface)
        self.rick.draw()
        self.zen_mode = False
        
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

    def play_game_music(self):
        pygame.mixer.music.load(
            "resources/rickandmorty/rickandmorty.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(1)
    def play_background_music(self):
        pygame.mixer.music.load(
            "resources/rickandmorty/rickandmorty_beginning.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.5)

    def play(self):
        
        if self.morty.length-1 > self.best_score:
            self.best_score = self.morty.length-1
        self.morty.walk()
        self.rick.draw()
        self.display_speed()
        self.display_score()
        self.display_title() 
        pygame.display.flip()
        # Morty killing Rick
        if self.is_collision(self.morty.block_x[0], self.morty.block_y[0], self.rick.block_x, self.rick.block_y):
            count = 0
            rick_sounds = str(random.randint(1, 13))
            self.play_rick_sound(rick_sounds)
            self.morty.increace_length()
            x,y = self.rick.move()
            occupied = True
            #Check whether Rick's new position is conflit with Mortys,if yes, randomly generate a new position for Rick until no conflit happen.
            while occupied:
                for i in range(0, self.morty.length):
                    if self.is_collision(x, y, self.morty.block_x[i], self.morty.block_y[i]):
                        x,y = self.rick.move()
                        occupied = True
                        count = 1
                if count == 0:
                    occupied = False
                count = 0
                


            
        # Morty killing himself
        for i in range(3, self.morty.length):
            if self.is_collision(self.morty.block_x[0], self.morty.block_y[0], self.morty.block_x[i], self.morty.block_y[i]):
                self.play_sound("LOSE")
                raise "game over"
        # Rick colliding with the boundries of the window
        if not (0 <= self.morty.block_x[0] <= 1100 and 142 <= self.morty.block_y[0] <= 768):
            self.play_sound('LOSE')
            raise "Hit the boundry error"
    def pause(self):
        self.speed = 0.3
        self.speed_level = 1
        self.surface.fill((255, 255, 255))
        font = pygame.font.Font('resources/font/rick_and_morty.ttf',30)
        line1 = font.render(
            f"Pause for a second and press Enter to continue", True, (
                0, 0, 0))
        self.surface.blit(line1, (300, 350))
        
        pygame.display.flip()

        pygame.mixer.music.pause()
    def display_title(self):
        if not self.zen_mode:
            font = pygame.font.Font('resources/font/get_schwifty.ttf',50)
            title = font.render(
                    "Crazy  Morty", True, (0,0,0)
            )
        if self.zen_mode:
            font = pygame.font.Font('resources/font/get_schwifty.ttf',50)
            title = font.render(
                    "Zen  Mode", True, (0,0,0)
            )
        self.surface.blit(title, (120, 30))
    def display_speed(self):
        
        if self.zen_mode:
            font = pygame.font.Font('resources/font/rick_and_morty.ttf',30)
            speed_up = font.render(
                    "To speed up Press F", True, (0,0,0)
            )
            self.surface.blit(speed_up, (500, 30))
            speed_down = font.render(
                    "To slow down Press S", True, (0,0,0)
            )
            self.surface.blit(speed_down, (500, 80))
            show_speed = font.render(
                    f"Speed: {self.speed_level}", True, (0,0,0)
            )
            self.surface.blit(show_speed, (550, 55))




    def display_score(self):
        font = pygame.font.Font('resources/font/rick_and_morty.ttf',30)
        numberRicks = self.morty.length-1
        if numberRicks>1:
            score = font.render(
                f"Morty killed: {numberRicks} Ricks", True, (0, 0, 0))
            self.surface.blit(score, (800, 30))
        score = font.render(
                f"Morty killed: {numberRicks} Rick", True, (0, 0, 0))
        self.surface.blit(score, (800, 30))

        best = font.render(
                f"Best killed {self.best_score} ", True, (0,0,0)
        )
        self.surface.blit(best, (800, 80))
        
        



    def play_rick_sound(self,sound):
        sound = pygame.mixer.Sound(f"resources/rick_sounds/{sound}.mp3")
        pygame.mixer.Sound.play(sound)
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/rickandmorty/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def show_game_over(self):
        self.speed = 0.3
        self.speed_level = 1
        if self.morty.length-1 > self.best_score:
            self.best_score = self.morty.length-1
        f = open("best_score.txt", "w")
        f.write(str(self.best_score))
        f.close()

        self.surface.fill((0, 0, 0))
        font = pygame.font.Font('resources/font/rick_and_morty.ttf',30)
        line1 = font.render(
            f"Wubba Lubba Dub-Dub!!! You just killed {self.morty.length-1} Rick", True, (
                255, 255, 255))
        self.surface.blit(line1, (350, 350))
        line2 = font.render(
            "To kill Rick again press Enter. To give up press Escape!", True, (
                255, 255, 255)
        )
        self.surface.blit(line2, (300, 400))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.zen_mode = False
        self.morty = Morty(self.surface, 1)
        self.rick = Rick(self.surface)
        self.speed_level = 1
        self.speed = 0.3
    def startpage(self):
        self.play_background_music()
        self.surface.blit(self.firstpageImg, (0,0))
        prompt_font = pygame.font.Font('resources/font/rick_and_morty.ttf',30)
        prompt1 = prompt_font.render(
            "To start killing Rick, press Enter", True, (
                255, 255, 255))
        self.surface.blit(prompt1, (425, 250))
        prompt2 = prompt_font.render(
            "To end the game, press Escape", True, (
                255, 255, 255))
        self.surface.blit(prompt2, (425, 300))
        zen = prompt_font.render(
            "Zen Mode, press Z", True, (255,255,255)
        )
        self.surface.blit(zen, (100, 500))
        title_font = pygame.font.Font('resources/font/get_schwifty.ttf',50)
        title = title_font.render("Crazy Morty", True, (225,225,225))
        self.surface.blit(title, (450,100))
        pygame.display.flip()
        start = True
        while start:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            self.reset()
                            self.play_sound("KILL")
                            return True
                        if event.key == K_z:
                            self.reset()
                            self.zen_mode = True
                            
                            self.play_sound("KILL")
                            return True
                        if event.key == K_ESCAPE:
                            self.play_sound("QUIT")
                            time.sleep(1.2)
                            return False
                elif event.type == QUIT:
                    self.play_sound("QUIT")
                    time.sleep(1.2)
                    return False

    def run(self,running):
        self.play_game_music()

        # running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if self.zen_mode:
                        if event.key == K_f:
                            if self.speed >0.1:
                                self.speed -=0.01
                                self.speed_level += 1
                        if event.key == K_s:
                            if self.speed< 0.3:
                                self.speed += 0.01
                                self.speed_level -= 1
                    if event.key == K_SPACE:
                        self.pause()
                        self.play_sound("PAUSE")
                        pause = True
                    if event.key == K_ESCAPE:
                        self.play_sound("GIVEUP")
                        
                        running = False
                    if event.key == K_RETURN:
                        self.speed = 0.3
                        self.speed_level = 1
                        self.play_sound("KILL")
                        time.sleep(2)
                        pygame.mixer.music.unpause()
                        pause = False
                    if event.key == K_RIGHT:
                        if self.morty.right:
                            self.morty.move_right()
                    if event.key == K_LEFT:
                        if self.morty.left:
                            self.morty.move_left()
                    if event.key == K_UP:
                        if self.morty.up:
                            self.morty.move_up()
                    if event.key == K_DOWN:
                        if self.morty.down:
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
                if self.zen_mode == True:
                    self.reset()
                    self.zen_mode = True
                if self.zen_mode == False:
                    self.reset()
            time.sleep(self.speed)


if __name__ == '__main__':
    game = Game()
    running = game.startpage()
    while running:
        game.run(running)
        running = game.startpage()
