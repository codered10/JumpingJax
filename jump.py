import pygame
import os
import random
import neat
import visualize
import pickle
vec = pygame.math.Vector2
import math

HEIGHT = 400
WIDTH = 800
FPS = 30
SPRITESHEET = "SpriteSheet_A.png"
#clock = pygame.time.Clock()
HS_FILE = "highscore.txt"

#COLORS
RED =(255,0,0)
GREEN= (0,255,0)
BLUE = (0,0,255)
WHITE =(255,255,255)
BLACK =(0,0,0)
GRAVITY = 0.8
FONT_NAME = 'arial'
#global x = 0

#set up assets folder
game_folder = os.path.dirname(__file__)
img_folder =os.path.join(game_folder, "imgs")
with open(os.path.join(game_folder, HS_FILE), 'r') as f:
    try:
        highscore_data = int(f.read())
    except:
        highscore_data = 0
        print("cannotttt loaddd ")
gen = 0

#Initialize pygame and set screen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Jumping Jax")
#screen.fill(WHITE)
clock = pygame.time.Clock()
font_name = pygame.font.match_font(FONT_NAME)

class Spritesheet():
    #utility class for loading and parsing Spritesheet
    def __init__(self,filename):
        self.spritesheet = pygame.image.load(filename).convert()
        """.convert()"""

    def get_image(self, x , y, width, height):
        #grab an image out of a larger spritesheet
        image = pygame.Surface((width, height)).convert()
        image.blit(self.spritesheet,(0,0), (x, y, width, height))
        #image.set_colorkey(BLACK)

        return image

# load spritesheet image
spritesheet = Spritesheet(os.path.join(img_folder, SPRITESHEET))


# load ground from spritesheet
bg = spritesheet.get_image(2, 54, 1200, 12)
bg.set_colorkey(BLACK)
#screen.blit(bg, (50,HEIGHT- 120))
bgX = 0
bgX2 = bg.get_width()

class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((20,50))
        self.last_update = 0
        self.current_frame = 0
        self.running = True
        self.jumping = False
        self.death = False
        self.load_images()
        self.image = self.running_frames[0].convert()
        #self.image.set_colorkey(BLACK)
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.bottom = HEIGHT - 28
        self.speedx = 0
        self.pos = vec(100, HEIGHT - 28)
        self.vel = vec(0,0)
        self.gravity = vec(0, GRAVITY)

    def load_images(self):
        self.running_frames = [spritesheet.get_image(936, 2, 44, 47),
                                spritesheet.get_image(980, 2, 44, 47)]
        for frame in self.running_frames:
            frame.set_colorkey(BLACK)

        self.jumping_frames = [spritesheet.get_image(848,2,44,47)]
        for frame in self.jumping_frames:
            frame.set_colorkey(BLACK)

        self.death_frames = [spritesheet.get_image(1024,2,44,47),spritesheet.get_image(1070,4,40,43)]
        for frame in self.death_frames:
            frame.set_colorkey(BLACK)

    def animate(self):
        now = pygame.time.get_ticks()
        if self.running:
            if now - self.last_update > 100:
                self.current_frame = (self.current_frame + 1) % len(self.running_frames)
                self.last_update = now
                bottom = self.rect.bottom
                self.image = self.running_frames[self.current_frame].convert()
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.centerx = 100
        if self.jumping:
            self.image = self.jumping_frames[0].convert()
            bottom = self.rect.bottom
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            self.rect.centerx = 100
        self.mask = pygame.mask.from_surface(self.image)
        if self.death:
            #print("death reached ****")
            if now - self.last_update > 1:
                self.current_frame = (self.current_frame + 1) % len(self.death_frames)
                self.last_update = now
                #bottom = self.rect.bottom
                bottom = self.rect.bottom
                #print("bottom ====", bottom)
                self.image = self.death_frames[self.current_frame].convert()
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.centerx = 100

    def jump(self):
        if self.rect.bottom == HEIGHT - 28:
            self.vel.y = -12
            self.jumping = True
        # equations of motion

    def die(self):
        self.death = True
        self.jumping = False
        self.running = False

    def update(self):
        # any code here will happen every time the game loop updates
        #self.animate()
        #keystate = pygame.key.get_pressed()
        # equations of motion
        #print(self.pos)
        if self.vel.y != 0:
            self.vel += self.gravity
            self.pos += self.vel + 0.5 * self.gravity
            if self.pos.y == HEIGHT - 28:
                self.vel.y = 0
                self.jumping = False
            self.rect.centerx = self.pos.x
            self.rect.bottom = self.pos.y
         # wrap around the sides of the screen
        #if self.pos.y > HEIGHT:
        #    self.pos.y = 0
        #if self.pos.y < 0:
        #    self.pos.y = HEIGHT
        #self.rect.centerx = self.pos.x
        #self.rect.bottom = self.pos.y
        #self.rect.midbottom = self.pos
        self.animate()

    """self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        """

