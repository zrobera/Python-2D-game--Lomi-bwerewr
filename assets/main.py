import pygame
from os import walk
import random



pygame.init()
WIDTH, HEIGHT = 1200, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("lomi")
FPS = 60


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image = pygame.image.load('./assets/bg.png')
        final_width, final_height = image.get_width(), image.get_height()
        self.image = pygame.Surface((final_width * 2, final_height))
        self.image.blit(image, (0, -150))
        self.image.blit(image, (final_width, -150))
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self,speed):
        self.pos.x -= speed
        if self.rect.centerx < 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)


class Lemon(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        image = pygame.image.load('./assets/lemon.png')
        self.image = pygame.transform.scale(image, (image.get_width() * 0.1, image.get_height() * 0.1))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.dir = pygame.math.Vector2(1, 1)




    def throw(self):
        self.rect.x += self.dir.x * self.speed
        if self.rect.left>WIDTH:
            self.kill()
    
    def update(self):
        self.throw()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.status = 'run'
        self.animation_index = 0
        self.animation_speed = 0.45
        self.import_images()
        image = self.animations[self.status][self.animation_index]
        self.image = pygame.transform.scale(image, (image.get_width() * 0.4, image.get_height() * 0.4))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)
        self.throw_counter=0
    def import_images(self):
        path = './assets/boy/'
        self.animations = {"idle": [], 'run': [], 'throw': []}
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = self.import_folder(full_path)

    def import_folder(self, full_path):
        surface_list = []
        for _, __, img_files in walk(full_path):
            for image in img_files:
                real_full_path = full_path + "/" + image
                image_surf = pygame.image.load(real_full_path).convert_alpha()
                surface_list.append(image_surf)
        return surface_list

    def animate(self):
        self.animation = self.animations[self.status]
        self.animation_index += self.animation_speed
        
        if self.animation_index >= len(self.animation):
            if self.status=='throw':
                self.status="run"
                self.animation_index = 0
            else:
             self.animation_index = 0
        image = self.animation[int(self.animation_index)]
        self.image = pygame.transform.scale(image, (image.get_width() * 0.4, image.get_height() * 0.4))
    def change_state(self,state):
        self.animation_index=0
        self.status=state
    def update(self):
        self.animate()

class Girl(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.status = 'run'
        self.animation_index = 0
        self.animation_speed = 1
        self.import_images()
        image = self.animations[self.status][self.animation_index]
        self.image = pygame.transform.scale(image, (image.get_width()*1.4, image.get_height()*1.4 ))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)
        self.gravity=2
        self.dir=pygame.math.Vector2(0,0)
        self.game_end=False
    def apply_gravity(self):
        self.dir.y+=self.gravity
        self.rect.y+=self.dir.y
        if self.rect.bottom>540:
            self.rect.bottom=540
            self.dir.y=0
    def jump(self):
        if self.dir.y==0:
         self.dir.y=-32



    def import_images(self):
        path = './assets/girl/'
        self.animations = {'run': [],"die":[]}
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = self.import_folder(full_path)

    def import_folder(self, full_path):
        surface_list = []
        for _, __, img_files in walk(full_path):
            for image in img_files:
                real_full_path = full_path + "/" + image
                image_surf = pygame.image.load(real_full_path).convert_alpha()
                surface_list.append(image_surf)
        return surface_list
    def animate(self):
        self.animation = self.animations[self.status]
        self.animation_index += self.animation_speed
        
        if self.animation_index >= len(self.animation):
            if self.status=='die':
                self.animation_index = len(self.animation)-1
                self.game_end=True
            else:
             self.animation_index = 0
        image = self.animation[int(self.animation_index)]
        self.image = pygame.transform.scale(image, (image.get_width() * 1.4, image.get_height() * 1.4))
    def change_state(self,state):
        self.animation_index=0
        self.status=state
    def update(self):
        self.apply_gravity()
        self.animate()
        if self.game_end:
            return False
        return True
        
        


def handle_collision(girl ,lomi_sprite,player):
   if pygame.sprite.spritecollide(girl,lomi_sprite,True):
       girl.change_state('die')
       player.change_state('idle')
       return False
   return True
