# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 01:32:01 2020

@author: Ken Zho
"""
#Contains all weapon classes, includes instructions for how to draw, movesets and damage
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
import FightArea as FA


class Sword(Widget):
    def __init__(self, startpos = (100,100), **kwargs):
        super().__init__(**kwargs)
        self.initpos = startpos
        self.damage = 10
    def move(self, dt):
        
        with self.canvas:
            self.hitbox = Rectangle(pos = startpos, size = (100, 50))
        startpos[1] -= 100 * dt
        
            
             
            

            