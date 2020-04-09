# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 01:32:01 2020

@author: Ken Zho
"""
#Contains all weapon classes, includes instructions for how to draw, movesets and damage
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle



class Sword(Widget):
    def __init__(self, startpos = (100,100), **kwargs):
        super().__init__(**kwargs)
        self.initpos = startpos
        self.startpos = startpos
        self.damage = 10
        
    def weapspawn(self, spawnpos):
        with self.canvas:
            self.hitbox = Rectangle(pos = spawnpos, size = (100, 50))
        self.spawnpos = spawnpos
    def move(self, dt):        
        curx, cury = self.hitbox.pos 
        
        cury -= 100 * dt        
        self.hitbox.pos = (curx, cury)
        
        if cury <= (self.spawnpos[1] - 100):
            return False
            
    def weapdespawn(self):
        pass