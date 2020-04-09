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

class FightArea(BoxLayout):
    keysPressed = set() #create set to store values of keys being pressed
    def __init__(self, playerone, playertwo, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(playertwo)
        self.add_widget(playerone)
        self.playerone = playerone
        self.playertwo = playertwo
        
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down = self._on_key_down) #binding key press to callback function
        self._keyboard.bind(on_key_up = self._on_key_up)
        
        def test(b1, b2, dt, *largs):
            if collides((b1.player.pos, b1.player.size), (b2.player.pos, b2.player.size)):
                print("Colliding")
            else:
                print("Not colliding")
        
        Clock.schedule_interval(partial(playerone.move_step, playertwo), 0)
        Clock.schedule_interval(partial(playertwo.move_step, playerone), 0)
        Clock.schedule_interval(partial(test, playerone, playertwo), 0)
        Clock.schedule_interval(partial(playertwo.damage_check, playerone.weapon), 0)
        
    
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