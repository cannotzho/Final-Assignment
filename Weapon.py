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
        self.size = (0, 0)
        self.pos = startpos
        self.damage = 10
        self.orientation = orientation
        self.movecost = 0
        self.attack_sound = SoundLoader.load("sword_slice.wav")
        self.attack_sound.seek(0)
        self.weapon_speed = 0.9
        
        with self.canvas:
            Color(1, 1, 1, 1)
            self.hitbox = Rectangle(pos = self.pos, size = (0, 0))
        self.recoil = False
        #dictionary containing information on weapon shape and movement direction based on orientation
    orientationdict = {0: [(40,100), (0, 500)], 1: [(40,100), (0, -500)], 2: [(100, 40), (1, -500)], 3: [(100, 40), (1, 500)]}  
        
    def weapspawn(self, spawnpos, orientation):
        self.spawnpos = spawnpos
        
        self.pos = spawnpos
        self.size = Sword.orientationdict[orientation][0]
        self.hitbox.pos = spawnpos
        self.hitbox.size = Sword.orientationdict[orientation][0]
        self.hitbox.source = "sword{:1}.png".format(orientation)
        pass
    def move(self, orientation, dt, *largs):
        if self.attack_sound.state == "stop":
            self.attack_sound.play()
        self.movecost = 20
        curx, cury = self.hitbox.pos 
        coords = [curx, cury]
        coords[Sword.orientationdict[orientation][1][0]] += Sword.orientationdict[orientation][1][1] * dt
        self.pos = (coords[0], coords[1])        
        self.hitbox.pos = (coords[0], coords[1])
        
        if abs(coords[Sword.orientationdict[orientation][1][0]] - self.spawnpos[Sword.orientationdict[orientation][1][0]]) >=  80:
            self.weapdespawn()
            return False
            
    def weapdespawn(self):
        self.size = (0, 0)
        self.pos = (1000, 0)
        self.hitbox.size = (0, 0)
        self.hitbox.pos = (-1000, 0)
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
        self.size = (0, 0)
        self.pos = startpos
        self.damage = 20
        self.orientation = orientation
        self.movecost = 0
        self.attack_sound = SoundLoader.load("weapon_swing.wav")
        self.weapon_speed = 1.2
        
        with self.canvas:
            Color(1, 1, 1, 1)
            self.hitbox = Rectangle(pos = self.pos, size = (0, 0))
        self.recoil = False
        #dictionary containing information on weapon shape and movement direction based on orientation
    orientationdict = {0: [(20,150), (1, 500)], 1: [(20,150), (1, -500)], 2: [(150, 20), (0, 500)], 3: [(150, 20), (0, -500)]}  
        
    def weapspawn(self, spawnpos, orientation):
        self.spawnpos = spawnpos
        
        self.pos = spawnpos
        self.size = Lance.orientationdict[orientation][0]
        self.hitbox.pos = spawnpos
        self.hitbox.size = Lance.orientationdict[orientation][0]
        self.hitbox.source = "lance{:1}.png".format(orientation)
        pass
    def move(self, orientation, dt, *largs):
        if self.attack_sound.state == "stop":
            self.attack_sound.play()
        self.movecost = 30
        curx, cury = self.hitbox.pos 
        coords = [curx, cury]
        coords[Lance.orientationdict[orientation][1][0]] += Lance.orientationdict[orientation][1][1] * dt        
        self.pos = (coords[0], coords[1])
        self.hitbox.pos = (coords[0], coords[1])
        
        if abs(coords[Lance.orientationdict[orientation][1][0]] - self.spawnpos[Lance.orientationdict[orientation][1][0]]) >=  80:
            self.weapdespawn()
            return False
            
    def weapdespawn(self):
        self.size = (0, 0)
        self.pos = (-1000, 0)
        self.hitbox.size = (0, 0)
        self.hitbox.pos = (-1000, 0)
        pass
    
    def stamdeduct(self, stam, nostam):
        if stam > self.movecost:
            stam -= self.movecost
            return (stam, nostam)
            
        else:
            nostam = True
            return (stam, nostam)
            
