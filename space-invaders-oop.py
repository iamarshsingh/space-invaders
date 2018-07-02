#Importing required modules
import pygame
import random
import time
import threading

#Defining RGB values for colours
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
TITLE_WHITE = ( 255, 200, 255)
LIGHT_GREEN = (0, 180, 0)
GREEN = (78, 255, 87)
YELLOW = (241, 255, 0)
BLUE = (80, 255, 239)
PURPLE = (203, 0, 255)
RED = (237, 28, 36)

timer = 0

# adding font file
FONT = "fonts/space_invaders.ttf"

#List to store enemy ships
ships = [
    [1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1]
]

class Ship(pygame.sprite.Sprite):
    """
    Defining the defender spaceship and its
    properties
    """

    # defines the initial x and y pos of our ship
    def __init__(self, x_pos, y_pos):
        super().__init__()

        #self.enemy1 = pygame.image.load("./images/enemy3_1.png").convert_alpha()
        #self.enemy1 = pygame.transform.scale(self.enemy1 , (40, 40))
        #self.screen.blit(self.enemy1, (300, 250))

        self.image = pygame.image.load("./images/ship.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = (x_pos, y_pos))
        #self.screen.blit(self.image, (x_pos, y_pos))
        self.moving_speed = 1
        self.bullet_group = pygame.sprite.Group()

    def update(self, screen, keystate):
        # Right Key
        if keystate[pygame.K_RIGHT]:
            if self.rect.x < 730:
                self.rect.x += self.moving_speed

        # Left Key
        if keystate[pygame.K_LEFT]:
            if self.rect.x > 20:
                self.rect.x -= self.moving_speed

        # Shoot Key
        if (keystate[pygame.K_SPACE] or keystate[pygame.K_w]) and (len(self.bullet_group.sprites()) == 0):
            self.shoot()

        self.draw(screen)

    def draw(self, screen):
        #Drawing the ship
        game.screen.blit(self.image, self.rect)
        grplen = len(self.bullet_group.sprites())
        if grplen:
            self.player_bullet.update()
            self.player_bullet.draw()

    def shoot(self):
        self.player_bullet = Bullet((self.rect.x + 25), self.rect.y, ofPlayer=True)
        self.bullet_group.add(self.player_bullet)
        #shoot_sound.play()

class Bullet(pygame.sprite.Sprite):
    """
    describing bullets; thinking to keep missils
    type same for everythnig - all alien ships and
    defender
    """
    def __init__(self, x_pos, y_pos, ofPlayer):

        super().__init__()

        if ofPlayer is True:
            self.image = pygame.image.load("./images/laser.png").convert_alpha()
            self.rect = self.image.get_rect(topleft=(x_pos, y_pos))
            self.velocity = -7
        else:
            self.image = pygame.image.load("./images/ship.png").convert_alpha()
            self.rect = self.image.get_rect(topleft=(x_pos, y_pos))
            self.velocity = 7

    def update(self):
        self.rect.y += self.velocity
        if self.rect.y < 25:
            self.kill()
        self.draw()

    def draw(self):
        game.screen.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    """
    class for alien spaceship and their
    properties. We need to create a list of
    lists of objects of this class Aliens probably.
    """

    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_H = 15
        self.speed_V = 12

    def update(self):
        game.timer_1 += game.elapsed_time
        game.timer_2 += game.elapsed_time
        game.timer_3 += game.elapsed_time

        for alien in game.All_Aliens:
            if alien.rect.y >= 415:
                pygame.quit()

        if game.timer_2 > 10750:
            self.speed_H = -(self.speed_H)
            for alien in game.All_Aliens:
                alien.rect.y += self.speed_V
                alien.draw()
            game.timer_2 -= 10750
            game.timer_1 -= 1500  ## To give a pause
            game.start_time = time.time()

        else:
            if game.timer_1 >= 750:
                for alien in game.All_Aliens:
                    alien.rect.x += self.speed_H
                    alien.draw()
                game.timer_1 -= 750
                game.start_time = time.time()

            else:
                for alien in game.All_Aliens:
                    alien.draw()

    def shoot(self):
        # not all ships will shoot at once, we need to randomly select some of them
        # and call the Missile.shoot function or something to make them shoot
        pass

    def draw(self):
        game.screen.blit(self.image, self.rect)

class Blocker(pygame.sprite.Sprite):
    """
    Class for defining blocks and their properties;
    basically their damage rate.
    """
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def draw(self):
        # pygame.draw.rect(screen, WHITE, [self.x, self.y, 125,  60])

        # instead of making it single rectangle, distributed each
        # rectangle into 25 smaller rectangles. Thought this may
        # help in collision detection and we can delete smaller rectangles
        # when a missile hits it.
        for i in range(5):
            for j in range(5):
                x_pos = self.x + 25*j
                y_pos = self.y + 12*i
                pygame.draw.rect(game.screen, WHITE, [x_pos, y_pos, 25, 12])

    def damage(self):
        pass


class Mystery(object):
    def __init__(self):
        pass

    #Other methods for displaying, updating and images


class Explosion(object):
    def __init__(self):
        pass

    #Other methods for displaying, updating and images

class Life(object):
    def __init__(self):
        pass

    #Other methods for displaying, updating and images

class SpaceInvaders(object):
    def __init__(self):
        #Initialize pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.timer = 0
        self.timer_2 = 0

        #Initial Game sound in infinite loop
        pygame.mixer.music.load('./sounds/Title_Screen.wav')
        pygame.mixer.music.play(-1)

        #Load screen and caption
        #Initialzing a screen for display
        self.screen = pygame.display.set_mode((800,600))
        #Setting Caption of the game
        pygame.display.set_caption('Space Invaders')

        #Initialzing variables
        self.current_score = 0
        self.lives = 3
        self.current_player = 1
        self.draw_state = 0
        #other variables will also be required

        #Initializing font module
        pygame.font.init()

        #Initialzing high score from text file "highscore.txt"
        try:
            filename = "highscore.txt"
            file = open(filename,"r")
            self.highest_score = int(file.read())
            if self.highest_score == ' ':
                self.highest_score=0
            file.close()
        except:
            self.highest_score=0
        #Functions for working on Sound, initial, score, displaying etc.
        #def reset(self):

    def welcome_screen(self):
	#Filling screen black
        self.screen.fill(BLACK)

    	########################################
	    ####Loading Titles and Enemy Points#####
	    ########################################

        pygame.mixer.music.load('./sounds/Title_Screen.wav')
        pygame.mixer.music.play(-1)
        self.titleText1 = pygame.font.Font(FONT, 50)
        textsurface = self.titleText1.render('SPACE', False, TITLE_WHITE)
        self.screen.blit(textsurface,(300,120))

        self.titleText2 = pygame.font.Font(FONT, 33)
        textsurface = self.titleText2.render('INVADERS', False, LIGHT_GREEN)
        self.screen.blit(textsurface,(300,170))

        #This font will be used for all enemy ships text and Continue text
        self.titleText3 = pygame.font.Font(FONT, 25)

        self.enemy1 = pygame.image.load("./images/enemy3_1.png").convert_alpha()
        self.enemy1 = pygame.transform.scale(self.enemy1 , (40, 40))
        self.screen.blit(self.enemy1, (300, 250))

        textsurface = self.titleText3.render('   =  10 pts', False, GREEN)
        self.screen.blit(textsurface,(350,250))

        self.enemy2 = pygame.image.load("./images/enemy2_2.png").convert_alpha()
        self.enemy2 = pygame.transform.scale(self.enemy2 , (40, 40))
        self.screen.blit(self.enemy2, (300, 300))

        textsurface = self.titleText3.render('   =  20 pts', False, BLUE)
        self.screen.blit(textsurface,(350,300))

        self.enemy3 = pygame.image.load("./images/enemy1_2.png").convert_alpha()
        self.enemy3 = pygame.transform.scale(self.enemy3 , (40, 40))
        self.screen.blit(self.enemy3, (300, 350))

        textsurface = self.titleText3.render('   =  30 pts', False, PURPLE)
        self.screen.blit(textsurface,(350,350))

        self.enemy4 = pygame.image.load("./images/mystery.png").convert_alpha()
        self.enemy4 = pygame.transform.scale(self.enemy4 , (80, 40))
        self.screen.blit(self.enemy4, (281, 400))

        textsurface = self.titleText3.render('   =  ?????', False, RED)
        self.screen.blit(textsurface,(350,400))

        textsurface = self.titleText3.render('Press any key to continue', False, TITLE_WHITE)
        self.screen.blit(textsurface,(200,500))

    def update_stats(self):
        """
        Function to show current score, highest score and number of lifes left
        """
        self.scoreText = pygame.font.Font(FONT, 20)

        #update score
        textsurface = self.scoreText.render(("Score: "+str(self.current_score)), False, BLUE)
        self.screen.blit(textsurface,(5,5))

        #update high score
        if self.highest_score <= self.current_score:
            self.highest_score = self.current_score
            #To write highest score to file
            filename = "highscore.txt"
            file = open(filename,"w")
            file.write(str(self.highest_score))
            file.close()

        textsurface = self.scoreText.render(("Highest Score: "+str(self.highest_score)), False, BLUE)
        self.screen.blit(textsurface,(280,5))

        #update Lifes
        textsurface = self.scoreText.render("Lives: ", False, BLUE)
        self.screen.blit(textsurface,(645,5))

        for i in range(self.lives):
            self.live = pygame.image.load("./images/ship.png").convert_alpha()
            self.live = pygame.transform.scale(self.live , (20, 20))
            self.screen.blit(self.live, (725+(i*25), 7))


    def update_screen(self):
        self.screen.fill(BLACK)
        self.new_surface.blit(self.background, (0,0))
        self.screen.blit(self.new_surface,(0,0))

    def start_game(self):
        self.background = pygame.image.load("./images/background.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (800,600))

        ## ADD GAMEPLAY START SOUND HERE
        self.timer_1 = 0
        self.timer_2 = 0
        self.timer_3 = 0
        self.start_time = time.time()
        self.screen.fill(BLACK)

        end =  False
        while not end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.elapsed_time = time.time() - self.start_time
            if self.elapsed_time <= 1:
                alpha = (1.0 * self.elapsed_time)

            else:
                end = True

            self.new_surface = pygame.surface.Surface((800,600))
            self.new_surface.set_alpha(255 * alpha)

            self.update_screen()
            pygame.display.flip()

        ### ADD all Sprites class object declaration HERE ###

        #Defender Ship
        self.player = Ship(375, 530)
        self.player.draw(self.screen)

        #Blockers
        self.block_1 = Blocker(75,450)
        self.block_2 = Blocker(337.5,450)
        self.block_3 = Blocker(600, 450)
        self.block_1.draw()
        self.block_2.draw()
        self.block_3.draw()

        # Drawing ships
        self.All_Aliens = pygame.sprite.Group()
        for i in range(11):
            self.SHIP = Enemy("./images/enemy1_1.png", 20 + 50 * i, 80)
            self.All_Aliens.add(self.SHIP)
            self.SHIP.draw()
        for i in range(11):
            self.SHIP = Enemy("./images/enemy2_1.png", 20 + 50 * i, 130)
            self.All_Aliens.add(self.SHIP)
            self.SHIP.draw()
        for i in range(11):
            self.SHIP = Enemy("./images/enemy2_1.png", 20 + 50 * i, 180)
            self.All_Aliens.add(self.SHIP)
            self.SHIP.draw()
        for i in range(11):
            self.SHIP = Enemy("./images/enemy3_1.png", 20 + 50 * i, 230)
            self.All_Aliens.add(self.SHIP)
            self.SHIP.draw()
        for i in range(11):
            self.SHIP = Enemy("./images/enemy3_1.png", 20 + 50 * i, 280)
            self.All_Aliens.add(self.SHIP)
            self.SHIP.draw()

        # All_Aliens.add(Alien_Row_1, Alien_Row_2, Alien_Row_3, Alien_Row_4, Alien_Row_5)
        # All_Aliens.update()

        pygame.display.flip()
        # self.SHIP.update()

        self.draw_state += 1

    def main(self):
        quit = False
        self.welcome_screen() #Display welcome message
        self.st = time.time()
        self.dt = 0
        while not quit:

            if self.draw_state == 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: #If user quits game
                        quit = True
                    if event.type == pygame.KEYDOWN:
                        self.start_game()

            if self.draw_state > 0:

                #Updating Ship's location
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: #If user quits game
                        quit = True
                keystate = pygame.key.get_pressed()

                ### CALL All updating functions here ###
                self.screen.blit(self.background,(0,0))
                self.player.update(self.screen, keystate)
                self.block_1.draw()
                self.block_2.draw()
                self.block_3.draw()

                game.SHIP.update()
                self.dt = time.time() - self.st
                self.update_stats()

            """ if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        #print("Shoot")
                        shoot()
                    if event.key == pygame.K_RIGHT:
                        #print("Right")
                        right()
                    if event.key == pygame.K_LEFT:
                        #print("Left")
                        left()
            if self.draw_state == 0:#If game has just begun
                self.welcome_screen()#Display welcome message

            if self.draw_state > 0: #If game has already begun
                self.screen.fill(BLACK)
                draw()#Draw game matrix

                won = 1
                #If user destroys all enemy ships
                for i in range(0,11):
                    for j in range(0,5):
                        if enemy_ship[i][j]==1: #Checking if any ship is left
                            won = 0
                if won == 1:
                    win_message()#Displaying victory message by calling win_message() function
            """
            pygame.display.flip()
            #pygame.display.update() #Update portions of the screen for software displays

        pygame.quit() #Uninitialize all pygame modules


if __name__ == '__main__':
    game = SpaceInvaders()
    game.main()
