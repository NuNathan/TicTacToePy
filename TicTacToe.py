# imports
import pygame
import random

# sprite class
class Sprite(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()

        self.image = pygame.Surface([width, height])

        pygame.draw.rect(self.image, "white", pygame.Rect(0,0, width, height))
        self.Rect = self.image.get_rect(topleft = (x, y))
        self.rect = (x, y)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.isx = False
        self.isy = False

    # at certain points later we are going to need to draw specific things in place of the sprites
    def draw(self, screen):
        pygame.draw.rect(self.image, "white", pygame.Rect(0,0, self.width, self.height))
        screen.blit(self.image, self.rect)
    def drawx(self, screen):
        pygame.draw.line(self.image, "green", (0,0), (self.width, self.height), 20)
        pygame.draw.line(self.image, "green", (self.width,0), (0, self.height), 20)
        screen.blit(self.image, self.rect)
    def drawy(self, screen):
        pygame.draw.circle(self.image, "blue", (self.width/2, self.height/2), self.width/3, width=10)
        screen.blit(self.image, self.rect)

# initialize some variables

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
w, h = pygame.display.get_surface().get_size()
ev = pygame.event.get()
all_sprites_list = pygame.sprite.Group()
turns = 0
WIN = 0
running = True
menu = True
ups = True
end = True
difficulty = 0
guessed = False


#top row
top_left = Sprite((w/3)-50, (h/3)-50, 50, 50)
top_center = Sprite((w/3), (h/3)-50, ((w)/3), 50)
top_right = Sprite((w/3)-50, (h/3)-50, ((w*2)/3), 50)

# #middle row
middle_left = Sprite((w/3)-50, (h/3), 50, ((h)/3))
middle_center = Sprite((w/3), (h/3), ((w)/3), h/3)
middle_right = Sprite((w/3)-50, (h/3), ((w*2)/3), ((h)/3))

# #bottom row
bottom_left = Sprite((w/3)-50, (h/3)-50, 50, ((h*2)/3))
bottom_center = Sprite((w/3), (h/3)-50, ((w)/3), (h*2)/3)
bottom_right = Sprite((w/3)-50, (h/3)-50, ((w*2)/3), ((h*2)/3))

all_sprites_list.add(top_left)
all_sprites_list.add(top_center)
all_sprites_list.add(top_right)
all_sprites_list.add(middle_left)
all_sprites_list.add(middle_center)
all_sprites_list.add(middle_right)
all_sprites_list.add(bottom_left)
all_sprites_list.add(bottom_center)
all_sprites_list.add(bottom_right)

# loop for the entire game which is also holds the menu

while menu:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu = False
    
    #reset the screen and draw the menu

    screen.fill("white")
    font = pygame.font.SysFont(None, 200)
    img = font.render('Tic Tac Toe', True, "black")
    screen.blit(img, (30,30))

    Medium = pygame.draw.rect(screen, "black", pygame.Rect(200,500, 400, 75))
    font = pygame.font.SysFont(None, 120)
    img = font.render('Medium', True, "white")
    screen.blit(img, (250, 500))

    Easy = pygame.draw.rect(screen, "black", pygame.Rect(200,600, 400, 75))
    font = pygame.font.SysFont(None, 120)
    img = font.render('Easy', True, "white")
    screen.blit(img, (300, 600))

    pygame.display.flip()
    clock.tick(60) 

    #if a difficulty is pressed set difficulty and move on to next loop

    if pygame.mouse.get_pressed()[0] and Easy.collidepoint(pygame.mouse.get_pos()):
        difficulty = 1
    if pygame.mouse.get_pressed()[0] and Medium.collidepoint(pygame.mouse.get_pos()):
        difficulty = 2
    
    if difficulty > 0:

        running = True
        end = True
        ups = True
    else:
        continue

    # loop for the actual game

    while running:

        #wait for a mouseup to avoid the mouse down clicking something immediately

        while ups:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    ups = False
                if event.type == pygame.QUIT:
                    menu = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu = False

        # wipe the menu

        screen.fill("white")

        # draw the correct symbols on the screen

        for sprite in all_sprites_list:
            sprite.draw(screen)
            if sprite.isx:
                sprite.drawx(screen)
            elif sprite.isy:
                sprite.drawy(screen)

        pygame.draw.line(screen, "black", (w/3,50), (w/3,h-50), 10)
        pygame.draw.line(screen, "black", ((2*w)/3,50), ((2*w)/3,h-50), 10)
        pygame.draw.line(screen, "black", (50,h/3), (w-50,h/3), 10)
        pygame.draw.line(screen, "black", (50,(2*h)/3), (w-50,(2*h)/3), 10)

        # player clicks one of the squares

        if WIN == 0:
            for sprite in all_sprites_list:
                if pygame.mouse.get_pressed()[0] and sprite.Rect.collidepoint(pygame.mouse.get_pos()) and not (sprite.isx or sprite.isy):
                    sprite.isx = True
                    turns += 1

                    # check for player win

                    if top_left.isx:
                        if top_center.isx:
                            if top_right.isx:
                                WIN = 1
                        if middle_center.isx:
                            if bottom_right.isx:
                                WIN = 1
                        if middle_left.isx:
                            if bottom_left.isx:
                                WIN = 1
                    if middle_left.isx:
                        if middle_center.isx:
                            if middle_right.isx:
                                WIN = 1
                    if bottom_left.isx:
                        if bottom_center.isx:
                            if bottom_right.isx:
                                WIN = 1
                        if middle_center.isx:
                            if top_right.isx:
                                WIN = 1
                    if top_center.isx:
                        if middle_center.isx:
                            if bottom_center.isx:
                                WIN = 1
                    if top_right.isx:
                        if middle_right.isx:
                            if bottom_right.isx:
                                WIN = 1
                    
                    # make sure there is still a square left to pick and that the player has not won, then computer picks based on difficulty

                    if (turns <= 8) and (WIN == 0):
                        if difficulty == 1:
                            while True:
                                randspr = (random.choice(all_sprites_list.sprites()))
                                if (randspr.isx or randspr.isy) == False:
                                    randspr.isy = True
                                    turns +=1
                                    break

                        # crude medium difficulty that is just a proof of concept

                        elif difficulty == 2:
                            while True:
                                if top_left.isy:
                                    if top_center.isy:
                                        if not top_right.isx:
                                            top_right.isy = True
                                            guessed = True
                                            break
                                    if middle_center.isy:
                                        if not middle_center.isx:
                                            bottom_right.isy = True
                                            guessed = True
                                            break
                                    if middle_left.isy:
                                        if not middle_left.isx:
                                            bottom_left.isy = True
                                            guessed = True
                                            break
                                    if top_right.isy:
                                        if not top_center.isx:
                                            top_center.isy = True
                                            guessed = True
                                            break
                                    if bottom_left.isy:
                                        if not middle_center.isx:
                                            middle_center.isy = True
                                            guessed = True
                                            break
                                    if bottom_right.isy:
                                        if not middle_center.isx:
                                            middle_center.isy = True
                                            guessed = True
                                            break
                                if middle_left.isy:
                                    if middle_center.isy:
                                        if not middle_right.isx:
                                            middle_right.isy = True
                                            guessed = True
                                            break
                                    if middle_right.isy:
                                        if not middle_center.isx:
                                            middle_center.isy = True
                                            guessed = True
                                            break
                                if bottom_left.isy:
                                    if bottom_center.isy:
                                        if not bottom_right.isx:
                                            bottom_right.isy = True
                                            guessed = True
                                            break
                                    if middle_center.isy:
                                        if not top_right.isx:
                                            top_right.isy = True
                                            guessed = True
                                            break
                                    if bottom_right.isy:
                                        if not bottom_center.isx:
                                            bottom_center.isy = True
                                            guessed = True
                                            break
                                    if top_right.isy:
                                        if not middle_center.isx:
                                            middle_center.isy = True
                                            guessed = True
                                            break
                                    if middle_left.isy:
                                        if not top_left.isx:
                                            top_left.isy = True
                                            guessed = True
                                            break
                                if top_center.isy:
                                    if middle_center.isy:
                                        if not bottom_center.isx:
                                            bottom_center.isy = True
                                            guessed = True
                                            break
                                    if bottom_center.isy:
                                        if not middle_center.isx:
                                            middle_center.isy = True
                                            guessed = True
                                            break
                                if top_right.isy:
                                    if middle_right.isy:
                                        if not bottom_right.isx:
                                            bottom_right.isy = True
                                            guessed = True
                                            break
                                    if bottom_right.isy:
                                        if not middle_right.isx:
                                            middle_right.isy = True
                                            guessed = True
                                            break
                                    if middle_center.isy:
                                        if not middle_left.isx:
                                            middle_left.isy = True
                                            guessed = True
                                            break
                                if middle_right.isy:
                                    if middle_center.isy:
                                        if not middle_left.isx:
                                            middle_left.isy = True
                                            guessed = True
                                            break
                                if bottom_right.isy:
                                    if middle_right.isy:
                                        if not top_right.isx:
                                            top_right.isy = True
                                            guessed = True
                                            break
                                    if bottom_center.isy:
                                        if not bottom_left.isx:
                                            bottom_left.isy = True
                                            guessed = True
                                            break
                                    if middle_center.isy:
                                        if not top_left.isx:
                                            top_left.isy = True
                                            guessed = True
                                            break
                                if bottom_center.isy:
                                    if middle_center.isy:
                                        if not top_center.isx:
                                            top_center.isy = True
                                            guessed = True
                                            break
                                while not guessed:
                                    randspr = (random.choice(all_sprites_list.sprites()))
                                    if (randspr.isx or randspr.isy) == False:
                                        randspr.isy = True
                                        turns +=1
                                        break
                                guessed = False
                                break

                        # check for computer win
                            
                        if top_left.isy:
                            if top_center.isy:
                                if top_right.isy:
                                    WIN = 2
                            if middle_center.isy:
                                if bottom_right.isy:
                                    WIN = 2
                            if middle_left.isy:
                                if bottom_left.isy:
                                    WIN = 2
                        if middle_left.isy:
                            if middle_center.isy:
                                if middle_right.isy:
                                    WIN = 2
                        if bottom_left.isy:
                            if bottom_center.isy:
                                if bottom_right.isy:
                                    WIN = 2
                            if middle_center.isy:
                                if top_right.isy:
                                    WIN = 2
                        if top_center.isy:
                            if middle_center.isy:
                                if bottom_center.isy:
                                    WIN = 2
                        if top_right.isy:
                            if middle_right.isy:
                                if bottom_right.isy:
                                    WIN = 2

        # check for a draw
        
        if (turns == 9) and (WIN == 0):
            WIN = 3
        
        #check for if someone has won to draw the correct win screen

        if WIN == 1:
            pygame.draw.rect(screen, "black", pygame.Rect(100,100, 600, 180))
            font = pygame.font.SysFont(None, 200)
            img = font.render('You win!', True, "white")
            screen.blit(img, (115,130))
        if WIN == 2:
            pygame.draw.rect(screen, "black", pygame.Rect(100,100, 600, 180))
            font = pygame.font.SysFont(None, 170)
            img = font.render('You Lose!', True, "white")
            screen.blit(img, (115,130))
        if WIN == 3:
            pygame.draw.rect(screen, "black", pygame.Rect(100,100, 600, 180))
            font = pygame.font.SysFont(None, 170)
            img = font.render('You Draw!', True, "white")
            screen.blit(img, (115,130))
            
        # draw the play again screen and wait for a click on either the X or menu button
        
        if WIN > 0:
            back = pygame.draw.rect(screen, "black", pygame.Rect(300,600, 200, 75))
            font = pygame.font.SysFont(None, 120)
            img = font.render('Back', True, "white")
            screen.blit(img, (300,600))
            if pygame.mouse.get_pressed()[0] and back.collidepoint(pygame.mouse.get_pos()):
                while end:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            end = False
                            running = False
                        if event.type == pygame.QUIT:
                            end = False
                            menu = False
                            running = False

                # reset all of the variables for a second game

                running = False
                WIN = 0
                top_left.isx = False
                top_left.isy = False
                top_center.isx = False
                top_center.isy = False
                top_right.isx = False
                top_right.isy = False
                middle_left.isx = False
                middle_left.isy = False
                middle_center.isx = False
                middle_center.isy = False
                middle_right.isx = False
                middle_right.isy = False
                bottom_left.isx = False
                bottom_left.isy = False
                bottom_center.isx = False
                bottom_center.isy = False
                bottom_right.isx = False
                bottom_right.isy = False
                turns = 0
                difficulty = 0
                guessed = False

        pygame.display.flip()

    clock.tick(60)

pygame.quit()