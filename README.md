import pygame
import math
from tkinter import *
import random
import time
import sqlite3
import sys
from sqlite3 import Error
import pickle

# initialize pygame
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 5)
display_width = 800
display_height = 600
# create screen
screen = pygame.display.set_mode((display_width, display_height))
# background
background = pygame.image.load('background.png')
title = pygame.image.load('game background4.png')

# title and icon
pygame.display.set_caption("adventure game")
icon = pygame.image.load('sword.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('elf.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

swordImg = pygame.image.load('sword.png')
swordX = playerX
swordY = playerY
swordX_change = 0
swordY_change = 2
sword_state = "ready"


# conn = sqlite3.connect('shoptrial5.db')
# c = conn.cursor()
# c.execute('''CREATE TABLE shop (item text, level real, pwr real, price real)''')
# c.execute("INSERT INTO shop VALUES ('sword1', 1, 10, 10)")
# conn.commit()
# conn.close()``````    Q

class enemy:
    def __init__(self, number, level, name, image):
        self.number = number
        self.level = level
        self.name = name
        self.image = image


e1 = enemy(1, 1, "rhino", 'rhino.png')
# e2 =...
enemies = [e1]


class playerchar:
    def __init__(self, level, name, image):
        self.level = level
        self.name = name
        self.image = image


plyrlvl = 1
plyrname = ("USERINPUT")

playerobj = playerchar(plyrlvl, plyrname, 'elf.png')


class item:
    def __init__(self, ID, name, addhealth, healing, attackpower, expadd, value):
        self.ID = ID
        self.name = name
        self.addhealth = addhealth
        self.healing = healing
        self.attackpower = attackpower
        self.expadd = expadd
        self.value = value


item1 = item(1, "health potion", 0, 100, 0, 0, 5)
item2 = item(2, "large sword", 0, 100, 0, 0, 5)
items = [item1]

enemyImg = pygame.image.load(enemies[0].image)
# rhinoX = random.randint(0, 800)
# rhinoY = random.randint(50, 300)
enemyX = (10)
enemyY = (20)
enemyX_change = 0
enemyY_change = 0

iterations = 0

# crash_sound = pygame.mixer.Sound("crash.wav")
attack_sound = pygame.mixer.Sound("353708__samsterbirdies__sword-swings.wav")


def backmusic(m):
    #pygame.mixer.music.load('261608__txirimiri__guitar-soundtrack.wav')
    pygame.mixer.music.load('261608__txirimiri__guitar-soundtrack.wav')
    if m == "on":
        # pygame.mixer.music.load('attack.wav')
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    if enemyalive:
        screen.blit(enemyImg, (x, y))
    # else:


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


money = 117

shoplist = [['health potion', '4', '10'],
            ['large sword', '20', '2'],
            ['heart', '6', '5'],
            ['luck potion', '10', '11']]

inventory = []


def shop():
    def which_selected():
        print("At {0}".format(select.curselection()))
        return int(select.curselection()[0])

    def which_invselected():
        print("At {0}".format(invselect.curselection()))
        return int(invselect.curselection()[0])

    def affordToBuy():
        global money
        price = int(costvar.get())
        numinstock = int(stockvar.get())
        if price <= money:
            print("you can afford")
            if numinstock > 0:

                money = money - price
                add_entry()
            else:
                print("there are none of these in stock")
        else:
            print("you cannot afford this")

    def add_entry():
        inventory.append([itemvar.get(), costvar.get(), stockvar.get()])
        set_invselect()

    def delete_entry():
        del inventory[which_invselected()]
        set_invselect()

    def load_entry():
        item, cost, stock = shoplist[which_selected()]
        itemvar.set(item)
        costvar.set(cost)
        stockvar.set(stock)

    def make_window():
        global itemvar, costvar, stockvar, select, invselect, money
        win = Tk()
        win.title("shop")

        def moneycalc():
            global money
            affordToBuy()
            win.money = money
            L['text'] = 'money: $' + str(win.money)

        frame1 = Frame(win)

        Label(frame1, text="Item Name").grid(row=0, column=0, sticky=W)
        itemvar = StringVar()
        item = Entry(frame1, textvariable=itemvar)
        item.grid(row=0, column=1, sticky=W)

        Label(frame1, text="Cost").grid(row=1, column=0, sticky=W)
        costvar = IntVar()
        cost = Entry(frame1, textvariable=costvar)
        cost.grid(row=1, column=1, sticky=W)

        Label(frame1, text="Stock").grid(row=2, column=0, sticky=W)
        stockvar = IntVar()
        stock = Entry(frame1, textvariable=stockvar)
        stock.grid(row=2, column=1, sticky=W)

        # .grid(row=3, column=0, sticky=W)

        frame2 = Frame(win)  # Row of buttons

        b1 = Button(frame2, text=" Purchase  ", command=moneycalc)
        b2 = Button(frame2, text="Delete", command=delete_entry)
        b3 = Button(frame2, text="View Item", command=load_entry)
        b4 = Button(frame2, text="Refresh", command=set_select)
        b1.pack(side=LEFT)
        b2.pack(side=LEFT)
        b3.pack(side=LEFT)
        b4.pack(side=LEFT)
        L = Label(win, text=('money: $' + str(money)))
        L.pack()

        frame3 = Frame(win)  # list of items in shop

        scroll = Scrollbar(frame3, orient=VERTICAL)
        select = Listbox(frame3, yscrollcommand=scroll.set, height=6)
        scroll.config(command=select.yview)
        scroll.pack(side=RIGHT, fill=Y)
        select.pack(side=LEFT, fill=BOTH, expand=1)

        frame4 = Frame(win)  # list of items in inventory

        scroll = Scrollbar(frame4, orient=VERTICAL)
        invselect = Listbox(frame4, yscrollcommand=scroll.set, height=6)
        scroll.config(command=invselect.yview)
        scroll.pack(side=RIGHT, fill=Y)
        invselect.pack(side=LEFT, fill=BOTH, expand=1)

        frame3.pack()
        frame2.pack()
        frame1.pack()
        frame4.pack()

        return win

    def set_select():
        shoplist.sort(key=lambda record: record[1])
        select.delete(0, END)
        for item, cost, stock in shoplist:
            select.insert(END, "{0}, {1}{2}".format(item, "$", cost))

    def set_invselect():
        shoplist.sort(key=lambda record: record[1])
        invselect.delete(0, END)
        for item, cost, stock in inventory:
            invselect.insert(END, "{0}, {1}{2}".format(item, "$", cost))

    win = make_window()
    set_select()
    set_invselect()
    win.mainloop()


def viewinventory():
    def which_invselected():
        print("At {0}".format(invselect.curselection()))
        return int(invselect.curselection()[0])

    def use_entry():
        item, cost, stock = inventory[which_invselected()]
        itemvar.set(item)
        costvar.set(cost)
        stockvar.set(stock)
        if itemvar.get() == "health potion":
            player1.sprite.get_health()
            del inventory[which_invselected()]
            set_invselect()
        elif itemvar.get() == "heart":
            player1.sprite.increasemaxhealth()
            del inventory[which_invselected()]
            set_invselect()

    def make_window():
        global itemvar, costvar, stockvar, select, invselect, money
        win = Tk()
        win.title("inventory")

        # .grid(row=3, column=0, sticky=W)

        frame2 = Frame(win)  # Row of buttons

        b2 = Button(frame2, text="USE ITEM", command=use_entry)

        b2.pack(side=LEFT)

        L = Label(win, text=('money: $' + str(money)))
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
        shoplist.sort(key=lambda record: record[1])
        invselect.delete(0, END)
        for item, cost, stock in inventory:
            invselect.insert(END, "{0}, {1}{2}".format(item, "$", cost))

    win = make_window()

    set_invselect()
    win.mainloop()


# def savegame():


def savemoney():
    global money
    money = "1111"
    gold = sqlite3.connect('money.db')
    cursor = gold.cursor()
    cursor.execute('''CREATE TABLE earnings (money int)''')

    makemoneyrecord = ("""INSERT INTO earnings
                              VALUES 
                             (?)""", money)
    cursor.execute(makemoneyrecord)
    gold.commit()
    cursor.close()
    gold.close()
    
def spawnenemy():
    global enemyX
    global enemyY
    global moveOrNot
    enemyX = 20
    enemyY = 10
    moveOrNot = 0.5
    enemyMovement(1)

def movement():
    global running
    global playerX_change
    global playerY_change
    global enemyX
    global enemyY
    global moveOrNot

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
                use_sword(swordX, swordY)
                print("f is pressed")

            if (event.key == pygame.K_TAB):
                pause()

            if event.key == pygame.K_w:
                player1.sprite.increasemaxhealth()
            if event.key == pygame.K_s:
                player1.sprite.get_damage()
            if event.key == pygame.K_n:
                savemoney()
            if event.key == pygame.K_e:
                spawnenemy()
            if event.key == pygame.K_y:
                player1.sprite.printhealth()
                sys.exit()

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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('elf.png').convert_alpha()
        self.rect = self.image.get_rect(center=(400, 400))
        self.health = 10
        self.max_health = 10
        self.luck = 0

    def printhealth(self):
        global y
        y=self.health
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
            player1.sprite.resetplayer()
            spawnenemy()
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


full_heart = pygame.image.load('full_heart.png').convert_alpha()
empty_heart = pygame.image.load('empty_heart.png').convert_alpha()
half_heart = pygame.image.load('half_heart.png').convert_alpha()

player1 = pygame.sprite.GroupSingle(Player())


def enemyofscreen():
    global moveOrNot
    global enemyX
    global enemyY
    enemyX = -200
    enemyY = -200
    moveOrNot = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('rhino.png').convert_alpha()
        self.rect = self.image.get_rect(center=(20, 20))
        self.health = 5
        self.max_health = 5

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
    player1.sprite.printhealth()
    root.printhealth= y
    print(y)


    #myLabel = Label(root, text="" ).pack()
    def recievedmg():

        enemyhit = random.randint(0, 3)
        if enemyhit == 0:
            myLabel = Label(root, text="enemy has missed").pack()
        else:
            myLabel = Label(root, text="you have recieved 5 damage").pack()
            Y['text'] = 'health remaining:' + str(root.printhealth)
            player1.sprite.get_damage()



    def dodamage():
        enemy1.sprite.get_damage()

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
            player1.sprite.get_health()
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


def redrawWindow2():
    screen.fill((255, 255, 255))
    screen.blit(title, [0, 0])
    optionsMenuTitle.draw(screen, (255, 255, 255))
    soundButton.draw(screen, (0, 0, 0))
    backButton.draw(screen, (0, 0, 0))


optionsMenuTitle = button((255, 255, 255), 350, 150, 100, 50, 'options')
soundButton = button((255, 0, 0), 125, 350, 100, 50, 'sound')
backButton = button((0, 255, 0), 575, 350, 100, 50, 'back')


def options():
    onoff = 1
    ruun = True
    while ruun:
        redrawWindow2()
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
                    ruun = False
            if event.type == pygame.MOUSEMOTION:
                if backButton.isOver(pos):
                    backButton.color = (255, 0, 0)
                else:
                    backButton.color = (0, 255, 0)


def intro():
    def redrawWindow():
        screen.fill((255, 255, 255))
        screen.blit(title, [0, 0])
        nameofgame.draw(screen, (255, 255, 255))
        playButton.draw(screen, (0, 0, 0))
        quitButton.draw(screen, (0, 0, 0))
        optionsButton.draw(screen, (0, 0, 0))

    run = True
    nameofgame = button((255, 255, 255), 350, 150, 100, 50, 'game')
    playButton = button((0, 255, 0), 575, 350, 100, 50, 'play')
    quitButton = button((0, 255, 0), 125, 350, 100, 50, 'quit')
    optionsButton = button((0, 255, 0), 350, 350, 100, 50, 'options')

    while run:
        redrawWindow()
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

            if event.type == pygame.MOUSEMOTION:
                if playButton.isOver(pos):
                    playButton.color = (255, 0, 0)
                elif quitButton.isOver(pos):
                    quitButton.color = (255, 0, 0)
                elif optionsButton.isOver(pos):
                    optionsButton.color = (255, 0, 0)
                else:
                    playButton.color = (0, 255, 0)
                    quitButton.color = (0, 255, 0)
                    optionsButton.color = (0, 255, 0)


def pause():
    root = Tk()
    root.title("game paused")
    root.iconbitmap()
    root.geometry("250x150")

    def selected(event):

        if clicked.get() == 'Shop':
            myLabel = Label(root, text="you have opened the shop").pack()
            shop()
        elif clicked.get() == 'Options':
            options()
            main(1000)
        elif clicked.get() == 'Inventory':
            myLabel = Label(root, text="you have accessed your inventory").pack()
            viewinventory()
        elif clicked.get() == 'Main menu':
            intro()
            main(1000)
            myLabel = Label(root, text="close pause menu to access main menu").pack()


        else:
            myLabel = Label(root, text=clicked.get()).pack()

    Options = [
        "Shop",
        "Inventory",
        "Main menu",
        "Options"
    ]  # etc

    clicked = StringVar()
    clicked.set(Options[0])

    drop = OptionMenu(root, clicked, *Options, command=selected)
    drop.pack(pady=20)

    root.mainloop()


# startScreen()
enemyalive = True

start = 0
ticks = 1000
moveOrNot = 0.5


def main(maxtick):
    global incombat
    running = True
    incombat = True
    ticks = 0
    while running:
        ticks = ticks + 1
        print(ticks)

        # background image
        screen.blit(background, (0, 0))
        movement()

        # player1.draw(screen)
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
        if (sword_state is "use") and (playerY_change == -1):
            use_sword(swordX, swordY)
            swordX = playerX
            swordY -= swordY_change

        if (sword_state is "use") and (playerY_change == 1):
            use_sword(swordX, swordY)
            swordX = playerX
            swordY += swordY_change

        if (sword_state is "use") and (playerX_change == -1):
            use_sword(swordX, swordY)
            swordY = playerY
            swordX -= swordX_change

        if (sword_state is "use") and (playerX_change == 1):
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

        player(playerX, playerY)
        enemy(enemyX, enemyY)
        pygame.display.update()


intro()
main(1000)
