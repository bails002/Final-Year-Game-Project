import pygame
import math
from tkinter import *
import random
import time
import sqlite3
import sys
from sqlite3 import Error
import pickle

#need to add shop and inventory stuff



# initialize pygame
pygame.init()
pygame.font.init()
myFont = pygame.font.SysFont('Comic Sans MS', 5)


# create screen
display_width = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))

# background
background = pygame.image.load('background.png')
title = pygame.image.load('game background4.png')

# title and icon
pygame.display.set_caption("adventure game")
icon = pygame.image.load('sword.png')
pygame.display.set_icon(icon)

# player

playerX = 370
playerY = 480


full_heart = pygame.image.load('full_heart.png').convert_alpha()
empty_heart = pygame.image.load('empty_heart.png').convert_alpha()
half_heart = pygame.image.load('half_heart.png').convert_alpha()

swordImg = pygame.image.load('sword.png')
swordX = playerX
swordY = playerY
swordX_change = 0
swordY_change = 2
sword_state = "ready"

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('elf.png').convert_alpha()
        self.rect = self.image.get_rect(center=(playerX, playerY))
        self.health = 10
        self.max_health = 10
        self.money = 100
        self.luck = 0
        self.weapon = swordImg

    def spawn(self, spawnx , spawny):
        screen.blit(self.image,(spawnx,spawny))

    def printhealth(self):
        global y
        y = self.health
        print(y)


    def resetplayer(self):
        global playerX
        global playerY
        playerX = 370
        playerY = 480
        self.max_health = 10
        self.health = self.max_health


    def get_damage(self):
        if self.health > 0:
            self.health -= 1
        elif self.health <= 0:
            screen.blit(gameover, (150, 125))
            pygame.display.update()
            time.sleep(5)
            player1.resetplayer()
            enemies[0].resetEnemy()
            intro()

    def get_health(self):
        if self.health < self.max_health:
            self.health += 2

    def full_hearts(self):
        for heart in range(self.health):
            screen.blit(full_heart, (heart * 50 + 10, 45))

    def empty_hearts(self):
        for heart in range(self.max_health):
            if heart < self.health:
                screen.blit(full_heart, (heart * 50 + 10, 5))
            else:
                screen.blit(empty_heart, (heart * 50 + 10, 5))

    def half_hearts(self):
        half_hearts_total = self.health / 2
        half_heart_exists = half_hearts_total - int(half_hearts_total) != 0

        for heart in range(int(self.max_health / 2)):
            if int(half_hearts_total) > heart:
                screen.blit(full_heart, (heart * 50 + 10, 5))
            elif half_heart_exists and int(half_hearts_total) == heart:
                screen.blit(half_heart, (heart * 50 + 10, 5))
            else:
                screen.blit(empty_heart, (heart * 50 + 10, 5))

    def increasemaxhealth(self):
        if self.max_health < 32:
            self.max_health += 2

    def update(self):
        self.half_hearts()

player1 = Player()

playerX_change = 0
playerY_change = 0



saveNumber = 1
Money = 100