def draw_start_screen():
    image=pygame.image.load('./assets/start.png')
    image=pygame.transform.scale(image,(image.get_width()*2,image.get_height()*2))
    start_rect=image.get_rect()
    start_rect.center=(WIDTH//2,500)
    boy=pygame.image.load('./assets/boy/idle/skeleton-00_idle_0.png')
    boy=pygame.transform.scale(boy,(boy.get_width()*0.3,boy.get_height()*0.3))
    boy_rect=boy.get_rect()
    boy_rect.center=(320,400)
    girl=pygame.image.load('./assets/girl/die/gr.png')
    girl_rect=girl.get_rect()
    girl_rect.center=(890,440)

    lomi=pygame.image.load('./assets/lomi.png')
    lomi=  pygame.transform.rotate(pygame.transform.scale(lomi,(lomi.get_width()*0.15,lomi.get_height()*0.15)),-40) 
    lomi_rect=lomi.get_rect()
    lomi_rect.center=((WIDTH//2)+80,250)

    text=pygame.image.load('./assets/text.png')
    text=pygame.transform.scale(text,(text.get_width()*1.2,text.get_height()*1.2)) 
    text_rect=text.get_rect()
    text_rect.center=((WIDTH//2)+80,140)

    
    WIN.blit(image,start_rect)
    WIN.blit(boy,boy_rect)
    WIN.blit(girl,girl_rect)
    WIN.blit(lomi,lomi_rect)
    WIN.blit(text,text_rect)
    mouse_buttons = pygame.mouse.get_pressed()
    if start_rect.collidepoint(pygame.mouse.get_pos()) and  mouse_buttons[0]:
        return "playing"
    return "start"
def draw_last_screen(girl,player,lemons_sprite,initial_shoot_interval,score):
        text=pygame.image.load('./assets/again.png')
        text=pygame.transform.scale(text,(text.get_width(),text.get_height())) 
        text_rect=text.get_rect()
        text_rect.center=((WIDTH//2),(HEIGHT//2)+200)
        WIN.blit(text,text_rect)
        score_text=score
        score_text = str(f"Score: {score_text}")
        text_surface = font.render(score_text, True, (128,0,32))
        text_rect = text_surface.get_rect()
        text_rect.center = (WIDTH // 2, (HEIGHT // 2)+110)
        WIN.blit(text_surface, text_rect)
        

        mouse_buttons = pygame.mouse.get_pressed()
        if text_rect.collidepoint(pygame.mouse.get_pos()) and  mouse_buttons[0]:
                girl.change_state('run')
                player.change_state('run')
                lemons_sprite.empty()
                return 0, pygame.time.get_ticks(),initial_shoot_interval,"playing"
        return 0,0,0,"game_over"
def display_score(score):
    score_text = pygame.font.Font(None, 60).render("score "+str(score), True, (255, 0, 0))
    WIN.blit(score_text, (50, 50))






clock = pygame.time.Clock()

all_sprite_for_now = pygame.sprite.Group()
all_sprite_for_now.add(Background())

player_sprite= pygame.sprite.GroupSingle()
player_sprite.add(Player(10, 560))
player=player_sprite.sprite

girl_sprite= pygame.sprite.GroupSingle()
girl_sprite.add(Girl(900, 560))
girl=girl_sprite.sprite




lemons_sprite = pygame.sprite.Group()
final_score=0
run = True
initial_shoot_interval = 4000  
shoot_interval = initial_shoot_interval
last_shoot_time = pygame.time.get_ticks()
time_passed = 0 
game_state = "start"

font = pygame.font.Font(None, 60)
score=0
while run:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                girl.jump()
                score+=1
           
    current_time = pygame.time.get_ticks()
  
    if current_time - last_shoot_time > shoot_interval and game_state == "playing":
        lemons_sprite.add(Lemon(200, 460, 14))
        player.change_state("throw")
        last_shoot_time = current_time

    time_passed += clock.get_time()
    if time_passed >= 6000 and shoot_interval > 1000:
        shoot_interval -= 400
        time_passed = 0

    if game_state == "playing":
        all_sprite_for_now.update(8)
        all_sprite_for_now.draw(WIN)
        display_score(score)
    else:
        all_sprite_for_now.update(0)
        all_sprite_for_now.draw(WIN)
    if game_state == "start":
       game_state= draw_start_screen()
       if game_state=='playing':last_shoot_time=pygame.time.get_ticks()
    else:
        player_sprite.update()
        player_sprite.draw(WIN)
        girl_sprite.update()
        girl_sprite.draw(WIN)
        lemons_sprite.update()
        lemons_sprite.draw(WIN)
    
    if(score!=0):
        final_score=score
    if game_state == "game_over":
        score,last_shoot_time,initial_shoot_interval,game_state=draw_last_screen(girl,player,lemons_sprite,initial_shoot_interval,final_score)

    if not handle_collision(girl, lemons_sprite, player) and game_state == "playing":
        game_state = "game_over"  

    pygame.display.update()

pygame.quit()