class Hammer(Widget):
    weaptype = "hammer"
    def __init__(self, startpos = (100,100), orientation = 0, **kwargs):
        super().__init__(**kwargs)
        self.size = (0, 0)
        self.pos = startpos
        self.damage = 40
        self.orientation = orientation
        self.movecost = 0
        self.weapon_speed = 1.5
        self.attack_sound = SoundLoader.load("hammer_strike.wav")
        self.attack_sound.volume = 0.5
        
        
        with self.canvas:
            self.weapon_color = Color(1, 1, 1, 1)
            self.hitbox = Rectangle(pos = self.pos, size = (0, 0))
            self.handle = Rectangle(pos = self.pos, size = (0, 0))
        self.recoil = False
        #dictionary containing information on weapon shape and movement direction based on orientation
    orientationdict = {0: [(500, 500), (1, 200), (100, 400)], 1: [(500,-500), (1, -200), (100, -400)], 2: [(500, 500), (0, 200), (400, 100)], 3: [(-500, 500), (0, -200), (-400, 100)]}  
        
    def weapspawn(self, spawnpos, orientation):
        self.spawnpos = spawnpos        
        self.pos = spawnpos        
        self.hitbox.pos = spawnpos
        self.hitbox.source = "Hammerhead{:1}.png".format(orientation)
        self.handle.source = "Hammerstick{:1}.png".format(orientation)
        
        pass
    def move(self, orientation, dt, *largs):
        if self.attack_sound.state == "stop":
            self.attack_sound.volume = 0.05
            self.attack_sound.play()
        self.movecost = 40
        curx, cury = self.hitbox.pos 
        coords = [curx, cury]
        coords_handle = [curx, cury]
        curxsize, curysize = self.size
        handle_xsize, handle_ysize = self.handle.size
        
        curxsize += Hammer.orientationdict[orientation][0][0] * dt
        curysize += Hammer.orientationdict[orientation][0][1] * dt
        
        handle_xsize += Hammer.orientationdict[orientation][2][0] * dt
        handle_ysize += Hammer.orientationdict[orientation][2][1] * dt
        #Instructions for the hammer head
        coords[Hammer.orientationdict[orientation][1][0]] += Hammer.orientationdict[orientation][1][1] * dt
        coords[(1-Hammer.orientationdict[orientation][1][0])] = self.spawnpos[(1-Hammer.orientationdict[orientation][1][0])] - abs(self.size[0])/2
        #Instructions for the hammer handle
        coords_handle[Hammer.orientationdict[orientation][1][0]] += Hammer.orientationdict[orientation][1][1] * 0.1 * dt
        coords_handle[(1-Hammer.orientationdict[orientation][1][0])] = self.spawnpos[(1-Hammer.orientationdict[orientation][1][0])] - abs(self.handle.size[(1-Hammer.orientationdict[orientation][1][0])]/2)
        #Final updating of positions and sizes
        self.pos = coords
        self.hitbox.pos = coords
        self.handle.pos = coords_handle
        self.size = (curxsize, curysize)
        self.hitbox.size = (curxsize, curysize)
        self.handle.size = (handle_xsize, handle_ysize)
        
        
        if abs(self.hitbox.size[0]) >= 150:
            self.weapdespawn()
            return False
            
    def weapdespawn(self):
        self.hitbox.size = (0, 0)
        self.hitbox.pos = (-1000, 0)
        
        self.handle.size = (0, 0)
        self.handle.pos = (-1000, 0)
        
        self.size = (0, 0)
        self.pos = (-1000, 0)
        
        pass
    
    def stamdeduct(self, stam, nostam):
        if stam > self.movecost:
            stam -= self.movecost
            return (stam, nostam)
            
        else:
            nostam = True
            return (stam, nostam)