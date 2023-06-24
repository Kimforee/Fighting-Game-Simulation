
import time
import simpy
import pygame
import random
import numpy as np
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

WEAK_ATTACK_DAMAGE = 5
WEAK_ATTACK_COOLDOWN = 1
STRONG_ATTACK_DAMAGE = 10
STRONG_ATTACK_COOLDOWN = 2
SPECIAL_ATTACK_DAMAGE = 50
SPECIAL_ATTACK_COOLDOWN = 3
MAX_HEALTH = 100
sim_time = 100
width = 1160
height = 600
global x
x = 0
root = Tk()
pygame.mixer.init()
style = ttk.Style()
style.configure("Custom.TButton", background="black",
                 foreground="#000000", font=("Helvetica", 16),
                  borderwidth=3, relief="raised", padding=2)

bkg = PhotoImage  (file="images/liuy.png")
widgetcolor = '#295F6C'
root.overrideredirect(False)
root.geometry     ("1280x720")
root.title        ("Epidemic Game Simulation")
title_bar = Frame (root,bg='#8D72E1',relief=SUNKEN,bd=2)

# setting the background image
bimage = Label(root,image=bkg)
bimage.place(x=0,y=0)

# to close the simulation window
def close():
    buttonsounds()
    ans=messagebox.askokcancel("Title","Do you really want to exit Simulation?")
    if(ans==True):
       pygame.mixer.music.stop()
       root.destroy()

# to play button sounds
def buttonsounds():
    sound.play()

# to play music
def musicplayer():
    global sound
    sound = pygame.mixer.Sound("audio/button.mp3")
    pygame.mixer.music.load("audio/start.mp3")
    pygame.mixer.music.play(loops=5)
musicplayer()

def audio():
    audiocan = Canvas(root,width=300,height=100,bd=3,
                      relief=SUNKEN,)
    audiocan.place(x=480,y=500)
    on = PhotoImage(file="images/on.png")
    off = PhotoImage(file="images/off.png")
    a = 0
    global volume
    volume = 0.9
    pygame.mixer.music.set_volume(volume)
    sound.set_volume(volume)
    def switch():
        buttonsounds()
        nonlocal a
        a = a + 1
        if(a % 2 == 0 or a==0):
            img = on
            pygame.mixer.music.unpause()
        else:
            img = off
            pygame.mixer.music.pause()
        onoff.config(image=img)
    img = on

    # Increase volume
    def incvolume():
        buttonsounds()
        global volume       
        volume += 0.1
        pygame.mixer.music.set_volume(volume)
        sound.set_volume(volume)
    
    # Decrease volume   
    def decvolume():
        buttonsounds()
        global volume 
        volume -= 0.1
        pygame.mixer.music.set_volume(volume)
        sound.set_volume(volume)
    incvbutton = Button(audiocan,text='+',
                        command=incvolume,
                        fg='black',
                        activeforeground='#C47AFF',
                        font=('Arial Bold', 22),
                        bd=2,width=3,height=1)
    incvbutton.place(x=10,y=35)
    decvbutton = Button(audiocan,text='-',
                        command=decvolume,fg='black',
                        activeforeground='#C47AFF',
                        font=('Arial Bold', 22),
                        bd=2,width=3,height=1)
    decvbutton.place(x=230,y=35)
    close = Button(audiocan, text='X', command=audiocan.destroy,fg='black',
                    relief=FLAT, 
                    activeforeground='#C47AFF',
                    font=('Arial Bold', 10),
                    bd=3,width=4,height=1)
    close.place(x=260,y=5)
    onoff = Button(audiocan, image=img, command=switch,
                    fg='black',
                    activeforeground='#C47AFF',
                    font=('Arial Bold', 16),
                    bd=3,width=25,height=25)
    onoff.place(x=135,y=20)
    
def destroyer1():  
    quitbutton.destroy()
    startbutton.destroy()

def backtomain():
    # canvas.destroy()
    main()

def outcan():
    # for zombies
    global can
    can = Canvas(root,width=290,height=300)
    can.place(x=900,y=50)
    back = ttk.Button(can,text='X',width=1,command=can.destroy,style="Custom.TButton")
    back.place(x=265,y=10)

