# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 14:52:46 2020

@author: Ken Zho
"""

#This file contains the character class, includes drawing instructions and player methods
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
import FightArea as FA
import Weapon as W
from kivy.clock import Clock

class Character(Widget): #Create subclass for all character types  player, enemies etc
    def __init__(self, startpos = (0,0), movekeys = list("wsdac"), **kwargs):
        super().__init__(**kwargs)
        self.movekeys = movekeys
        self.name = __name__
        
        with self.canvas:
            self.player = Rectangle(pos = startpos, size = (100, 100))
            self.health = Rectangle(source = 'lifebar.png', pos = (startpos[0], startpos[1]+150), size = (100, 20))
            self.stamina = Rectangle(source = 'staminabar.png', pos = (startpos[0], startpos[1]+130), size = (100, 20))
        
        self.weapon = W.Sword(((self.player.pos[0] +100), (self.player.pos[1]+100)))    
    def move_step(self, b2, dt, *largs):
        newx, newy = self.player.pos
        currentx, currenty = self.player.pos
        step_size = 100 * dt
        
        if self.movekeys[0] in FA.FightArea.keysPressed:
            newy += step_size
            
        if self.movekeys[1] in FA.FightArea.keysPressed:
            newy -= step_size
            
        if self.movekeys[2] in FA.FightArea.keysPressed:
            newx += step_size
            
        if self.movekeys[3] in FA.FightArea.keysPressed:
            newx -= step_size
            
        self.player.pos = (newx, newy)
        self.health.pos = (newx, newy+150)
        self.stamina.pos = (newx, newy+130)
        
        if FA.collides((self.player.pos, self.player.size), (b2.player.pos, b2.player.size)):
            self.player.pos = (currentx, currenty)
            self.health.pos = (currentx, currenty+150)
            self.stamina.pos = (currentx, currenty+130)
            
        if self.movekeys[4] in FA.FightArea.keysPressed:
            self.weapon.weapspawn(((self.player.pos[0] +100), (self.player.pos[1]+100)))
            Clock.schedule_interval(self.weapon.move, 0)
            
    def damage_check(self, weap, dt, *largs):
        try:
            if FA.collides((self.player.pos, self.player.size), (weap.hitbox.pos, weap.hitbox.size)):
                if self.health.size[0] > 0:
                    self.health.size = ((self.health.size[0]-weap.damage), self.health.size[1])
                
                    
        except:
            pass
            
        if self.health.size[0] == 0:
            print(self.name + " is dead!")
            