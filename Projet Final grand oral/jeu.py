import pygame
import pytmx
import pyscroll
import time
from math import *

class SpriteSheet():
    def __init__(self,name):
        self.sprite_sheet = pygame.image.load(name)
        self.images =dict()




    def load_images(self ,name,numbers = 1,row = 0):
        images = []
        for i in range(0,numbers):
            image = pygame.Surface([32,32])
            image.blit(self.sprite_sheet,(0,0),(i * 32,32*row,32,32))
            images.append(image)

        self.images.update({name : images})


    def get_images(self,name):
        return self.images[name]

class Player(pygame.sprite.Sprite):

    def __init__(self,x,y):
        super().__init__()
        self.sprite_sheet= SpriteSheet("player.png")
        self.sprite_sheet.load_images("idle_r",numbers = 8)
        self.sprite_sheet.load_images("idle_l",numbers = 8,row = 1)
        self.sprite_sheet.load_images("run_r",numbers = 8,row = 2)
        self.sprite_sheet.load_images("run_l",numbers = 8,row = 3)
        self.sprite_sheet.load_images("attack_r",numbers = 8,row = 4)
        self.sprite_sheet.load_images("attack_l",numbers = 8,row = 5)
        self.sprite_sheet.load_images("hit",numbers = 8,row = 6)
        self.sprite_sheet.load_images("death",numbers = 8,row = 7)
        self.sprite_sheet.load_images("fall_r",numbers = 8,row = 8)
        self.sprite_sheet.load_images("fall_l",numbers = 8,row = 9)
        self.image = self.sprite_sheet.get_images("idle_r")[0]
        self.rect= self.image.get_rect()
        self.position  = [x,y]
        self.feet = pygame.Rect(0,0,self.rect.width,12)
        self.collision = pygame.Rect(0,0,self.rect.width,self.rect.height)
        self.current_animation = "idle_r"
        self.old_position = self.position
        self.current_animation_index = 0
        self.cooldown = -100
        self.speed=3
        self.life  = 3
        self.alive = True
        self.last_view = "idle_r"
        self.fall_instance = False

    def move_right(self):
        self.position[0] += self.speed

    def move_left(self):
        self.position[0] -= self.speed

    def move_up(self):
        self.position[1] -= self.speed

    def move_down(self):
        self.position[1] += self.speed

    def move_back(self):
        self.position = self.old_position

    def fall(self,spawn):
        if self.fall_instance == True:
            self.change_animation("fall_l")
        self.position = spawn

    def teleportation(self,spawn):
        self.position = spawn


    def change_animation(self,name):
        self.current_animation = name

    def get_animation(self):
        return self.sprite_sheet.get_images(self.current_animation)

    def animation(self):
        if self.cooldown > 100 :
            self.current_animation_index += 1
            if self.current_animation_index == len(self.get_animation()):
                self.current_animation_index = 0
            self.cooldown = 0

    def save_location(self):
        self.old_position = self.position.copy()

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.animation()
        self.image = self.get_animation()[self.current_animation_index %8]
        self.image.set_colorkey((0,0,0))
        self.image = pygame.transform.scale(self.image,(50,50))
        self.start = time.time()

