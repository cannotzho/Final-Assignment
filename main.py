# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 13:59:58 2020

@author: Ken Zho
"""

from kivy.app import App
import Character as char
import FightArea as FA




    
        
        

            
    

playertwo = char.Character((300,0), list("ijklm"))
playerone = char.Character()
box = FA.FightArea(playerone, playertwo)



class SimpleFight(App):
    def build(self):
        return box
    
if __name__ == "__main__":
    app = SimpleFight()
    app.run()