def Outputviewer(output,row):
    row = int(row)
    outputlabel = Label(can,text=output,width=35,height=1,
                        relief=SUNKEN,highlightbackground='#CDFCF6',
                        activeforeground='#C47AFF',
                        fg='black',bg='#D3ECFF',
                        bd=1)
    outputlabel.place(x=10,y=10+(row*20))
    outputlabel.update()

def outcan1():
    # for humans
    global can1
    can1 = Canvas(root,width=290,height=300)
    can1.place(x=70,y=50)
    back = ttk.Button(can1,text='X',width=1,command=can1.destroy,style="Custom.TButton")
    back.place(x=265,y=10)

def Outputviewer1(output,row):
    row = int(row)
    outputlabel = Label(can1,text=output,width=35,height=1,
                        highlightbackground='#CDFCF6',relief=SUNKEN,
                        activeforeground='#C47AFF',
                        fg='black',bg='#D3ECFF',
                        bd=1)
    outputlabel.place(x=10,y=10+(row*20))
    outputlabel.update()

def winner(output):
    global win 
    win = Label(root,text=output,width=25,height=2,
                        highlightbackground='#CDFCF6',relief=RAISED,
                        activeforeground='#C47AFF',
                        fg='black',bg='#D3ECFF',font=('Arial Bold', 14),
                        bd=2)
    win.place(x=490,y=100)

#border design left side
line1 = Label(root, text= "",
             highlightbackground='#CDFCF6',
             relief=RAISED,
             activeforeground='#C47AFF',
             fg='black',bg=widgetcolor,
             bd=10,
             width=1,
             height=100)
line1.place(x= 1,y= 1)

#border design right side
line2 = Label(root, text= "",
             highlightbackground='#CDFCF6',
             relief=RAISED,
             activeforeground='#C47AFF',
             fg='black',bg=widgetcolor,
             bd=10,
             width=1,
             height=100)
line2.place(x= 1250,y=1)