class Pnj(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.sprite_sheet = SpriteSheet("female.png")
        self.sprite_sheet.load_images("idle",numbers = 6, row = 0)
        self.current_animation = "idle"
        self.image = self.sprite_sheet.get_images("idle")[0]
        self.position = [x,y]
        self.current_animation_index = 0
        self.cooldown = 0
        self.rect= self.image.get_rect()

    def get_animation(self):
        return self.sprite_sheet.get_images(self.current_animation)


    def update(self):
        self.rect.topleft=self.position
        self.animation()
        self.image=self.get_animation()[self.current_animation_index]
        self.image.set_colorkey((0,0,0))
        self.image = pygame.transform.scale(self.image,(50,50))
        self.start = time.time()

    def animation(self):
        if self.cooldown > 100 :
            self.current_animation_index += 1
            if self.current_animation_index == len(self.get_animation()):
                self.current_animation_index = 0
            self.cooldown = 0


class Cobra(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.sprite_sheet = SpriteSheet("Cobra.png")
        self.sprite_sheet.load_images("idle",numbers = 8, row = 0)
        self.sprite_sheet.load_images("attack",numbers = 6, row = 2)
        self.current_animation = "idle"
        self.image = self.sprite_sheet.get_images("idle")[0]
        self.rect= self.image.get_rect()
        self.position = [x,y]
        self.old_position = self.position
        self.current_animation_index = 0
        self.cooldown = 0

    def update(self):
        self.rect.topleft=self.position
        self.animation()
        self.image=self.get_animation()[self.current_animation_index]
        self.image.set_colorkey((0,0,0))
        self.image = pygame.transform.scale(self.image,(50,50))
        self.start = time.time()

    def get_animation(self):
        return self.sprite_sheet.get_images(self.current_animation)

    def animation(self):
        if self.cooldown > 100 :
            self.current_animation_index += 1
            if self.current_animation_index == len(self.get_animation()):
                self.current_animation_index = 0
            self.cooldown = 0
    def change_animation(self,name):
        self.current_animation = name



class Game:
    def __init__(self):
        self.screen=pygame.display.set_mode((1080,720))
        pygame.display.set_caption("Hero Quest")


        # chargement de la carte
        tmx_data = pytmx.util_pygame.load_pygame("map jeu.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer=pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        # chargement du groupe avec la map
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer , default_layer = 1)

        #récupération de la position du spawn du joueur
        self.spawn_point = tmx_data.get_object_by_name("player_spawn")
        self.spawn_point_bis = tmx_data.get_object_by_name("spawn_2")
        self.sortie = tmx_data.get_object_by_name("player_spawn2")

        #chargement du joueur
        self.player=Player(self.spawn_point.x,self.spawn_point.y)
        self.group.add(self.player)

        #Zoom de la map
        map_layer.zoom = 2.5
        #chargement de toutes les collisions
        self.walls = []
        self.void = []
        self.exit = []
        self.exit2 = []
        #group des monstres
        self.monster = pygame.sprite.Group()
        for obj in tmx_data.objects:
            if obj.name == "collision" :
                self.walls.append(pygame.rect.Rect(obj.x,obj.y,obj.width,obj.height))
        for obj in tmx_data.objects:
            if obj.name == "void" :
                self.void.append(pygame.rect.Rect(obj.x,obj.y,obj.width,obj.height))
        for obj in tmx_data.objects:
            if obj.name == "exit" :
                self.exit.append(pygame.rect.Rect(obj.x,obj.y,obj.width,obj.height))
        for obj in tmx_data.objects:
            if obj.name == "exit2" :
                self.exit2.append(pygame.rect.Rect(obj.x,obj.y,obj.width,obj.height))
        for obj in tmx_data.objects:
            if obj.name == "ennemy" :
                cobra = Cobra(obj.x,obj.y)
                self.monster.add(cobra)
        for obj in tmx_data.objects:
            if obj.name == "pnj" :
                pnj=Pnj(obj.x, obj.y)
                self.monster.add(pnj)
        #chargement des monstres
        self.group.add(self.monster)

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if self.player.alive == True:
            if pressed[pygame.K_UP]:
                self.player.move_up()
                self.player.change_animation("run_r")
                self.player.last_view = "idle_r"
            elif pressed[pygame.K_DOWN]:
                self.player.move_down()
                self.player.change_animation("run_l")
                self.player.last_view = "idle_l"
            elif pressed[pygame.K_RIGHT]:
                self.player.move_right()
                self.player.change_animation("run_r")
                self.player.last_view = "idle_r"
            elif pressed[pygame.K_LEFT]:
                self.player.move_left()
                self.player.change_animation("run_l")
                self.player.last_view = "idle_l"
            elif pressed[pygame.K_0]:
                self.player.change_animation("attack_r")
                self.player.last_view = "idle_r"
            elif pressed[pygame.K_1]:
                self.player.change_animation("attack_l")
                self.player.last_view = "idle_l"
            elif pressed[pygame.K_f]:
                self.player.change_animation("fall_l")
                self.player.last_view = "idle_l"
            elif pressed[pygame.K_g]:
                self.player.change_animation("fall_r")
                self.player.last_view = "idle_r"
            else:
                self.player.change_animation(self.player.last_view)





    def update(self):
        self.group.update()

        # vérifie la collision avec un mur
        for sprite in self.group.sprites():
            if self.player.feet.collidelist(self.walls) >-1:
                # le joueur revient juste en arrière
                self.player.move_back()
                self.player.change_animation("hit")
                #vérifie la collision avec un trou
            if self.player.feet.collidelist(self.void) >-1:
                # renvoie le joueur au point de spawn
                self.player.change_animation("fall_l")
                self.player.fall_instance = True
                self.player.fall([self.spawn_point.x,self.spawn_point.y])
                self.player.fall_instance = False
                self.player.last_view = "idle_l"
                self.player.life -= round(1/17,3)
                print("Vous êtes tombés et il vous reste",self.player.life,"vie")
                #vérifie si la collision entre le joueur et la sortie dans la grotte
            if self.player.feet.collidelist(self.exit) >-1:
                self.player.teleportation([self.spawn_point_bis.x,self.spawn_point_bis.y])
                print("en cours de développement")
                #vérifie la collision entre le joueur et la sortie dans la forêt
            if self.player.feet.collidelist(self.exit2) >-1:
                self.player.teleportation([self.sortie.x,self.sortie.y])
                print("en cours de développement")






    def run(self):
        running = True
        clock = pygame.time.Clock()
        song = pygame.mixer.Sound("musique _ambiance.ogg")
        song.set_volume(0.008)
        while running:
            #actualisation de la carte
            self.player.save_location()
            self.handle_input()
           # self.release_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)

            self.player.cooldown += clock.get_time()
            for monster in self.monster:
                monster.cooldown += clock.get_time()
            if self.player.life <= 0 :
                self.player.change_animation("death")
                self.player.alive = False
            #actualisation de l'écran
            pygame.display.flip()
            song.play()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False



            clock.tick(60)
        pygame.quit()

if __name__ == '__main__':
    pygame.init()
    game= Game()
    game.run()