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




class Character(Widget): #Create subclass for all character types  player, enemies etc
    
    def __init__(self, startpos = (0,0), movekeys = list("wsdaczx"), weapon_choice = W.Sword, name = "player", character_number = 1, **kwargs):
        super().__init__(**kwargs)
        #initiate widget size and widget pos
        self.pos = startpos
        self.size_hint = (0.5/4, 0.5/3) #weird size_hint being used because ScreenManager is a stupid relative layout
        
        self.game_over = False
        self.movekeys = movekeys
        self.name = name
        #orientation information and some other base player attributes
        self.movespeed = 300
        self.orientation = 0        
        self.directiondict = {0: (0, 500), 1: (0, -500), 2: (500, 0), 3: (-500, 0)}
        
        #information about different states and special combat related variables
        self.istate = False
        self.atkoffcd = True
        self.rollstate = False
        self.parry_state = False
        self.vuln_state = False
        self.guard_state = False
        self.hammer_charge = 0
        
        #effect variables
        self.char_no = character_number
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
            self.player = Rectangle(source = 'knight {:1}.png'.format(self.char_no), pos = startpos, size = (100, 100))
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
            self.weapon = W.Sword(((self.player.pos[0]+1000), (self.player.pos[1])+1000))
        if weapon_choice.weaptype == "lance":
            self.weapondirectiondict = {0: (40, 110), 1: (40, -110), 2: (110, 40), 3: (-110, 40)}
            self.weapon = W.Lance(((self.player.pos[0])+1000, (self.player.pos[1])+1000))
        if weapon_choice.weaptype == "hammer":
            self.weapondirectiondict = {0: (50, 110), 1: (50, -10), 2: (110, 50), 3: (-10, 50)}
            self.weapon = W.Hammer(((self.player.pos[0])+1000, (self.player.pos[1])+1000))
        
        self.add_widget(self.weapon)
        
        self.posilock = self.player.pos
        
        
    #movement function which also contains information for all different player controls.
    #This is so that the number of scheduled functions in the FightArea widget can be reduced    
    def move_step(self, b2, dt, *largs):
        #First need to make sure the invisible character widget is the right size and updates even when the window changes in size
        self.size_hint = (100/self.parent.size[0], 100/self.parent.size[1])
        newx, newy = self.pos
        nextcoords = [newx, newy]
        currentx, currenty = self.pos
        step_size = self.movespeed * dt
        was_guarding = False
        
        if self.guard_state:
            self.movespeed = 200
            was_guarding = True
        elif self.hammer_charge != 0:
            self.movespeed = 100
        else:
            self.movespeed = 300
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
                
            self.pos = (newx, newy)
            self.player.pos = (newx, newy)
            self.health.pos = (newx, newy+150)
            self.stamina.pos = (newx, newy+130)
        #updating position of player model
        
        
            
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
                Clock.schedule_once(self.attackcooldown, self.weapon.weapon_speed)
                
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
            if self.weapon.weaptype == "sword" and not self.parry_state and not self.vuln_state and self.stamavail >= 50:
                self.stamavail -= 50
                self.parry_state = True                    
                
                Clock.schedule_once(self.recover_parry, 0.7)
            #lances have guard as a special move
            if self.weapon.weaptype == "lance":
                if not self.vuln_state:
                    self.guard_state = True
                    
                    if not was_guarding:
                        self.guarding_sound.play()
                        FA.guard_animation(self, self.left_shield, self.right_shield, self.player.pos)
           
            #Great hammers have a ground smash special            
            if self.weapon.weaptype == "hammer" and not self.parry_state and not self.vuln_state:
                
                self.weapon.weapon_color.rgba = (1, 1, 1, 0.5)
                if self.stamavail >= 0.56:
                    self.stamavail -= 0.56
                    self.hammer_charge += 100 * dt
                
                self.weapon.pos = (self.pos[0] + 50 - self.weapon.hitbox.size[0]/2, self.pos[1] + 50 - self.weapon.hitbox.size[1]/2)
                self.weapon.hitbox.pos = (self.pos[0] + 50 - self.weapon.hitbox.size[0]/2, self.pos[1] + 50 - self.weapon.hitbox.size[1]/2) 
                self.weapon.hitbox.size = (self.hammer_charge, self.hammer_charge)
        
        #This block is specially set aside to reset hammer charge special
        if self.movekeys[6] not in FA.FightArea.keysPressed and self.hammer_charge != 0:
            self.weapon.weapon_color.rgba = (1, 1, 1, 1)
            self.weapon.size = (self.hammer_charge, self.hammer_charge)
            self.vuln_state = True
            Clock.schedule_once(self.hammer_charge_reset, 1)
                
        #stamina recovery        
        if self.stamavail < 100 and not self.guard_state and self.hammer_charge == 0:        
            self.stamavail += 10 * dt
        self.stamina.size = (self.stamavail, self.stamina.size[1])
        
        #Ensures that player sprites don't get stuck inside each other
        if self.collide_widget(b2) or not self.atkoffcd:    
            
            self.pos = (currentx, currenty)
            self.player.pos = (currentx, currenty)
            self.health.pos = (currentx, currenty+150)
            self.stamina.pos = (currentx, currenty+130)
           
        
            
    #function to update all visual changes        
    def update_visuals(self, dt):
        #update background to be relative to window size
        self.parent.background.size = self.parent.size
        
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
        
        elif self.collide_widget(b2):
            Clock.schedule_once(self.recoverroll, 1)
            newcoords[0] -= self.directiondict[self.orientation][0] * dt
            newcoords[1] -= self.directiondict[self.orientation][1] * dt
            self.pos = newcoords
            self.player.pos = newcoords
            self.health.pos = (newcoords[0], newcoords[1]+150)
            self.stamina.pos = (newcoords[0], newcoords[1]+130)
            return False
            
        
        if not self.collide_widget(b2):    
            newcoords[0] += self.directiondict[self.orientation][0] * dt
            newcoords[1] += self.directiondict[self.orientation][1] * dt
            
        self.pos = newcoords    
        self.player.pos = newcoords
        self.health.pos = (newcoords[0], newcoords[1]+150)
        self.stamina.pos = (newcoords[0], newcoords[1]+130)
        
        
    def damage_check(self, weap, dt, *largs):            
        damage_multiplier = 1
        if self.istate:
            self.player.source = 'knight {:1} hurt.png'.format(self.char_no)
            
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
            self.player.source = 'knight {:1} parry.png'.format(self.char_no)
            
        elif self.game_over:
            self.player.source = 'knight {:1} dead.png'.format(self.char_no)
            
        else:
            
            self.player.source = 'knight {:1}.png'.format(self.char_no)
            
        
        
            
        if self.collide_widget(weap) and self.istate == False:
            print(weap.pos, weap.size)
            print(self.pos, self.size)
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
                
                FA.knockback_animation(self.player, weap_orient)
                self.player.source = 'knight {:1} hurt.png'.format(self.char_no)
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
        
    def hammer_charge_reset(self, dt):
        self.hammer_charge = 0
        
        self.weapon.weapdespawn()
        self.vuln_state = False
        

        