class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((20,50))
        self.last_update = 0
        self.current_frame = 0
        self.load_images()
        #self.image = self.cacti_frames01[7]
        #self.image.set_colorkey(BLACK)
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.bottom = HEIGHT - 28
        self.x = 0

    def load_images(self):
        i=0
        posx01 = 228
        width01 = 102//6
        posx02 = 332
        #width02 = 49 //2
        width02 = 100 // 4
        #posx03 = 432
        #width03 = 100//4
        self.cacti_frames01 = []
        self.cacti_frames02 = []
        self.cacti_frames03 = []
        for i in range(6):
            self.cacti_frames01.append(spritesheet.get_image(posx01, 2, width01 , 35 ))
            posx01 += width01
        """for frame in self.cacti_frames01:
            frame.set_colorkey(BLACK)"""
        for i in range(4):
            if i == 3:
                self.cacti_frames02.append(spritesheet.get_image(posx02, 2, width02-1 , 50 ))
                posx02 += width02
                break
            self.cacti_frames02.append(spritesheet.get_image(posx02, 2, width02 , 50 ))
            posx02 += width02
        """for frame in self.cacti_frames02:
            frame.set_colorkey(BLACK)"""
        self.cacti_frames03 = [spritesheet.get_image(432, 2, 50 , 50 )]
        """for frame in self.cacti_frames03:
            frame.set_colorkey(BLACK)"""
        self.cacti_frames01 += self.cacti_frames02 + self.cacti_frames03
        self.load_random()

    def load_random(self):
        w1 = 17
        h1 = 35
        w2 = 25
        h2 = 50
        w3 = 50
        h3 = 50

        #nSprites = random.randrange(1,3)
        self.image = pygame.Surface((75,50)).convert()
        i = 0
        nSprites = random.randrange(1,4)
        #print(nSprites)
        widthPrev = 0
        for i in range(nSprites):
            tSprite = random.randrange(0,11)
            #print(tSprite)
            if tSprite == 10:
                self.image.blit(self.cacti_frames01[tSprite],(0,0))
                break
            if tSprite in range(0,6):
                self.image.blit(self.cacti_frames01[tSprite],(widthPrev,50-self.cacti_frames01[tSprite].get_rect().height-2))
            else:
                self.image.blit(self.cacti_frames01[tSprite],(widthPrev,50-self.cacti_frames01[tSprite].get_rect().height))
            widthPrev += self.cacti_frames01[tSprite].get_rect().width
        self.image.set_colorkey(BLACK)
        self.mask = pygame.mask.from_surface(self.image)
        #self.mimage = pygame.Surface((75,50)).convert()
        """olist = self.mask.outline()
        pygame.draw.lines(self.image, (BLUE),1,olist)"""


    def update(self):
        # any code here will happen every time the game loop updates
        #self.animate()
        self.rect.x -= 5