# Starts the simulation 
def start():
    global hweak,hstrong,hspecial,hdefense,zweak,zstrong,zspecial,zdefense
    global hp1
    global hp2
    zweak  = 0
    zstrong  = 0
    zspecial = 0
    zdefense = 0
    hweak = 0
    hstrong = 0
    hspecial = 0
    hdefense = 0
    outcan1()
    outcan()
    buttonsounds()
    random.seed(23)
    # Human attack function
    class PlayerHuman:
        def __init__(self, env, name):
            self.env = env
            self.name = name
            self.hp = MAX_HEALTH
            self.weak_attack_ready = True
            self.strong_attack_ready = True
            self.special_attack_ready = True

        def weak_attack(self, opponent):
            global hweak
            hweak = hweak + 1
            output =(f'{self.name}    used weak attack at {env.now}')
            opponent.hp -= WEAK_ATTACK_DAMAGE
            self.weak_attack_ready = False
            self.env.process(self.cooldown(WEAK_ATTACK_COOLDOWN, lambda: self.weak_attack_ready == True))
            return output
            
        def strong_attack(self, opponent):
            global hstrong
            hstrong = hstrong + 1
            output =(f'{self.name}  used strong attack at {env.now}')
            opponent.hp -= STRONG_ATTACK_DAMAGE
            self.strong_attack_ready = False
            self.env.process(self.cooldown(STRONG_ATTACK_COOLDOWN, lambda: self.strong_attack_ready == True))
            return output

        def special_attack(self, opponent):
            global hspecial
            hspecial = hspecial + 1
            output =(f'{self.name} used special attack at {env.now}')
            opponent.hp -= SPECIAL_ATTACK_DAMAGE
            self.special_attack_ready = False
            self.env.process(self.cooldown(SPECIAL_ATTACK_COOLDOWN, lambda: self.special_attack_ready == True))
            return output

        def do_nothing(self):
            global hdefense
            hdefense = hdefense + 1
            output =(f'{self.name}          did    nothing at {env.now}')
            return output

        def attack(self, opponent):
            if self.special_attack_ready and self.hp <= SPECIAL_ATTACK_DAMAGE:
                output = self.special_attack(opponent)
                Outputviewer1(output,int(env.now))
            else:
                attack_type = random.choice(['weak', 'strong', 'weak', 'none','strong'])
                if attack_type == 'weak' and self.weak_attack_ready:
                    output = self.weak_attack(opponent)
                    Outputviewer1(output,int(env.now))
                elif attack_type == 'strong' and self.strong_attack_ready:
                    output = self.strong_attack(opponent)
                    Outputviewer1(output,int(env.now))
                elif attack_type == 'none':
                    output = self.do_nothing()
                    Outputviewer1(output,int(env.now))
                else:
                    output = self.weak_attack(opponent)
                    Outputviewer1(output,int(env.now))
            

        def cooldown(self, time, callback):
            yield self.env.timeout(time)
            callback()

    # Zombie attack function
    class PlayerZombie:
        global hweak,hstrong,hspecial,hdefense
        global zweak,zstrong,zspecial,zdefense
        def __init__(self, env, name):
            self.env = env
            self.name = name
            self.hp = MAX_HEALTH
            self.weak_attack_ready = True
            self.strong_attack_ready = True
            self.special_attack_ready = True

        def weak_attack(self, opponent):
            global zweak
            zweak = zweak + 1
            output =(f'{self.name}   used weak attack at {env.now}')
            opponent.hp -= WEAK_ATTACK_DAMAGE
            self.weak_attack_ready = False
            self.env.process(self.cooldown(WEAK_ATTACK_COOLDOWN, lambda: self.weak_attack_ready == True))
            return output

        def strong_attack(self, opponent):
            global zstrong
            zstrong = zstrong + 1
            output =(f'{self.name} used strong attack at {env.now}')
            opponent.hp -= STRONG_ATTACK_DAMAGE
            self.strong_attack_ready = False
            self.env.process(self.cooldown(STRONG_ATTACK_COOLDOWN, lambda: self.strong_attack_ready == True))
            return output

        def special_attack(self, opponent):
            global zspecial
            zspecial = zspecial + 1
            output =(f'{self.name}used special attack at {env.now}')
            opponent.hp -= SPECIAL_ATTACK_DAMAGE
            self.special_attack_ready = False
            self.env.process(self.cooldown(SPECIAL_ATTACK_COOLDOWN, lambda: self.special_attack_ready == True))
            return output

        def do_nothing(self):
            global zdefense
            zdefense = zdefense + 1
            output =(f'{self.name}         did    nothing at {env.now}')
            return output
            
        def attack(self, opponent):
            
            if self.special_attack_ready and self.hp <= SPECIAL_ATTACK_DAMAGE:
                output = self.special_attack(opponent)
                Outputviewer(output,int(env.now))
            else:
                attack_type = random.choice(['weak', 'strong', 'weak', 'none','strong'])
                if attack_type == 'weak' and self.weak_attack_ready:
                    output = self.weak_attack(opponent)
                    Outputviewer(output,int(env.now))
                elif attack_type == 'strong' and self.strong_attack_ready:
                    output = self.strong_attack(opponent)
                    Outputviewer(output,int(env.now))
                elif attack_type == 'none':
                    output = self.do_nothing()
                    Outputviewer(output,int(env.now))
                else:
                    output = self.weak_attack(opponent)
                    Outputviewer(output,int(env.now))
            

        def cooldown(self, time, callback):
            yield self.env.timeout(time)
            callback()

    class Battle:
        global hweak,hstrong,hspecial,hdefense
        global zweak,zstrong,zspecial,zdefense
        global hp1
        global hp2
        hp1 = []
        hp2 = []
        def __init__(self, env):
            self.env = env
            self.player1 = PlayerHuman(env, 'Human')
            self.player2 = PlayerZombie(env, 'Zombie')

        def run(self):
            
            while self.player1.hp > 0 and self.player2.hp > 0:
                hp1.append(self.player1.hp)
                hp2.append(self.player2.hp)
                time.sleep(1)

                (self.player1.attack(self.player2))
                if self.player2.hp <= 0:
                    output =(f'{self.player1.name}s won! at {env.now}')
                    winner(output)
                    break
                self.player2.attack(self.player1)
                if self.player1.hp <= 0:
                    output =(f'{self.player2.name}s won! at {env.now}')
                    winner(output)
                    break
                yield self.env.timeout(1)
                
    env = simpy.Environment()
    battle = Battle(env)
    env.process(battle.run())
    env.run(until=sim_time)
    
