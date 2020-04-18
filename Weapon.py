# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 01:32:01 2020

@author: Ken Zho
"""
#Contains all weapon classes, includes instructions for how to draw, movesets and damage
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.core.audio import SoundLoader


class Sword(Widget):
    weaptype = "sword"
    def __init__(self, startpos = (100,100), orientation = 0, **kwargs):
        super().__init__(**kwargs)
        self.initpos = startpos
        self.startpos = startpos
        self.damage = 10
        self.orientation = orientation
        self.movecost = 0
        self.attack_sound = SoundLoader.load("weapon_swing.wav")
        self.attack_sound.seek(0)
        
        
        with self.canvas:
            Color(1, 1, 1, 1)
            self.hitbox = Rectangle(pos = startpos, size = (0, 0))
        self.recoil = False
        #dictionary containing information on weapon shape and movement direction based on orientation
    orientationdict = {0: [(40,100), (0, 500)], 1: [(40,100), (0, -500)], 2: [(100, 40), (1, -500)], 3: [(100, 40), (1, 500)]}  
        
    def weapspawn(self, spawnpos, orientation):
        self.spawnpos = spawnpos
        self.hitbox.pos = spawnpos
        self.hitbox.size = Sword.orientationdict[orientation][0]
        pass
    def move(self, orientation, dt, *largs):
        self.attack_sound.play()
        self.movecost = 20
        curx, cury = self.hitbox.pos 
        coords = [curx, cury]
        coords[Sword.orientationdict[orientation][1][0]] += Sword.orientationdict[orientation][1][1] * dt        
        self.hitbox.pos = (coords[0], coords[1])
        
        if abs(coords[Sword.orientationdict[orientation][1][0]] - self.spawnpos[Sword.orientationdict[orientation][1][0]]) >=  80:
            self.weapdespawn()
            return False
            
    def weapdespawn(self):
        self.hitbox.size = (0, 0)
        self.hitbox.pos = (1000, 1000)
        pass
    
    def stamdeduct(self, stam, nostam):
        if stam > self.movecost:
            stam -= self.movecost
            return (stam, nostam)
            
        else:
            nostam = True
            return (stam, nostam)
        
class Lance(Widget):
    weaptype = "lance"
    def __init__(self, startpos = (100,100), orientation = 0, **kwargs):
        super().__init__(**kwargs)
        self.initpos = startpos
        self.startpos = startpos
        self.damage = 20
        self.orientation = orientation
        self.movecost = 0
        self.attack_sound = SoundLoader.load("weapon_swing.wav")
        
        
        with self.canvas:
            Color(1, 1, 1, 1)
            self.hitbox = Rectangle(pos = startpos, size = (0, 0))
        self.recoil = False
        #dictionary containing information on weapon shape and movement direction based on orientation
    orientationdict = {0: [(20,150), (1, 500)], 1: [(20,150), (1, -500)], 2: [(150, 20), (0, 500)], 3: [(150, 20), (0, -500)]}  
        
    def weapspawn(self, spawnpos, orientation):
        self.spawnpos = spawnpos
        self.hitbox.pos = spawnpos
        self.hitbox.size = Lance.orientationdict[orientation][0]
        pass
    def move(self, orientation, dt, *largs):
        self.attack_sound.play()
        self.movecost = 30
        curx, cury = self.hitbox.pos 
        coords = [curx, cury]
        coords[Lance.orientationdict[orientation][1][0]] += Lance.orientationdict[orientation][1][1] * dt        
        self.hitbox.pos = (coords[0], coords[1])
        
        if abs(coords[Lance.orientationdict[orientation][1][0]] - self.spawnpos[Lance.orientationdict[orientation][1][0]]) >=  80:
            self.weapdespawn()
            return False
            
    def weapdespawn(self):
        self.hitbox.size = (0, 0)
        self.hitbox.pos = (1000, 1000)
        pass
    
    def stamdeduct(self, stam, nostam):
        if stam > self.movecost:
            stam -= self.movecost
            return (stam, nostam)
            
        else:
            nostam = True
            return (stam, nostam)
            
