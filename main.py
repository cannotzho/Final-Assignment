# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 13:59:58 2020

@author: Ken Zho
"""

from kivy.app import App

import OtherMenus as M
from kivy.uix.screenmanager import ScreenManager



 
        
screen_manager = ScreenManager()


# Add the screens to the manager and then supply a name
# that is used to switch screens
screen_manager.add_widget(M.MainMenu(name="menu"))
screen_manager.add_widget(M.Controls(name="game_settings"))
screen_manager.add_widget(M.Credits(name="game_credits"))
#screen_manager.add_widget(FA.FightArea(playerone, playertwo, name = "game_area"))

            
    






class SimpleFight(App):
    
    def build(self):
        return screen_manager
    
if __name__ == "__main__":
    app = SimpleFight()
    app.run()