def graph1():
    buttonsounds()
    global canvas,win
    global hp1
    global hp2
    win.destroy()
    #creating canvas
    canvas = Canvas(root,width=700,height=500)
    canvas.place(x=55,y=25)
    back = ttk.Button(canvas,text='X',width=1,command=canvas.destroy,style="Custom.TButton")
    back.place(x=660,y=10)
    next = ttk.Button(canvas,text='>',width=1,command=graph2,style="Custom.TButton")
    next.place(x=660,y=50)
    fig, ax = plt.subplots()
    ax.plot(hp1, label='Human Health')
    ax.plot(hp2, label='Zombie Health')
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, canvas)
    canvas.get_tk_widget().place(x=5,y=5)

def graph2():
    buttonsounds()
    species = ("Humans", "Zombies")
    penguin_means = {
        'Weak': (hweak, zweak),
        'Strong': (hstrong, zstrong),
        'Special': (hspecial, zspecial),
        'Defense': (hdefense, zdefense)
    }
    global canva
    # create a Figure object and plot the data
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    x = np.arange(len(species))
    width = 0.2
    multiplier = 0

    for attribute, measurement in penguin_means.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # set the labels and title
    ax.set_ylabel('Value')
    ax.set_title('Attributes of Humans and Zombies')
    ax.set_xticks(x + width * 1.5, species)
    ax.legend(loc='upper left', ncol=4)
    ax.set_ylim(0, 11)

    # create a canvas and add the Figure to it
    canva = Canvas(root,width=700,height=500)
    canva.place(x=55,y=25)
    back = ttk.Button(canva,text='X',width=1,command=canva.destroy,style="Custom.TButton")
    back.place(x=660,y=10)
    next = ttk.Button(canva,text='>',width=1,command=graph1,style="Custom.TButton")
    next.place(x=660,y=50)
    canva = FigureCanvasTkAgg(fig,canva)
    canva.get_tk_widget().place(x=5,y=5)
    
def main():
    global quitbutton
    global startbutton
    # button to start the simulation
    startbutton=  Button(root,text=" START ",
                        fg='black',bg='#B9E0FF',
                        activeforeground='#C47AFF',
                        font=('Arial Bold', 16),
                        bd=3,width=15,height=1,
                        command=start) 
    startbutton.place   (x=530,y=160)
    # Sounding
    soundbutton=  Button(root,text=" AUDIO ",fg='black',
                        bg='#B9E0FF',
                        activeforeground='#C47AFF',
                        font=('Arial Bold', 16),
                        bd=3,width=15,height=1,
                        command=audio)
    soundbutton.place   (x=530,y=220)
    # Gives analysis
    analytics=  Button(root,text=" ANALYTICS ",fg='black',
                        bg='#B9E0FF',
                        activeforeground='#C47AFF',
                        font=('Arial Bold', 16),
                        bd=3,width=15,height=1,
                        command=graph1)
    analytics.place   (x=530,y=280)
    # Quit button Quits the simulation
    quitbutton=  Button(root,text=" QUIT ",fg='black',
                        bg='#B9E0FF',
                        activeforeground='#C47AFF',
                        font=('Arial Bold', 16),
                        bd=3,width=15,height=1,
                        command=close)
    quitbutton.place   (x=530,y=340)
    c = Canvas(root,width=400,height=300)
    c.place(x=450,y=80)
    b = ttk.Button(c,text='X',width=1,command=c.destroy,style="Custom.TButton")
    b.place(x=375,y=10)
    lab = Label(c, text= "Data Simulation Lab",
             highlightbackground='#CDFCF6',
             relief=RAISED,font=('Arial Bold', 14),
             activeforeground='#C47AFF',
             fg='black',bg='#B9E0FF',
             bd=1,
             width=25,
             height=1)
    lab.place(x= 50,y= 50)
    game = Label(c, text= "Epidemic Game Simulation",
             highlightbackground='#CDFCF6',
             relief=RAISED,font=('Arial Bold', 14),
             activeforeground='#C47AFF',
             fg='black',bg='#B9E0FF',
             bd=1,
             width=25,
             height=1)
    game.place(x= 50,y= 95)

    name = Label(c, text= "Made by : Keshav Singh",
             highlightbackground='#CDFCF6',
             relief=RAISED,font=('Arial Bold', 14),
             activeforeground='#C47AFF',
             fg='black',bg='#B9E0FF',
             bd=1,
             width=25,
             height=1)
    name.place(x= 50,y= 140)
main()
root.mainloop()