all_sprites = pygame.sprite.Group()
cactus_sprites = pygame.sprite.Group()
dino = Dinosaur()
#cactus = Cactus() #need it
#all_sprites.add(cactus)
#cactus_sprites.add(cactus)
all_sprites.add(dino)
"""def redrawWindow():
    #largeFont = pygame.font.SysFont('comicsans', 30)
    screen.blit(bg, (bgX, HEIGHT-20))
    screen.blit(bg, (bgX2,HEIGHT-20))
    #text = largeFont.render('Score: ' + str(score), 1, (255,255,255))
    #runner.draw(win)
    '''for obstacle in obstacles:
        obstacle.draw(win)'''

    #win.blit(text, (700, 10))
    pygame.display.update()"""
# Game loop
interval = pygame.time.get_ticks()
#count = 10
#x=0
#running = True
#score = 0
def draw_text(text, size, color, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)
        #pygame.display.update()

waiting = True
while waiting:
    clock.tick(FPS)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            waiting = False
            pygame.quit()
        if event.type == pygame.KEYUP:
            waiting = False
#cactus_ind = 0
def draw_window(dinos, cactus_list,cactus_ind):
    """
    draws the windows for the main game loop
    :param win: pygame window surface
    :param bird: a Bird object
    :param pipes: List of pipes
    :param score: score of the game (int)
    :param gen: current generation
    :param pipe_ind: index of closest pipe
    :return: None
    """
    for dino in dinos:
        # draw lines from bird to pipe
        if True:
            #print("dino  ", dino.rect.x )
            #pygame.draw.line(screen, RED, (100 , dino.rect.y),  (cactus_list[cactus_ind].rect.x, 0), 5)
            try:
                pygame.draw.line(screen, RED, (dino.rect.x + dino.rect.width , dino.rect.y), (cactus_list[cactus_ind].rect.x,cactus_list[cactus_ind].rect.y), 5)
                pygame.draw.line(screen, GREEN, (dino.rect.x + dino.rect.width , dino.rect.y), (cactus_list[cactus_ind].rect.x,cactus_list[cactus_ind].rect.y + cactus_list[cactus_ind].rect.height ), 5)
                #print("enter ", cactus_list[cactus_ind])
                #pygame.draw.line(screen, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
            except Exception as e:
                #print(e)
                pass

    pygame.display.update()

