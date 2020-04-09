# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 13:59:58 2020

@author: Ken Zho
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout



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

class Character(Widget): #Create subclass for all character types  player, enemies etc
    def __init__(self, startpos = (0,0), movekeys = list("wsda"), **kwargs):
        super().__init__(**kwargs)
        self.movekeys = movekeys
        
        
        with self.canvas:
            self.player = Rectangle(pos = (startpos[0], startpos[1]), size = (100, 100))
            
            
            
    def move_step(self, dt):
        currentx, currenty = self.player.pos
        step_size = 100 * dt
        
        if self.movekeys[0] in FightArea.keysPressed:
            currenty += step_size
            
        if self.movekeys[1] in FightArea.keysPressed:
            currenty -= step_size
            
        if self.movekeys[2] in FightArea.keysPressed:
            currentx += step_size
            
        if self.movekeys[3] in FightArea.keysPressed:
            currentx -= step_size
            
        self.player.pos = (currentx, currenty)
    
        
        
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
        
        def test(dt):
            if collides((playerone.player.pos, playerone.player.size), (playertwo.player.pos, playertwo.player.size)):
                print("Colliding")
            else:
                print("Not colliding")
        
        Clock.schedule_interval(playerone.move_step, 0)
        Clock.schedule_interval(playertwo.move_step, 0)
        Clock.schedule_interval(test, 0)
        
        
    
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
            
    

playertwo = Character((300,0), ["t", "g", "h", "f"])
playerone = Character()
box = FightArea(playerone, playertwo)



class SimpleFight(App):
    def build(self):
        return box
    
if __name__ == "__main__":
    app = SimpleFight()
    app.run()