def save(sx,sy):
    conn = sqlite3.connect('savedGames.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS savedGame 
                        (save int PRIMARY KEY,Money int)''')

    c.execute("INSERT OR IGNORE INTO savedGame VALUES (?, ?)",[sx,sy])

    conn.commit()


def checkSave():
    conn = sqlite3.connect('savedGames.db')
    c = conn.cursor()
    num = 0
    for row in c.execute("SELECT save FROM savedGame"):
        num += 1
        print (num)
    return num + 1



def useSave(num):
    conn = sqlite3.connect('savedGames.db')
    c = conn.cursor()
    for row in c.execute('''SELECT save FROM savedGame'''):
        testnum = "(",str(num),",)"
        textnum = "".join(testnum)

        if str(row) == str(textnum.strip()):
            c.execute("SELECT money FROM savedGame WHERE save = (?)",[num])
            hope = c.fetchone()
            print("success")
            return hope[0]

        else:
            print("something went wrong")



# conn.commit()
# conn.close()``````    Q

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('rhino.png')
        self.rect = self.image.get_rect(center=(20, 20))
        self.health = 5
        self.max_health = 5

    def spawn(self, spawnx , spawny):
        if enemyalive:
            screen.blit(self.image,(spawnx,spawny))

    def get_damage(self):
        if self.health > 0:
            self.health -= 1
        else:
            enemyofscreen()

    def get_health(self):
        if self.health < self.max_health:
            self.health += 5

    def displayenemyhealth(self):
        self.health

    def resetEnemy(self):
        global enemyX
        global enemyY
        global moveOrNot
        enemyX = 20
        enemyY = 10
        moveOrNot = 0.5
        self.health = 5
        enemyMovement(1)

e1 = Enemy()
# e2 =...
enemies = [e1]



# rhinoX = random.randint(0, 800)
# rhinoY = random.randint(50, 300)
enemyX = 10
enemyY = 20
enemyX_change = 0
enemyY_change = 0

iterations = 0

# crash_sound = pygame.mixer.Sound("crash.wav")
attack_sound = pygame.mixer.Sound("353708__samsterbirdies__sword-swings.wav")


def backmusic(m):

    pygame.mixer.music.load('261608__txirimiri__guitar-soundtrack.wav')
    if m == "on":
        # pygame.mixer.music.load('attack.wav')
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

def enemyMovement(speed):
    global iterations
    global enemyX_change
    global enemyY_change
    if iterations < 1:
        if (enemyX, enemyY) <= (320, 250):
            while enemyalive:

                enemyX_change = speed
                enemyY_change = 0
                if enemyX >= 150:
                    enemyX_change = 0
                    enemyY_change = speed  # works

                if enemyY >= 40:
                    enemyX_change = speed
                    enemyY_change = 0

                if enemyX >= 200:
                    enemyX_change = 0
                    enemyY_change = speed

                if enemyY >= 100:
                    enemyX_change = speed
                    enemyY_change = 0

                if enemyX == 320:
                    enemyX_change = 0
                    enemyY_change = speed

                print(enemyX, enemyY)
                break

        else:
            iterations = 5
    else:
        if enemyX == 320:
            enemyX_change = 0
            enemyY_change = -speed

        if enemyY <= 100:
            enemyX_change = -speed
            enemyY_change = 0

        if enemyX <= 200:
            enemyX_change = 0
            enemyY_change = -speed

        if enemyY <= 40:
            enemyX_change = -speed
            enemyY_change = 0

        if enemyX <= 150:
            enemyX_change = 0
            enemyY_change = -speed
        if enemyY == 5:
            enemyX_change = -speed
            enemyY_change = 0
        if (enemyX, enemyY) == (0, 5):
            iterations = 0


def use_sword(x, y):
    global sword_state
    sword_state = "use"
    screen.blit(swordImg, (x + 16, y + 10))


atx = playerX
aty = playerY
def attack():
    global atx, aty
    mx,my = pygame.mouse.get_pos()
    circle1 = pygame.draw.circle(screen,"blue",(atx,aty),30,0)
    circle2 = pygame.draw.circle(screen, "red", (mx, my), 50, 0)
    screen.blit(swordImg, (atx, aty))

    dx = mx - atx
    dy = my - aty

    angle = math.atan2(dx,dy)

    mvx = math.sin(angle) * 2 # increase number to increase speed
    mvy = math.cos(angle) * 2 #

    atx += mvx
    aty += mvy


class item:
    def __init__(self, ID, name, value, stock):
        self.ID = ID
        self.name = name
        self.value = value
        self.stock = stock


item1 = item(1, "health potion", 5, 10)
item2 = item(2, "heart",  5, 5)
items = [item1,item2] # contains items = item info

inventory = []
itemList = [] # will contain item buttons to interact with
def shop():
    def itemButton(itemName,y):
        item = button((0, 255, 0), 500, y, 100, 50, itemName)
        return item
    def shopWindow():

        moolaText = "Your Money:", str(player1.money)
        moola = " ".join(moolaText)

        #screen.fill((255, 255, 255))
        screen.blit(title, [0, 0]) # shop window background

        shopIcon.draw(screen, (255, 255, 255))

        exitButton.draw(screen, (0, 0, 0))

        yourMoney = button((0, 255, 0), 100, 100, 300, 50, moola)
        yourMoney.draw(screen, (0, 0, 0))
        if len(itemList) < len(items):
            for i in items:
                itemText = i.name, str(i.stock)
                itext = ":".join(itemText)
                shopitem = itemButton(itext, ((i.ID * 350) / 5 + 300))
                itemList.append(shopitem)
        else:
            #print ("cant do that!!!")
            itemList.clear()

        for z in itemList:
            z.draw(screen, (0, 0, 0))

    run = True



    shopIcon = button((255, 255, 255), 350, 150, 100, 50, 'Shop')
    exitButton = button((0, 255, 0), 125, 350, 100, 50, 'Exit')



    def affordToBuy(selected):
        price = selected.value
        numinstock = selected.stock
        if price <= player1.money:
            print("you can afford")
            if numinstock > 0:
                player1.money = player1.money - price
                selected.stock -= 1
                inventory.append(selected)

                print (inventory)
            else:
                print("there are none of these in stock")
        else:
            print("you cannot afford this")


    while run:

        shopWindow()
        pygame.display.update()

        for event in pygame.event.get():

            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            for j in range(0, len(itemList)):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exitButton.isOver(pos):
                        print("button clicked")
                        run = False

                    elif itemList[j].isOver(pos): #here we want the items to be added to inventory
                         affordToBuy(items[j])
                         # "items" and "itemList" should be the same length and should map 1:1.

                if event.type == pygame.MOUSEMOTION:
                    if exitButton.isOver(pos):
                        exitButton.color = (255, 0, 0)
                    elif itemList[j].isOver(pos):
                        itemList[j].color = (255, 0, 0)
                    else:
                        exitButton.color = (0, 255, 0)
                        itemList[j].color = (0, 255, 0)

def viewinventory():
    def which_invselected():
        print("At {0}".format(invselect.curselection()))
        return int(invselect.curselection()[0])

    def use_entry():
        selectedItem = inventory[which_invselected()]
        if  selectedItem.name== "health potion":
            player1.get_health()
            del inventory[which_invselected()]
            set_invselect()
        elif selectedItem.name == "heart":
            player1.increasemaxhealth()
            del inventory[which_invselected()]
            set_invselect()

    def make_window():
        global invselect
        win = Tk()
        win.title("Inventory")
        frame2 = Frame(win)  # Row of buttons
        b2 = Button(frame2, text="USE ITEM", command=use_entry)
        b2.pack(side=LEFT)
        L = Label(win, text=('money: $' + str(player1.money)))
        L.pack()
        frame4 = Frame(win)  # list of items in inventory
        scroll = Scrollbar(frame4, orient=VERTICAL)
        invselect = Listbox(frame4, yscrollcommand=scroll.set, height=6)
        scroll.config(command=invselect.yview)
        scroll.pack(side=RIGHT, fill=Y)
        invselect.pack(side=LEFT, fill=BOTH, expand=1)
        frame2.pack()
        frame4.pack()
        return win

    def set_invselect():
        #shoplist.sort(key=lambda record: record[1])
        invselect.delete(0, END)
        for item in inventory:
            invselect.insert(END, "{0}".format(item.name))
    win = make_window()
    set_invselect()
    win.mainloop()


def movement():
    global running
    global playerX_change
    global playerY_change
    global enemyX
    global enemyY
    global moveOrNot
    global atx,aty
    debug = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        # if any key is pressed check whether its left or right
        if event.type == pygame.KEYDOWN:
            print("a keystroke has been pressed")

            if event.key == pygame.K_LEFT:
                playerX_change = -1
                print("left arrow is pressed")

            if event.key == pygame.K_RIGHT:
                playerX_change = 1
                print("right arrow is pressed")

            if event.key == pygame.K_UP:
                playerY_change = -1
                print("up arrow is pressed")

            if event.key == pygame.K_DOWN:
                playerY_change = 1
                print("down arrow is pressed")

            if (event.key == pygame.K_f):
                swordX = playerX
                swordY = playerY
                atx = playerX
                aty = playerY
                attack()
                use_sword(swordX, swordY)

                print("f is pressed")

            if (event.key == pygame.K_ESCAPE):
                pause()

            if (event.key == pygame.K_TAB):
                viewinventory()

            if event.key == pygame.K_n:

                save(checkSave(),player1.money)

            if (event.key == pygame.K_p):
                debug = True
                time.sleep(1)

            while (debug == True):
                print("still running")
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        sys.exit()

                    # if any key is pressed check whether its left or right
                    if event.type == pygame.KEYDOWN:
                        print("a keystroke has been pressed")
                        if (event.key == pygame.K_t):
                            shop()

                        if event.key == pygame.K_w:
                            player1.increasemaxhealth()
                            player1.printhealth()

                        if event.key == pygame.K_s:
                            player1.get_damage()
                            player1.printhealth()

                        if event.key == pygame.K_e:
                            enemies[0].resetEnemy()

                        if event.key == pygame.K_y:
                            player1.printhealth()
                            sys.exit()

                        if (event.key == pygame.K_p):
                            debug = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                print("keystroke has been released")
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
                print("keystroke has been released")




def isCollision(enemyX, enemyY, swordX, swordY):
    distance = math.sqrt((math.pow(enemyX - swordX, 2)) + (math.pow(enemyY - swordY, 2)))
    if distance < 27:
        return True
    else:
        return False


def isInteract(enemyX, enemyY, swordX, swordY):
    distance = math.sqrt((math.pow(enemyX - swordX, 2)) + (math.pow(enemyY - swordY, 2)))
    if distance < 27:
        return True
    else:
        return False


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


# window = pygame.display.set_mode((500,500))
# window.fill((255,255,255))
class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


gameover = pygame.image.load('death screen.png')

def enemyofscreen():
    global moveOrNot
    global enemyX
    global enemyY
    enemyX = -200
    enemyY = -200
    moveOrNot = 0

enemy1 = pygame.sprite.GroupSingle(Enemy())
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(enemy1)
cont = True

def removefrom(place, x):
    for i in range(len(place)):

        if place[i] == x:
            place.remove(i)
            break
    return -1

def combat():
    global y
    root = Tk()
    root.title("attack box")
    root.iconbitmap()
    root.geometry("100x100")
    player1.printhealth()
    root.printhealth= y
    print(y)

    #myLabel = Label(root, text="" ).pack()
    def recievedmg():

        enemyhit = random.randint(0, 3)
        if enemyhit == 0:
            myLabel = Label(root, text="enemy has missed").pack()
        else:
            myLabel = Label(root, text="you have recieved 5 damage").pack()
            print (player1)
            player1.get_damage()

    def dodamage():
        enemies[0].get_damage()

    # top = Toplevel()
    def selected(event):
        global moveOrNot
        global ticks
        global enemyX
        global enemyY
        global enemyY_change
        global enemyX_change
        global enemyhealth
        # global root
        if clicked.get() == 'attack':
            myLabel = Label(root, text="enemy has been attacked").pack()
            dodamage()
            recievedmg()
            time.sleep(2)
            root.destroy()

        elif clicked.get() == 'emergency heal':
            player1.get_health()
            removefrom(inventory, "health potion")
            myLabel = Label(root, text="you have been healed for 5 points of health").pack()

        elif clicked.get() == 'run away':
            ticks = 0
            myLabel = Label(root, text="you can now run away").pack()
            root.destroy()
            main(1000)

        else:
            myLabel = Label(root, text=clicked.get()).pack()
        # time.sleep(5)

    Options = [
        "nothing",
        "attack",
        "emergency heal",
        "run away"
    ]  # etc

    clicked = StringVar()
    clicked.set(Options[0])
    enemy1.sprite.displayenemyhealth()
    label = Label(root, text="COMBAT").pack()
    drop = OptionMenu(root, clicked, *Options, command=selected)
    drop.pack(pady=20)

    root.mainloop()
    main(5)

optionsMenuTitle = button((255, 255, 255), 350, 150, 100, 50, 'options')
soundButton = button((255, 0, 0), 125, 350, 100, 50, 'sound')
backButton = button((0, 255, 0), 575, 350, 100, 50, 'back')

def options():
    onoff = 1
    run = True

    def optionsWindow():
        screen.fill((255, 255, 255))
        screen.blit(title, [0, 0])
        optionsMenuTitle.draw(screen, (255, 255, 255))
        soundButton.draw(screen, (0, 0, 0))
        backButton.draw(screen, (0, 0, 0))

    while run:
        optionsWindow()
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if soundButton.isOver(pos):
                    print("button clicked")
                    if onoff == 1:
                        backmusic("on")
                        onoff -= 1
                        soundButton.color = (0, 255, 0)
                    elif onoff == 0:
                        backmusic("off")
                        onoff += 1
                        soundButton.color = (255, 0, 0)

                elif backButton.isOver(pos):
                    run = False
            if event.type == pygame.MOUSEMOTION:
                if backButton.isOver(pos):
                    backButton.color = (255, 0, 0)
                else:
                    backButton.color = (0, 255, 0)


def intro():
    def introWindow():
        screen.fill((255, 255, 255))
        screen.blit(title, [0, 0])
        nameofgame.draw(screen, (255, 255, 255))
        playButton.draw(screen, (0, 0, 0))
        quitButton.draw(screen, (0, 0, 0))
        optionsButton.draw(screen, (0, 0, 0))
        loadButton.draw(screen, (0, 0, 0))
    #loadsave = input("Load Save:")
    #player1.money = useSave(loadsave) # number here decides what save is chosen


    run = True
    nameofgame = button((255, 255, 255), 270, 150, 300, 50, 'Final Year Project')
    playButton = button((0, 255, 0), 50, 350, 200, 50, 'New Game')
    quitButton = button((0, 255, 0), 650, 350, 100, 50, 'Quit')
    optionsButton = button((0, 255, 0), 300, 350, 120, 50, 'Options')
    loadButton = button((0, 255, 0), 460, 350, 160, 50, 'Load Game')
    while run:
        introWindow()
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.isOver(pos):
                    print("button clicked")
                    run = False
                elif quitButton.isOver(pos):
                    run = False
                    pygame.quit()
                    quit()
                elif optionsButton.isOver(pos):
                    options()
                elif loadButton.isOver(pos):
                    loadsave = input("Load Save:")
                    player1.money = useSave(loadsave)
                    run = False # number here decides what save is chosen

            if event.type == pygame.MOUSEMOTION:
                if playButton.isOver(pos):
                    playButton.color = (255, 0, 0)
                elif quitButton.isOver(pos):
                    quitButton.color = (255, 0, 0)
                elif optionsButton.isOver(pos):
                    optionsButton.color = (255, 0, 0)
                elif loadButton.isOver(pos):
                    loadButton.color = (255, 0, 0)
                else:
                    playButton.color = (0, 255, 0)
                    quitButton.color = (0, 255, 0)
                    optionsButton.color = (0, 255, 0)
                    loadButton.color = (0, 255, 0)


def pause():

    def pauseWindow():
        screen.fill((255, 255, 255))
        screen.blit(title, [0, 0])
        gamePaused.draw(screen, (255, 255, 255))
        returnButton.draw(screen, (0, 0, 0))
        quitButton.draw(screen, (0, 0, 0))
        optionsButton.draw(screen, (0, 0, 0))

    run = True
    gamePaused = button((255, 255, 255), 420, 150, 0, 0, 'Game Paused')
    returnButton = button((0, 255, 0), 125, 350, 100, 50, 'Return')
    quitButton = button((0, 255, 0), 460, 350, 200, 50, 'Save & Quit')
    optionsButton = button((0, 255, 0), 270, 350, 120, 50, 'Options')

    while run:
        pauseWindow()
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if returnButton.isOver(pos):
                    print("button clicked")
                    run = False
                elif quitButton.isOver(pos):
                    save(checkSave(), player1.money)
                    run = False

                    print ("your latest save number:",checkSave()-1)
                    pygame.quit()
                    quit()
                elif optionsButton.isOver(pos):
                    options()

            if event.type == pygame.MOUSEMOTION:
                if returnButton.isOver(pos):
                    returnButton.color = (255, 0, 0)
                elif quitButton.isOver(pos):
                    quitButton.color = (255, 0, 0)
                elif optionsButton.isOver(pos):
                    optionsButton.color = (255, 0, 0)
                else:
                    returnButton.color = (0, 255, 0)
                    quitButton.color = (0, 255, 0)
                    optionsButton.color = (0, 255, 0)


# startScreen()
enemyalive = True

start = 0
#ticks = 1000
moveOrNot = 0.5

x=100
y=100

def main(maxtick):
    global incombat
    running = True
    incombat = True
    ticks = 0

    checkSave()


    while running:
        ticks = ticks + 1
        print(ticks)

        # background image
        screen.blit(background, (0, 0))
        movement()
        attack() # set bounds for this then work this new sword into existing framework

        player1.update()
        enemy1.update()

        # player boundary
        global playerY, sword_state
        global playerX
        global enemyY
        global enemyX
        playerY += playerY_change
        playerX += playerX_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736
        if playerY <= 5:
            playerY = 5
        elif playerY >= 530:
            playerY = 530

        enemyMovement(moveOrNot)

        # enemy boundary

        global swordY
        global swordX
        enemyY += enemyY_change
        enemyX += enemyX_change

        if swordY <= playerY - 50:
            swordX = int(playerX)
            swordY = int(playerY)
            sword_state = "ready"

        if swordY >= playerY + 50:
            swordX = int(playerX)
            swordY = int(playerY)
            sword_state = "ready"

        if swordX <= playerX - 50:
            swordX = int(playerX)
            swordY = playerY
            sword_state = "ready"

        if swordX >= playerX + 50:
            swordX = playerX
            swordY = playerY
            sword_state = "ready"

        # using sword in different directions
        if (sword_state == "use") and (playerY_change == -1):
            use_sword(swordX, swordY)
            swordX = playerX
            swordY -= swordY_change

        if (sword_state == "use") and (playerY_change == 1):
            use_sword(swordX, swordY)
            swordX = playerX
            swordY += swordY_change

        if (sword_state == "use") and (playerX_change == -1):
            use_sword(swordX, swordY)
            swordY = playerY
            swordX -= swordX_change

        if (sword_state == "use") and (playerX_change == 1):
            use_sword(swordX, swordY)
            swordY = playerY
            swordX += swordX_change

        collision = isCollision(enemyX, enemyY, swordX, swordY)

        if ticks < maxtick:
            incombat = False
        elif ticks > maxtick:
            incombat = True

        if incombat and collision:
            sword_state = ""
            # pygame.mixer.Sound.play(attack_sound)
            print("collision has occurred")
            while incombat:
                combat()
                time.sleep(1)
                main(1)

        player1.spawn(playerX, playerY)
        enemies[0].spawn(enemyX, enemyY)
        pygame.display.update()

save(1,100)
intro()
main(1000)
