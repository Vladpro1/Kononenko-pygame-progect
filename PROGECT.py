import pygame
import random

BLACK = (0, 0, 0)
BLUE = (29, 32, 76)
WHITE = (255, 255, 255)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, im='hero.png'):

        super().__init__()

        self.image = pygame.image.load(im).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


        self.change_x = 0
        self.change_y = 0
        self.walls = None


        self.coins = None
        self.collected_coins = 0


        self.enemies = pygame.sprite.Group()
        self.alive = True


    def update(self):
        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:

            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:

                self.rect.left =  block.rect.right



                self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:

            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom


                coins_hit_list = pygame.sprite.spritecollide(self, self.coins, False)
                for coin in coins_hit_list:
                    self.collected_coins
                    coin.kill()



                    if pygame.sprite.spritecollide(self, self.enemies, False):
                        self.alive = False

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, im="coin.png"):
        super().__init__()

        self.image = pygame.image.load(im).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y




class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, im='pumpkin.png'):
        super().__init__()

        self.image = pygame.image.load(im).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #Злая тыква должна ходить туда(start) и обратно(stop)
        self.start = x
        self.stop = x + random.randint(180, 240)
        self.direction = 1

    def update(self):
        #тыква дошла до stop, поворот обратно(налево), значение direction = -1
        if self.rect.x >= self.stop:
            self.rect.x = self.stop
            self.direction = -1
        #тыква долшла до start, поворот обратно(направо), значение direction = 1
        if self.rect.x <= self.start:
            self.rect.x = self.start
            self.direction = 1

        self.rect.x += self.direction * 2


pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('ПРОДВИНУТЫЙ ЛАБИРИНТ')


all_sprite_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()

wall_coords = [
    [0, 0, 10, 600],
    [790, 0, 10, 600],
    [10, 0, 790, 10],
    [0, 200, 100, 10],
    [0, 590, 600, 10],
    [450, 400, 10, 200],
    [550, 450, 250, 10]
]
for coord in wall_coords:
    wall = Wall(coord[0], coord[1], coord[2], coord[3])
    wall_list.add(wall)
    all_sprite_list.add(wall)




coins_list = pygame.sprite.Group()
coins_coord = [[100, 140], [236, 50], [400, 234]]

for coord in coins_coord:
    coin = Coin(coord[0], coord[1])
    coins_list.add(coin)
    all_sprite_list.add(coin)



enemies_list = pygame.sprite.Group()
enemies_coord = [[10, 500], [400, 50]]
for coord in enemies_coord:
    enemy = Enemy(coord[0], coord[1])
    enemies_list.add(enemy)
    all_sprite_list.add(enemy)



player = Player(50, 50)
player.walls = wall_list
all_sprite_list.add(player)


player.coins = coins_list


player.enemies = enemies_list