def eval_genomes(genomes, config):
#def loop():
    """
    runs the simulation of the current population of
    birds and sets their fitness based on the distance they
    reach in the game.
    """
    nets = []
    dinos = []
    ge = []
    cactus_ind = 0



    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        dino = Dinosaur()
        all_sprites.add(dino)
        dinos.append(dino)
        ge.append(genome)

    cactus_list = []
    cactus = Cactus()
    all_sprites.add(cactus)
    cactus_sprites.add(cactus)
    cactus_list.append(cactus)



    x=0
    running = True
    score = 0

    while running and len(dinos) > 0:

        clock.tick(FPS)
        #all_sprites.add(dino)
        # keep loop running at the right speed
        #clock.tick(FPS)
        #draw_text(str(score), 22, BLACK, 600, 20)
        screen.fill(WHITE)
        #draw_text("HIGH SCORE    " + str(highscore_data), 22, BLUE, 100, 20)
        draw_text(str(score), 22, BLACK, 600, 20)
        rel_x = x % bg.get_rect().width
        screen.blit(bg, (rel_x - bg.get_rect().width, HEIGHT -40))
        #bg.set_colorkey(BLACK)
        if rel_x < WIDTH:
            screen.blit(bg, (rel_x,HEIGHT- 40))
            #bg.set_colorkey(BLACK)
        x -= 5
        if x % random.randrange(200,800,200) == 0:
            cactus = Cactus()
            cactus_list.append(cactus)
            #cactus_list = [cactus]
            #print("dd ",cactus_list)
            all_sprites.add(cactus)
            #print("dd ",cactus_list)
            cactus_sprites.add(cactus)
        #pygame.draw.line(screen, (255, 0, 0), (rel_x, 0), (rel_x, HEIGHT), 3)
        #pygame.display.update()
        # Process input (events)
        #cactus_ind = 0
        #global cactus_ind
        if len(dinos) > 0:
            if len(dinos) > 1 and dinos[0].rect.x > cactus_list[cactus_ind].rect.x + 75:  # determine whether to use the first or second
                cactus_ind += 1
                #print (cactus_ind)
            #before nice lines
            """cactus_list[cactus_ind].mask = pygame.mask.from_surface(cactus_list[cactus_ind].image)
            #self.mimage = pygame.Surface((75,50)).convert()
            olist = cactus_list[cactus_ind].mask.outline()
            pygame.draw.lines(cactus_list[cactus_ind].image, (BLUE),1,olist)"""

        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            """if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()"""

        for x0, dino in enumerate(dinos):  # give each bird a fitness of 0.1 for each frame it stays alive
            ge[x0].fitness += 0.1
            #bird.move()
            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            #output = nets[dinos.index(dino)].activate((dino.rect.x + dino.rect.width, abs(cactus_list[cactus_ind].rect.x - (dino.rect.x + dino.rect.width)),cactus_list[cactus_ind].rect.x + 75, cactus_list[cactus_ind].rect.y))
            #pygame.draw.line(screen, RED, (dino.rect.x + dino.rect.width , dino.rect.y), (cactus_list[cactus_ind].rect.x,cactus_list[cactus_ind].rect.y), 5)
            #pygame.draw.line(screen, GREEN, (dino.rect.x + dino.rect.width , dino.rect.y), (cactus_list[cactus_ind].rect.x,cactus_list[cactus_ind].rect.y + cactus_list[cactus_ind].rect.height ), 5)
            ar01=math.hypot(((dino.rect.x + dino.rect.width)-cactus_list[cactus_ind].rect.x),(dino.rect.y-cactus_list[cactus_ind].rect.y))
            ar02=math.hypot(((dino.rect.x + dino.rect.width)-cactus_list[cactus_ind].rect.x),(dino.rect.y-(cactus_list[cactus_ind].rect.y + cactus_list[cactus_ind].rect.height )))
            output = nets[dinos.index(dino)].activate((dino.rect.x + dino.rect.width, ar01,ar02, cactus_list[cactus_ind].rect.x + 75))

            if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                dino.jump()

        # Update
        """
        hits = pygame.sprite.spritecollide(dino , cactus_sprites, False, pygame.sprite.collide_mask)
        if hits:
            dino.die()
            #dino.pos.y = hits[0].rect.top
            if (score> highscore_data):
                highscore_data = score
                #draw_text("HIGH SCORE    " + str(highscore_data), 22, BLUE, 100, 20)
                with open(os.path.join(game_folder, HS_FILE), 'w') as f:
                        f.write(str(score))
            running = False
            """
        for dino in dinos:
            hits = pygame.sprite.spritecollide(dino , cactus_sprites, False, pygame.sprite.collide_mask)
            if hits:
                dino.die()
                ge[dinos.index(dino)].fitness -= 1
                nets.pop(dinos.index(dino))
                ge.pop(dinos.index(dino))
                dinos.pop(dinos.index(dino))
                dino.kill()
                #running = False



        all_sprites.update()
        """hits = pygame.sprite.spritecollide(dino , cactus_sprites, False, pygame.sprite.collide_mask)
        if hits:
            dino.die()
            running = False"""
        # Draw / render
        #screen.fill(WHITE)
        all_sprites.draw(screen)
        score += 1
        #draw_text(str(score), 22, BLACK, 600, 20)
        # *after* drawing everything, flip the display
        #draw_window(dinos,cactus_list, cactus_ind)
        pygame.display.update()
        draw_window(dinos,cactus_list, cactus_ind)
        #clock.tick(FPS)
    #pygame.quit()
    cactus_sprites.empty()
    all_sprites.empty()

def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)
    #loop()

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
