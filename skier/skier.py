import json
import random

import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL,
    K_4, K_1, K_2, K_3, K_5)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600


# Powerups: 1 - p1: X Small (Makes player small for 2 seconds)
# 2 - p2: X Evasion (Makes player faster for 2 seconds)
# 3 - p3: X Scarce (Makes trees appear slowly for 2 seconds)
# 4 - p4: X Clear (Immediately clears all trees on screen)
# 5 - p5: X Ghost (Allows user to pass through trees for 5 seconds)
# Mode-c 1: (Reverses mode for 10 seconds;
# player gets more points for hitting trees, and loses points for each tree not hit)

class Skier(pygame.sprite.Sprite):
    speedFactor = 1

    def __init__(self):
        super(Skier, self).__init__()
        self.surface = pygame.image.load("skier.jpg").convert()
        self.surface = pygame.transform.scale(self.surface, (50, 50))
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.surface.set_alpha(255)
        self.rect = self.surface.get_rect()

    def update(self, pressed):
        if pressed[K_UP]:
            self.rect.move_ip(0, -self.speedFactor)
        if pressed[K_DOWN]:
            self.rect.move_ip(0, self.speedFactor)
        if pressed[K_LEFT]:
            self.rect.move_ip(-self.speedFactor, 0)
        if pressed[K_RIGHT]:
            self.rect.move_ip(self.speedFactor, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def p1(self):
        w, h = self.surface.get_size()
        self.surface = pygame.transform.scale(self.surface, (int(w / 2), int(h / 2)))
        self.rect.w = self.rect.w / 2
        self.rect.h = self.rect.h / 2
        pygame.time.set_timer(BIG, 2000, True)

    def revp1(self):
        self.surface = pygame.transform.scale2x(self.surface)
        self.rect.w = self.rect.w * 2
        self.rect.h = self.rect.h * 2

    def p2(self):
        self.speedFactor += 1
        pygame.time.set_timer(SLOW, 2000, True)

    def revp2(self):
        self.speedFactor -= 1


class Tree(pygame.sprite.Sprite):
    def __init__(self):
        super(Tree, self).__init__()
        self.surface = pygame.image.load("tree.png").convert()
        self.surface = pygame.transform.scale(self.surface, (50, 50))
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surface.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                SCREEN_HEIGHT,
            )
        )
        self.speed = random.randint(1, 1)

    def update(self):
        self.rect.move_ip(0, -1)
        if self.rect.bottom < 0:
            self.kill()


def start():
    font = pygame.font.Font("/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf", 32)
    for i in range(3, 0, -1):
        screen.fill((0, 0, 0))
        text = font.render("Game starts in: " + i.__str__(), True, (0, 255, 0))
        t_rect = text.get_rect()
        t_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        screen.blit(text, t_rect)
        pygame.display.flip()
        pygame.time.delay(1000)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
accounts = json.load(open("accounts.json"))
account = "apoorv"
accountData = accounts["accounts"][account]
if accountData["tester"]:
    testmode = True
else:
    testmode = False
    print("Current powerups: " + accountData["powerups"].__str__())
start()

BIG = pygame.USEREVENT + 2
NEWTREE = pygame.USEREVENT + 1
SLOW = pygame.USEREVENT + 3
MORETREES = pygame.USEREVENT + 4
SOLIDIFY = pygame.USEREVENT + 5

mode = "ultra hard"
speeds = {
    "easy": 500,
    "normal": 400,
    "hard": 300,
    "very hard": 250,
    "super hard": 200,
    "ultra hard": 150
}
newTreeTime = speeds[mode]
pygame.time.set_timer(NEWTREE, newTreeTime)

skier = Skier()
score = 0

obstacles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(skier)
ghost = False

running = True
while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_1:
                if testmode or accountData["powerups"]["p1"] > 0:
                    skier.p1()
                    accountData["powerups"]["p1"] -= 1
            elif event.key == K_2:
                if testmode or accountData["powerups"]["p2"] > 0:
                    skier.p2()
                    accountData["powerups"]["p2"] -= 1
            elif event.key == K_3:
                if testmode or accountData["powerups"]["p3"] > 0:
                    newTreeTime = newTreeTime + 250
                    pygame.time.set_timer(MORETREES, 2000)
                    pygame.time.set_timer(NEWTREE, 0)
                    pygame.time.set_timer(NEWTREE, newTreeTime)
                    accountData["powerups"]["p3"] -= 1
            elif event.key == K_4:
                if testmode or accountData["powerups"]["p4"] > 0:
                    for sprite in obstacles:
                        sprite.kill()
                    accountData["powerups"]["p4"] -= 1
            elif event.key == K_5:
                if testmode or accountData["powerups"]["p5"] > 0:
                    ghost = True
                    skier.surface.set_alpha(128)
                    pygame.time.set_timer(SOLIDIFY, 5000, True)
                    accountData["powerups"]["p5"] -= 1
        elif event.type == QUIT:
            running = False
        elif event.type == NEWTREE:
            tree = Tree()
            all_sprites.add(tree)
            obstacles.add(tree)
        elif event.type == BIG:
            skier.revp1()
        elif event.type == SLOW:
            skier.revp2()
        elif event.type == MORETREES:
            newTreeTime = newTreeTime - 250
            pygame.time.set_timer(NEWTREE, 0)
            pygame.time.set_timer(NEWTREE, newTreeTime)
            print(newTreeTime)
        elif event.type == SOLIDIFY:
            skier.surface.set_alpha(255)
            ghost = False
    keys = pygame.key.get_pressed()
    skier.update(keys)
    obstacles.update()
    screen.fill((249, 246, 239))
    for sprite in all_sprites:
        screen.blit(sprite.surface, sprite.rect)
    if not ghost and pygame.sprite.spritecollideany(skier, obstacles):
        skier.kill()
        print("Your score is: " + score.__str__())
        print("Played by: " + account)
        if not testmode:
            highscores = json.load(open("highScores.json"))
            if score > highscores["highscores"][mode]["score"]:
                print("NEW HIGHSCORE ON MODE " + mode.upper() + "!!")
                highscores["highscores"][mode]["score"] = score
                highscores["highscores"][mode]["accountName"] = account
            else:
                print("Highscore: " + highscores["highscores"][mode]["score"].__str__() + "\nHighscore made by: " +
                      highscores["highscores"][mode]["accountName"])
            json.dump(highscores, open("highScores.json", "w"))
            # give out powerups based on score
            accountData["powerups"]["p1"] = max(
                accountData["powerups"]["p1"] + round(score / 4000) + random.randint(-1, 2), 0)
            accountData["powerups"]["p2"] = max(
                accountData["powerups"]["p2"] + round(score / 3000) + random.randint(-2, 3), 0)
            accountData["powerups"]["p3"] = max(
                accountData["powerups"]["p3"] + round(score / 6000) + random.randint(0, 2), 0)
            accountData["powerups"]["p4"] = max(
                accountData["powerups"]["p4"] + round(score / 7000) + random.randint(0, 1), 0)
            accountData["powerups"]["p5"] = max(
                accountData["powerups"]["p5"] + round(score / 8000) + random.randint(0, 1), 0)
            print("New powerups: " + accountData["powerups"].__str__())
            accounts["accounts"][account] = accountData
            json.dump(accounts, open("accounts.json", "w"))
        running = False
    pygame.display.flip()
    score += 1
