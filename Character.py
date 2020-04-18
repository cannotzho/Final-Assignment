# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 14:52:46 2020

@author: Ken Zho
"""

#This file contains the character class, includes drawing instructions and player methods
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Ellipse, Color
import FightArea as FA
import Weapon as W
from kivy.clock import Clock
from functools import partial
from kivy.core.audio import SoundLoader
from kivy.animation import Animation



class Character(Widget): #Create subclass for all character types  player, enemies etc
    
    def __init__(self, startpos = (0,0), movekeys = list("wsdaczx"), weapon_choice = W.Sword, name = "player", **kwargs):
        super().__init__(**kwargs)
        self.game_over = False
        self.movekeys = movekeys
        self.name = name
        #orientation information
        self.orientation = 0        
        self.directiondict = {0: (0, 500), 1: (0, -500), 2: (500, 0), 3: (-500, 0)}
        
        #information about different states
        self.istate = False
        self.atkoffcd = True
        self.rollstate = False
        self.parry_state = False
        self.vuln_state = False
        self.guard_state = False
        
        #effect variables
        self.blink_size = 0
        self.effect_opacity = (1, 1, 1, 1)
        self.shield_opacity = (1, 1, 1, 0)
        self.left_shield_startpos = (0, 0)
        self.right_shield_startpos = (0, 0)
        self.parry_sound = SoundLoader.load("ds_parrysound.wav")
        self.parry_sound.seek(0)
        self.crit_sound = SoundLoader.load("critical_hit.wav")
        self.crit_sound.seek(0)
        self.hit_sound = SoundLoader.load("landed_hit.wav")
        self.hit_sound.seek(0)
        self.block_sound = SoundLoader.load("blocked_hit.wav")
        self.block_sound.seek(0)
        self.guarding_sound = SoundLoader.load("ds_guarding.wav")
        self.guarding_sound.seek(0)
        
        #drawing instructions
        with self.canvas:
            self.player_color = Color(1, 1, 1, 1)
            self.player = Rectangle(source = 'player.png', pos = startpos, size = (100, 100))
            self.health = Rectangle(source = 'lifebar.png', pos = (startpos[0], startpos[1]+150), size = (100, 20))
            self.stamina = Rectangle(source = 'staminabar.png', pos = (startpos[0], startpos[1]+130), size = (100, 20))
            
            #drawings for animations
            self.effect_color = Color(1, 1, 1, 1)
            self.effects = Ellipse(source = 'lifebar.png',pos = self.player.pos, size = (self.blink_size, self.blink_size))
            
            self.shield_color = Color(1, 1, 1, 0)
            self.left_shield = Rectangle(source = 'leftshield.png', pos = startpos, size = (50, 100))
            self.right_shield = Rectangle(source = 'rightshield.png', pos = startpos, size = (50, 100))
            
        self.stamavail = self.stamina.size[0]
        #Weapon information
        if weapon_choice.weaptype == "sword":
            self.weapondirectiondict = {0: (-10, 110), 1: (70, -110), 2: (110, 70), 3: (-110, -10)}
            self.weapon = W.Sword(((self.player.pos[0] +100), (self.player.pos[1]+100)))
        if weapon_choice.weaptype == "lance":
            self.weapondirectiondict = {0: (50, 110), 1: (50, -110), 2: (110, 50), 3: (-110, 50)}
            self.weapon = W.Lance(((self.player.pos[0] +100), (self.player.pos[1]+100)))
        
        self.add_widget(self.weapon)
        self.posilock = self.player.pos
        
        
    #movement function which also contains information for all different player controls.
    #This is so that the number of scheduled functions in the FightArea widget can be reduced    
    def move_step(self, b2, dt, *largs):
        newx, newy = self.player.pos
        nextcoords = [newx, newy]
        currentx, currenty = self.player.pos
        step_size = 300 * dt
        was_guarding = False
        if self.guard_state:
            was_guarding = True
        self.guard_state = False
        #movement functionality, checks for other states
        if not self.rollstate and not self.parry_state and not self.vuln_state:
            
            if self.movekeys[0] in FA.FightArea.keysPressed:
                newy += step_size
                self.orientation = 0
            if self.movekeys[1] in FA.FightArea.keysPressed:
                newy -= step_size
                self.orientation = 1
            if self.movekeys[2] in FA.FightArea.keysPressed:
                newx += step_size
                self.orientation = 2
            if self.movekeys[3] in FA.FightArea.keysPressed:
                newx -= step_size
                self.orientation = 3
            
            self.player.pos = (newx, newy)
            self.health.pos = (newx, newy+150)
            self.stamina.pos = (newx, newy+130)
        #updating position of player model
        if FA.collides((self.player.pos, self.player.size), (b2.player.pos, b2.player.size)) or not self.atkoffcd:
            self.player.pos = (currentx, currenty)
            self.health.pos = (currentx, currenty+150)
            self.stamina.pos = (currentx, currenty+130)
        #attack functionality    
        if self.movekeys[4] in FA.FightArea.keysPressed:
            
            nostam = False
            
            nostam = self.weapon.stamdeduct(self.stamavail, nostam)[1]
            if not nostam and self.stamavail > 0 and self.atkoffcd and not self.rollstate and not self.parry_state and not self.vuln_state:
                self.stamavail = self.weapon.stamdeduct(self.stamavail, nostam)[0]
                self.stamina.size = (self.stamavail, self.stamina.size[1])
                self.weapon.weapspawn(((self.player.pos[0] + self.weapondirectiondict[self.orientation][0]), (self.player.pos[1]+ self.weapondirectiondict[self.orientation][1])), self.orientation)
                Clock.schedule_interval(partial(self.weapon.move, self.orientation), 0)
                self.atkoffcd = False
                Clock.schedule_once(self.attackcooldown, 0.5)
                
            else:
                self.stamina.size = self.stamina.size
        #rolldodge functionality
        if self.movekeys[5] in FA.FightArea.keysPressed:
            if self.stamavail > 30 and self.atkoffcd and not self.rollstate and not self.parry_state and not self.vuln_state:
                self.posilock = currentx, currenty
                self.istate = True
                self.rollstate = True
                Clock.schedule_once(self.recoverdmg, 0.6)
                
                self.stamavail -= 30
                self.stamina.size = (self.stamavail, self.stamina.size[1])                         
                Clock.schedule_interval(partial(self.roll, nextcoords, self.posilock, b2), 0)
        #special functionality        
        if self.movekeys[6] in FA.FightArea.keysPressed:
            #swords have parry as a special move
            if self.weapon.weaptype == "sword" and not self.parry_state and not self.vuln_state:
                self.parry_state = True                    
                self.player.source = 'staminabar.png'
                Clock.schedule_once(self.recover_parry, 0.7)
            #lances have guard as a special move
            if self.weapon.weaptype == "lance":
                if not self.vuln_state:
                    self.guard_state = True
                    if not was_guarding:
                        self.guarding_sound.play()
                        FA.guard_animation(self, self.left_shield, self.right_shield, self.player.pos)
                
                
        #stamina recovery        
        if self.stamavail < 100 and not self.guard_state:        
            self.stamavail += 10 * dt
            self.stamina.size = (self.stamavail, self.stamina.size[1])
            
            
    #function to update all visual changes        
    def update_visuals(self, dt):
        
        self.effects.size = self.blink_size, self.blink_size
        self.effects.pos = (self.player.pos[0]+50-self.effects.size[0]/2, self.player.pos[1]+50-self.effects.size[1]/2)
        
        self.effect_color.rgba = self.effect_opacity
        if not self.guard_state:
            self.shield_color.rgba = (1, 1, 1, 0)
            self.left_shield_startpos = (self.player.pos[0]-50, self.player.pos[1])
            self.right_shield_startpos = (self.player.pos[0]+100, self.player.pos[1])
        if self.guard_state:
            self.left_shield_startpos = self.player.pos
            self.right_shield_startpos = (self.player.pos[0]+50, self.player.pos[1])
            self.shield_color.rgba = self.shield_opacity
            
        self.left_shield.pos = self.left_shield_startpos
        self.right_shield.pos = self.right_shield_startpos
        
        if self.istate:
            self.player_color.rgba = (1, 1, 1, 0.7)
        else:
            self.player_color.rgba = (1, 1, 1, 1)
        
            
    def recoverdmg(self, dt):
        self.istate = False

    def attackcooldown(self, dt):
        self.atkoffcd = True
        
    def recover_parry(self, dt):
        self.vuln_state = True        
        self.parry_state = False
        Clock.schedule_once(self.recover_vulnerable, 0.3)
        
    def recover_vulnerable(self, dt):
        self.vuln_state = False
        
    def recoverroll(self, dt):
        self.rollstate = False
        
    def roll(self, newcoords, originalcoords, b2, dt):
        if (abs(newcoords[0] - originalcoords[0]) > 300) or (abs(newcoords[1] - originalcoords[1]) > 300):
            self.rollstate = False
            return False
        elif FA.collides((self.player.pos, self.player.size), (b2.player.pos, b2.player.size)):
            Clock.schedule_once(self.recoverroll, 1)
            newcoords[0] -= self.directiondict[self.orientation][0] * dt
            newcoords[1] -= self.directiondict[self.orientation][1] * dt
            self.player.pos = newcoords
            self.health.pos = (newcoords[0], newcoords[1]+150)
            self.stamina.pos = (newcoords[0], newcoords[1]+130)
            return False
            
        if not FA.collides((self.player.pos, self.player.size), (b2.player.pos, b2.player.size)):
            newcoords[0] += self.directiondict[self.orientation][0] * dt
            newcoords[1] += self.directiondict[self.orientation][1] * dt
            
        self.player.pos = newcoords
        self.health.pos = (newcoords[0], newcoords[1]+150)
        self.stamina.pos = (newcoords[0], newcoords[1]+130)
        
        
    def damage_check(self, weap, dt, *largs):            
        damage_multiplier = 1
        if self.istate:
            self.player.source = 'hurtplayer.png'
            
        elif self.vuln_state:
            self.player.source = 'vulnerableplayer.png'
            
        elif self.weapon.recoil:
            self.parry_sound.play()
            self.vuln_state = True
            self.weapon.recoil = False
            self.player.source = 'lifebar.png'
            event = Clock.schedule_interval(self.damage_anim, 0.05)
            Clock.schedule_once(lambda dt: event.cancel, 0.5)
            FA.parried_animation(self)
            Clock.schedule_once(self.recover_vulnerable, 1.5)
        
        elif self.parry_state:
            
            self.player.source = 'parryingplayer.png'
        else:
            
            self.player.source = 'player.png'
            
        
        if FA.collides((self.player.pos, self.player.size), (weap.hitbox.pos, weap.hitbox.size)) and self.istate == False:
            if self.parry_state and not weap.parent.vuln_state:
                weap.recoil = True
                
                
                
            elif self.health.size[0] > 0 and not self.parry_state:
                if self.vuln_state:
                    self.crit_sound.play()
                    damage_multiplier = 3
                elif self.guard_state:
                    self.block_sound.play()
                    damage_multiplier = 0.5
                self.hit_sound.play()
                self.health.size = ((self.health.size[0]-damage_multiplier * weap.damage), self.health.size[1])
                weap_orient = (self.player.pos[0] + weap.parent.directiondict[weap.parent.orientation][0]*0.1, self.player.pos[1] + weap.parent.directiondict[weap.parent.orientation][1]*0.1)
                #weap_orient = (0,0)
                FA.knockback_animation(self.player, weap_orient)
                self.player.source = 'hurtplayer.png'
                self.istate = True
                Clock.schedule_once(self.recoverdmg, 2)

            
            
        if self.health.size[0] <= 0:
            self.game_over = True
                        
    
    def damage_anim(self, dt):
        newx, newy = self.player.pos
        if int(newx)%2 == 0:
            self.player.pos = (newx+7, newy+7)
        else:
            self.player.pos = (newx-7, newy-7)
        if not self.vuln_state:
            return False
        

        