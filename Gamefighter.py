import pygame
from pygame import mixer
import time,sys
from fighters import Fighter

mixer.init()
pygame.init()

width = 1000
height = 700

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Fighter Game")




# upload music and sounds # 
pygame.mixer.music.load("C:\\Users\\Main\\Desktop\\learnC++\\MyProtfilo\\pythonGames\\music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1,0.0,5000)
sword_fx = pygame.mixer.Sound("C:\\Users\\Main\\Desktop\\learnC++\\MyProtfilo\\pythonGames\\sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("C:\\Users\\Main\\Desktop\\learnC++\\MyProtfilo\\pythonGames\\magic.wav")
magic_fx.set_volume(0.75)
# set frame rate #
clock = pygame.time.Clock()
FBS = 60
# define font 
count_font = pygame.font.Font("C:\\Users\\Main\\Desktop\\learnC++\\MyProtfilo\\pythonGames\\turok.ttf", 80)
score_font = pygame.font.Font("C:\\Users\\Main\\Desktop\\learnC++\\MyProtfilo\\pythonGames\\turok.ttf", 30)

# define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
# define fighter variables #
warrior_size = 162
warrior_scale = 4
warrior_offset = [72,56]
warrior_data = [warrior_size , warrior_scale ,warrior_offset]
wizard_size = 250
wizard_scale = 3
wizard_offset = [112,107]
wizard_data = [wizard_size , wizard_scale , wizard_offset]

# define score variables
score = [0,0]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# load background image #
bg_image = pygame.image.load("C:\\Users\\Main\\Desktop\\learnC++\\MyProtfilo\\pythonGames\\background.jpg").convert_alpha()
# load warrior for sprites #
warrior_sheet = pygame.image.load("C:\\Users\\Main\\Desktop\\learnC++\\MyProtfilo\\pythonGames\\warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("C:\\Users\\Main\\Desktop\\learnC++\\MyProtfilo\\pythonGames\\wizard.png").convert_alpha()
# load victory images #
victor_img = pygame.image.load("C:\\Users\\Main\\Desktop\\learnC++\\MyProtfilo\\pythonGames\\victory.png").convert_alpha()

# define num. of steps in each animation !#
WARRIOR_ANIMATION_LIST = [10,8,1,7,7,3,7]
WIZARD_ANIMATION_LIST = [8,8,1,8,8,3,7] 

# function to draw text
def draw_text(text,font,font_color , x,y):
    img = font.render(text, True , font_color)
    screen.blit(img ,(x,y))

# function to draw the bg #
def draw_bg():
    scale_bg = pygame.transform.scale(bg_image,(width,height))
    screen.blit(scale_bg,(0,0))

# function to draw health bars #
def draw_healthBar(health ,x,y):
    ratio = health / 100
    pygame.draw.rect(screen, 'white' , (x-3,y-3,404 ,34))
    pygame.draw.rect(screen, 'red' , (x,y,400 ,30) )
    pygame.draw.rect(screen , 'yellow' , (x,y , 400 * ratio, 30))


# create 2 instances of fighters #
fighter_1 = Fighter(1,200,390,False,warrior_data,warrior_sheet,WARRIOR_ANIMATION_LIST,sword_fx)
fighter_2 = Fighter(2,650,440,True,wizard_data,wizard_sheet,WIZARD_ANIMATION_LIST,magic_fx)

run = True
while run:
    clock.tick(FBS)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    # call draw func #
    draw_bg()
    # show player health bar #
    draw_healthBar(fighter_1.health,20,20)
    draw_healthBar(fighter_2.health,580,20)
    draw_text("Warrior: " + str(score[0]),score_font,'red',20,60)
    draw_text("wizard: " + str(score[1]),score_font,'red',580,60)
    # call draw func as fighter #
    fighter_1.draw(screen)
    fighter_2.draw(screen)
    # updates the fighters #
    if intro_count <= 0:         
        fighter_1.move(width,height,fighter_2,round_over)
        fighter_2.move(width,height,fighter_1,round_over)
    else:
        # display time counter #
        draw_text(str(intro_count),count_font,'red' , width / 2 , height / 3)
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
        
    fighter_1.update()
    fighter_2.update()
    # call the move func #
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        # display victory images #
        screen.blit(victor_img,(360,150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1,200,390,False,warrior_data,warrior_sheet,WARRIOR_ANIMATION_LIST,sword_fx)
            fighter_2 = Fighter(2,650,440,True,wizard_data,wizard_sheet,WIZARD_ANIMATION_LIST,magic_fx)

    pygame.display.update()
pygame.quit()
