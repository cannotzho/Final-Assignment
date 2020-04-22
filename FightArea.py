# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 15:01:43 2020

@author: Ken Zho
"""
#FightArea class

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from functools import partial
from kivy.graphics import Rectangle, Color
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label


def collides(body1, body2):
    r1x = body1[0][0]
    r1y = body1[0][1]
    r2x = body2[0][0]
    r2y = body2[0][1]
    r1w = body1[1][0]
    r1h = body1[1][1]
    r2w = body2[1][0]
    r2h = body2[1][1]

    if (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
        return True
    return False

def parried_animation(widget, *args):
    widget.blink_size = 0
    widget.effect_opacity = (1, 1, 1, 1)
    
    anim = Animation(effect_opacity = (1, 1, 1, 0), blink_size = 200)
    
    anim.start(widget)
                 
def knockback_animation(player, weap_orient, *args):
    
    
    anim = Animation(pos = weap_orient, duration = 0.2)
    
    anim.start(player) 

def guard_animation(player, left_shield, right_shield, player_pos, *args):
    anim = Animation(shield_opacity = (1,1,1, 0.7), duration = 0.4)
    animleft = Animation(pos = player_pos, duration = 0.3)
    animright = Animation(pos = (player_pos[0] + 50, player_pos[1]), duration = 0.3)
    anim.start(player)
    animleft.start(left_shield)
    animright.start(right_shield)    

class FightArea(Screen):
    keysPressed = set() #create set to store values of keys being pressed

    
    def __init__(self, playerone, playertwo, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.background = Rectangle(source = 'background.png', pos = self.pos, size = (800, 600))
        self.add_widget(playertwo)
        self.add_widget(playerone)
        
        self.playerone = playerone
        self.playertwo = playertwo
        self.weaponone = playerone.weapon
        self.weapontwo = playertwo.weapon
        self.winner = ""
        
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down = self._on_key_down) #binding key press to callback function
        self._keyboard.bind(on_key_up = self._on_key_up)
        
        
            
        
        Clock.schedule_interval(partial(playerone.move_step, playertwo), 0)
        Clock.schedule_interval(partial(playertwo.move_step, playerone), 0)

        Clock.schedule_interval(playerone.update_visuals, 0)
        Clock.schedule_interval(playertwo.update_visuals, 0)

        Clock.schedule_interval(partial(self.playertwo.damage_check, self.weaponone), 0)
        Clock.schedule_interval(partial(self.playerone.damage_check, self.weapontwo), 0)
        
        Clock.schedule_interval(self.game_over_check, 0)
    
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down = self._on_key_down)
        self._keyboard.unbind(on_key_up = self._on_key_up)
        self._keyboard = None
        
    def _on_key_down(self, keyboard, keycode, text, modifiers):
        FightArea.keysPressed.add(text)
        
         
        
    def _on_key_up(self, keyboard, keycode):
        inpud = keycode[1]
        if inpud in FightArea.keysPressed:
            FightArea.keysPressed.remove(inpud)
            
    def game_over_check(self, dt):
        if self.playerone.game_over or self.playertwo.game_over:
            if self.playerone.game_over:
                self.winner = self.playertwo.name
            if self.playertwo.game_over:
                self.winner = self.playerone.name
            
            self.add_widget(End_Screen_Overlay(winner = self.winner))
            
            return False
            
class End_Screen_Overlay(Widget):
    def __init__(self, winner, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.overlay_color = Color(0, 0, 0, 0.6)
            self.overlay = Rectangle(pos = (0, 0), size = (1000, 1000))
        self.play_again = Button(text = "Play Again", pos = (350, 200))
        self.play_again.bind(on_press = self.go_to_main)
        self.add_widget(self.play_again)
        self.winner_label = Label(pos = (350, 400), text = "{:10} wins!".format(winner))
        self.add_widget(self.winner_label)
    def go_to_main(self, *args):
        self.parent.manager.current = "menu"
        
        
