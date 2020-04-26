# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 15:19:22 2020

@author: Ken Zho
"""

from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from functools import partial
from kivy.app import App

class Test_object(Widget):
    def __init__(self, movekeys = "wsda", **kwargs):
        super().__init__(**kwargs)
        self.pos = (50, 50)
        self.size = (50, 50)
        self.movekeys = movekeys
        with self.canvas:
            self.player = Rectangle(pos = self.pos, size = self.size)
        
    def move_step(self, p2, dt, *largs):
        newx, newy = self.pos
        
        
        step_size = 300 * dt
        
        
        #movement functionality, checks for other states
        
            
        if self.movekeys[0] in Test_Window.keysPressed:
            newy += step_size
            self.orientation = 0
        if self.movekeys[1] in Test_Window.keysPressed:
            newy -= step_size
            self.orientation = 1
        if self.movekeys[2] in Test_Window.keysPressed:
            newx += step_size
            self.orientation = 2
        if self.movekeys[3] in Test_Window.keysPressed:
            newx -= step_size
            self.orientation = 3
        
        self.player.pos = (newx, newy)
        self.pos = (newx, newy)
        
        if self.collide_widget(p2):
            print("Colliding")
        
            
        
class Test_Window(Widget):
    
    keysPressed = set() #create set to store values of keys being pressed

    
    def __init__(self, playerone, playertwo, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.background = Rectangle(source = 'background.png', pos = self.pos, size = (1000, 1000))
        self.add_widget(playertwo)
        self.add_widget(playerone)
        
        self.playerone = playerone
        self.playertwo = playertwo
        
        self.winner = ""
        
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down = self._on_key_down) #binding key press to callback function
        self._keyboard.bind(on_key_up = self._on_key_up)
        
        
            
        
        Clock.schedule_interval(partial(playerone.move_step, playertwo), 0)
        Clock.schedule_interval(partial(playertwo.move_step, playerone), 0)
        
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down = self._on_key_down)
        self._keyboard.unbind(on_key_up = self._on_key_up)
        self._keyboard = None
        
    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.keysPressed.add(text)
        
         
        
    def _on_key_up(self, keyboard, keycode):
        inpud = keycode[1]
        if inpud in self.keysPressed:
            print(keycode)
            self.keysPressed.remove(inpud)
        
p1 = Test_object()
p2 = Test_object("iklj")
game = Test_Window(p1, p2)        
        
class TestApp(App):
    def build(self):
        return game
    
test = TestApp()
test.run()
