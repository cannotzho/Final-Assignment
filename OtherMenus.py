# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 22:03:15 2020

@author: Ken Zho
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
import FightArea as FA
import Character as char
import Weapon as W


class MainMenu(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        BL = BoxLayout()
        BL.orientation = "vertical"
        BL.size_hint = (0.4, 0.4)
        BL.pos = (200, 200)
        play_button = Button(text = "Play")
        play_button.bind(on_press = self.playgame)
        settings_button = Button(text = "Credits")
        settings_button.bind(on_press = self.go_to_credits)
        
        
        BL.add_widget(play_button)
        BL.add_widget(settings_button)
        self.add_widget(BL)
    def playgame(self, *args):
        self.manager.current = "game_settings"
    def go_to_credits(self, *args):
        self.manager.current = "game_credits"
        
        
class Controls(Screen):
    
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.newfight = ObjectProperty(None)
        self.move_labels = ["up", "down", "right", "left", "attack", "roll", "special"]
        
        BL = BoxLayout()
        BL.orientation = "vertical"
        
        #Create Gridlayout for 2 columns for all character options
        GL = GridLayout()
        GL.cols = 2
        self.weap1 = W.Sword
        self.weap2 = W.Sword
        self.player1_choice = 1
        self.player2_choice = 1
        #Row 1 of widgets in Gridlayout, textline input to change control scheme (pretty bad right now, change later)
        self.newtext1 = TextInput(multiline = False)
        self.newtext1.size_hint = (1, 0.2)
        GL.add_widget(self.newtext1)
        
        self.newtext2 = TextInput(multiline = False)
        self.newtext2.size_hint = (1, 0.2)
        GL.add_widget(self.newtext2)
        
        #Row 2 of widgets in Gridlayout, button to submit textinput to change controls. Again, needs an improvement
        self.confirm_button1 = Button(text = "Confirm Player 1 controls: wsdaert(default)")
        self.confirm_button1.bind(on_press = self.change_controls1)
        GL.add_widget(self.confirm_button1)        
                        
        self.confirm_button2 = Button(text = "Confirm Player 2 controls: ol;kp[](default)")
        self.confirm_button2.bind(on_press = self.change_controls2)
        GL.add_widget(self.confirm_button2)
        
        #Row 3 of widgets in Gridlayout, includes character choices (purely cosmetic)
        P1_characters = BoxLayout()
        
        self.character1_button1 = Button(background_normal = "knight 1.png")
        self.character1_button1.bind(on_press = self.p1_change_char1)
        P1_characters.add_widget(self.character1_button1)        
                        
        self.character1_button2 = Button(background_normal = "knight 2.png")
        self.character1_button2.bind(on_press = self.p1_change_char2)
        P1_characters.add_widget(self.character1_button2)
        
        GL.add_widget(P1_characters)
        
        P2_characters = BoxLayout()
        
        self.character2_button1 = Button(background_normal = "knight 1.png")
        self.character2_button1.bind(on_press = self.p2_change_char1)
        P2_characters.add_widget(self.character2_button1)        
                        
        self.character2_button2 = Button(background_normal = "knight 2.png")
        self.character2_button2.bind(on_press = self.p2_change_char2)
        P2_characters.add_widget(self.character2_button2)
        
        GL.add_widget(P2_characters)
        
        #Row 4 of widgets in GridLayout
        GLP1 = GridLayout()
        GLP1.cols = 2
        BLP1 = BoxLayout()
        BLP1.orientation = "vertical"
        player1moves = "wsdazxc"
        self.player1labels = []
        for i, j in enumerate(player1moves):
            newbutt = Label(text = "{:6}: {:1}".format(self.move_labels[i], j))
            self.player1labels.append(newbutt)
            BLP1.add_widget(newbutt)
                            
        GLP1.add_widget(BLP1)
        
        BL2P1 = BoxLayout()
        BL2P1.orientation = "vertical"
        
        sword_select1 = Button(text = "Sword \n Special: Parry")
        sword_select1.bind(on_press = self.choose_sword1)        
        BL2P1.add_widget(sword_select1)
        
        lance_select1 = Button(text = "Lance \n Special: Guard")
        lance_select1.bind(on_press = self.choose_lance1)
        BL2P1.add_widget(lance_select1)
        
        hammer_select1 = Button(text = "Great Hammer \n Special: Smash")
        hammer_select1.bind(on_press = self.choose_hammer1)
        BL2P1.add_widget(hammer_select1)
        
        GLP1.add_widget(BL2P1)
        
        GL.add_widget(GLP1)
        
        GLP2 = GridLayout()
        GLP2.cols = 2
        BLP2 = BoxLayout()
        BLP2.orientation = "vertical"
        player2moves = "ol;kp[]"
        self.player2labels = []
        for i, j in enumerate(player2moves):
            newbutt = Label(text = "{:6}: {:1}".format(self.move_labels[i], j))
            self.player2labels.append(newbutt)
            BLP2.add_widget(newbutt)
        
        GLP2.add_widget(BLP2)
        
        BL2P2 = BoxLayout()
        BL2P2.orientation = "vertical"
        BL2P2.weapon_choice = W.Sword
        sword_select2 = Button(text = "Sword \n Special: Parry")
        sword_select2.bind(on_press = self.choose_sword2)
        BL2P2.add_widget(sword_select2)
        
        lance_select2 = Button(text = "Lance \n Special: Guard")
        lance_select2.bind(on_press = self.choose_lance2)
        BL2P2.add_widget(lance_select2)
        
        hammer_select2 = Button(text = "Great Hammer \n Special: Smash")
        hammer_select2.bind(on_press = self.choose_hammer2)
        BL2P2.add_widget(hammer_select2)

        
        GLP2.add_widget(BL2P2)
        
        GL.add_widget(GLP2)
        
        BL.add_widget(GL)
        
        #Row 2 of Overall Boxlayout, for the play button
        
        self.play_button = Button(text = "Play", size_hint = (1, 0.2))
        self.play_button.bind(on_press = self.playgame)
        BL.add_widget(self.play_button)
        
        
        self.add_widget(BL)
        
    def choose_sword1(self, *args):
        self.weap1 = W.Sword
        self.confirm_button1.text = "Confirm Player 1 controls: {:10} \n Weapon choice: Sword".format(self.newtext1.text)
        
    def choose_lance1(self, *args):
        self.weap1 = W.Lance
        self.confirm_button1.text = "Confirm Player 1 controls: {:10} \n Weapon choice: Lance".format(self.newtext1.text)
        
    def choose_hammer1(self, *args):
        self.weap1 = W.Hammer
        self.confirm_button1.text = "Confirm Player 1 controls: {:10} \n Weapon choice: Hammer".format(self.newtext1.text)
        
    def choose_sword2(self, *args):
        self.weap2 = W.Sword
        self.confirm_button2.text = "Confirm Player 1 controls: {:10} \n Weapon choice: Sword".format(self.newtext2.text)
        
    def choose_lance2(self, *args):
        self.weap2 = W.Lance
        self.confirm_button2.text = "Confirm Player 1 controls: {:10} \n Weapon choice: Lance".format(self.newtext2.text)
        
    def choose_hammer2(self, *args):
        self.weap2 = W.Hammer
        self.confirm_button2.text = "Confirm Player 1 controls: {:10} \n Weapon choice: Hammer".format(self.newtext2.text)
        
        
        
        
    def playgame(self, *args):
        #Checks for valid player controls before game can start
        
        play_valid = True
        for i in self.newtext1.text:
            if i in self.newtext2.text:
                play_valid = False
                self.play_button.text = "Players cannot share controls!"
            if self.newtext1.text.count(i) != 1:
                play_valid = False
                self.play_button.text = "Do not repeat control buttons!"
                
        for i in self.newtext2.text:
            if self.newtext2.text.count(i) != 1:
                play_valid = False
                self.play_button.text = "Do not repeat control buttons!"
        if len(self.newtext1.text) != 7 or len(self.newtext2.text) !=7:
            play_valid = False
            self.play_button.text = "Please enter 7 characters"
        #Remove any previous instances of games
        try:
            self.parent.remove_widget(self.newfight)
        except:
            pass
        
        if len(self.newtext1.text) ==  0 and len(self.newtext2.text) == 0:
            playerone = char.Character((100, 300), list("wsdaert"), self.weap1, name = "P1", character_number = self.player1_choice)
            playertwo = char.Character((500, 300),list("ol;kp[]"), self.weap2, name = "P2", character_number = self.player2_choice)
            self.newfight = FA.FightArea(playerone, playertwo, name = "game_area")
            self.parent.add_widget(self.newfight)
            self.manager.current = "game_area"
        if play_valid:
        
            playerone = char.Character((100, 300), list(self.newtext1.text), self.weap1, name = "P1", character_number = self.player1_choice)
            playertwo = char.Character((500, 300),list(self.newtext2.text), self.weap2, name = "P2", character_number = self.player2_choice)
            self.newfight = FA.FightArea(playerone, playertwo, name = "game_area")
            self.parent.add_widget(self.newfight)
            #self.parent.add_widget(FA.FightArea(playerone, playertwo, name = "game_area"))
            self.manager.current = "game_area"
        
            
            
        
    def change_controls1(self, *args):
        player1moves = self.newtext1.text
        for i, j in enumerate(player1moves):
            try:
                self.player1labels[i].text = "{:6}: {:1}".format(self.move_labels[i], j)
            except:
                pass
        self.confirm_button1.text = "Confirm Player 1 controls: {:10}".format(self.newtext1.text)
        
    def change_controls2(self, *args):
        player2moves = self.newtext2.text
        for i, j in enumerate(player2moves):
            try:
                self.player2labels[i].text = "{:6}: {:1}".format(self.move_labels[i], j)
            except:
                pass
        self.confirm_button2.text = "Confirm Player 2 controls: {:10}".format(self.newtext2.text)                
        
    def p1_change_char1(self, *args):
        self.player1_choice = 1
        
    def p1_change_char2(self, *args):
        self.player1_choice = 2
        
    def p2_change_char1(self, *args):
        self.player2_choice = 1
        
    def p2_change_char2(self, *args):
        self.player2_choice = 2
        
        
class Credits(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.back_button = Button(text = "Art by Jovin Lim Jing Kai \n Hey Brudderrrrr")
        self.back_button.bind(on_press = self.go_back)
        self.add_widget(self.back_button)
        
    def go_back(self, *args):
        self.manager.current = "menu"
        
        
