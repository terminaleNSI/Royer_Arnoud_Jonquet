import pygame
import pytmx
import pyscroll
import time


class SpriteSheet():
    def __init__(self,name):
        self.sprite_sheet = pygame.image.load(name)
        self.images =dict()
        self.load_images("idle",numbers = 5)
        self.load_images("run",numbers = 8,row = 1)
        self.load_images("attack",numbers = 8,row = 2)



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
        self.image = self.sprite_sheet.get_images("idle")[0]
        self.rect= self.image.get_rect()
        self.position  = [x,y]
        self.feet = pygame.Rect(0,0,self.rect.width *0.5,12)
        self.current_animation = "idle"
        self.old_position = self.position
        self.current_animation_index = 0
        self.cooldown = 0
        self.speed=3

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
        self.position =spawn
    def attack(self):
        self.change_animation("attack")


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
        self.rect.topleft=self.position
        self.feet.midbottom = self.rect.midbottom
        self.animation()
        self.image=self.get_animation()[self.current_animation_index]
        self.image.set_colorkey((0,0,0))
        self.image = pygame.transform.scale(self.image,(50,50))
        self.start = time.time()




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

        #chargement du joueur
        self.player=Player(self.spawn_point.x,self.spawn_point.y)
        self.group.add(self.player)
        #Zoom de la map
        map_layer.zoom = 2.5
        #chargement de toutes les collisions
        self.walls = []
        self.void = []
        for obj in tmx_data.objects:
            if obj.name == "collision" :
                self.walls.append(pygame.rect.Rect(obj.x,obj.y,obj.width,obj.height))
        for obj in tmx_data.objects:
            if obj.name == "void" :
                self.void.append(pygame.rect.Rect(obj.x,obj.y,obj.width,obj.height))

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation("run")
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation("run")
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation("run")
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation("run")
        elif pressed[pygame.K_0]:
            self.player.attack()








    def update(self):
        self.group.update()

        # vérifie la collision
        for sprite in self.group.sprites():
            if self.player.feet.collidelist(self.walls) >-1:
                # le joueur revient juste en arrière
                self.player.move_back()
            if self.player.feet.collidelist(self.void) >-1:
                self.player.fall([self.spawn_point.x,self.spawn_point.y])





    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            #actualisation de la carte
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            #actualisation de l'écran
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


            self.player.cooldown += clock.get_time(     )
            clock.tick(60)
        pygame.quit()

if __name__ == '__main__':
    pygame.init()
    game= Game()
    game.run()
