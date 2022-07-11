from copyreg import remove_extension
from multiprocessing.sharedctypes import Value
import os,glob,shutil
import json
from turtle import screensize, width
import types
import win32api
import subprocess
from elevate import elevate
import threading
import re
import time
import tkinter
#Pre-configurations for app's layout
from kivy.config import Config 
Config.set('graphics','height','520')
Config.set('graphics','width','900')
Config.set('graphics','position','custom')
Config.set('graphics','top','200')
Config.set('graphics','left','510')
Config.set('graphics','resizable','0')


from kivy.utils import get_color_from_hex
from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle,InstructionGroup,Rectangle
from kivy.properties import StringProperty,ColorProperty,ObjectProperty,ListProperty,NumericProperty
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.uix.screen import Screen
from kivymd.uix.label import MDLabel,MDIcon
from kivymd.uix.list import MDList,ImageLeftWidget,OneLineAvatarListItem,ImageRightWidget
from kivymd.uix.datatables import MDDataTable
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior,HoverBehavior,RectangularRippleBehavior
from kivymd.theming import ThemableBehavior
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager,RiseInTransition,FadeTransition
from kivymd.uix.card import MDCard
from kivy.uix.button import Button
from kivymd.uix.button import MDIconButton
from kivy.uix.scrollview import ScrollView
from kivymd.uix.textfield import MDTextField
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from plyer import filechooser
from kivy.core.text import FONT_BOLD, LabelBase
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.list import OneLineAvatarIconListItem
from kivy.uix.checkbox import CheckBox
LabelBase.register(name='Calibri Light',fn_regular='C:\\Windows\\Fonts\\calibril.ttf')
LabelBase.register(name='Quicksand',fn_regular=r'C:\Users\thuan\AppData\Local\Microsoft\Windows\Fonts\Quicksand-VariableFont_wght.ttf')
LabelBase.register(name='Sans Serif',fn_regular=r'C:\Windows\Fonts\micross.ttf')
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

configLocation = r"E:\My Coding Shits\Python Shits\OS Experiments\GUIExperiments\gameLauncher\gameLauncherWithCustomRes\config.json"
configData = json.load(open(configLocation))

screenProperties = """
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
ScreenManager:
    transition: FadeTransition()
    WelcomeScreen:
        name:'welcome'
    AllGamesScreen:
        name:'allGames'
    CustomGameInfo:
        name:'customInfo'

#-----------------LAYOUT SETTINGS (cuz i dunno how to implement these in Python)---------------#
<ItemConfirm>
    on_release: root.set_icon(check)
    CheckboxLeftWidget:
        id: check
        group: "check"
#------------------SCREENS ONLY------------------#
<WelcomeScreen>
    canvas.before:
        Rectangle:
            pos:self.pos
            size:self.size
            source: './images/bg.jpg'    
    Image:
        source: './images/joystick.png'
        pos_hint:{'center_x':0.5,'center_y':0.65}
        size_hint:None,None
        width:90
        height:90
    MDLabel:
        text: "CustRes Launcher"
        font_style: "Caption"
        font_size: 50
        pos:(0,0)
        halign:'center'
        theme_text_color: 'Custom'
        text_color:(255/255,255/255,255/255,1)
    MDLabel:
        text:" V1.0 "
        font_style: "H3"
        font_size:30
        halign:'center'
        pos:(0,-60)
        theme_text_color: 'Custom'
        text_color:(255/255,255/255,255/255,1)

<AllGamesScreen>
    canvas.before:
        Rectangle:
            pos:self.pos
            size:self.size
            source: './images/bg.jpg'   
    MDLabel:
        text:'Games'
        font_style:'H2'
        pos:(45,200)
        theme_text_color: 'Custom'
        text_color:(255/255,255/255,255/255,1)
        font_size:50

    ScrollView: 
        pos_hint:{'center_x':0.558,'center_y':0.43}
        size_hint_y:None
        do_scroll_y:True
        height:350
        width:800
        scroll_wheel_distance:60
        scroll_distance:60

        GridLayout:
            id: listOfGames
            cols:3
            rows:4
            spacing:(80,70)
            size_hint_y:None
            height:700

<CustomGameInfo>  
    canvas.before:
        Rectangle:
            pos:self.pos
            size:self.size
            source: './images/bg.jpg'   
    MDLabel:
        text:'Pre-customizations'
        font_style:'H2'
        pos:(45,200)
        theme_text_color: 'Custom'
        text_color:(255/255,255/255,255/255,1)
        font_size:50



"""
#------------------PER-SCREEN OBJECTS---------------------#
class eachCustomField(FloatLayout):
    gameName = ''
    gameDir = ''
    gameIcon = ''
    def __init__(self,fieldName,iconLoc,fieldPos,fieldXOffset,fieldYOffset,tag,**kwargs):
        super().__init__(**kwargs)    
        x = fieldPos[0] #100
        y = fieldPos[1] #200        


        #For inner configurations
        self.tag = tag
        self.iconLoc = iconLoc
        self.fieldName = fieldName

        with self.canvas.before:
            Color(rgba=(86/255,72/255,139/255,0.8))
            RoundedRectangle(size=(770,80),pos=(x-28,y+70),
                             radius=[(30, 30), (30, 30), (30, 30), (30, 30)])                             
        
        group = FloatLayout(pos=fieldPos)                      
        customIcon = Image(source=self.iconLoc,pos=(x-15,y+75),
                            size_hint=(None,None),width=60,height=60)
        group.add_widget(customIcon)                        
        tag = Label(text=self.fieldName,font_size=30,
                    pos=(x-360+fieldXOffset,y-80),font_name="Quicksand",halign='left')
        group.add_widget(tag)                        
        selectButton = Button(background_normal="./images/open-folder.png",
                              background_down="./images/open-folder-dark.png",
                              size_hint=(None,None),width=65,height=65,pos=(x+650,y+76),
                              border=(0,0,0,0),on_release=self.addingCustomInfo)        
        group.add_widget(selectButton)
        nameGrid = GridLayout(cols=1,rows=1,pos=(x-60,y-130),size=(80,80))
        self.nameLabel = Label(text="",halign='left',
                        font_name="Calibri Light",font_size=32,
                        width=30,text_size=(600,80))
        nameGrid.add_widget(self.nameLabel)
        group.add_widget(nameGrid)        
        
        self.add_widget(group)
    

    def addingCustomInfo(self,*args):            
        #Data to return to each game cards                       
        if self.tag == 0: #Exe picker
            path = []
            try:
                path = filechooser.open_file(title="Choose a game file...", 
                                filters=[("Games", "*.exe")])            
            except Exception as e:
                print(e)
            if len(path) !=0:                                
                gamePath = path[0]
                name = os.path.split(gamePath)[1]                   
                self.nameLabel.text = name 
                                
                eachCustomField.gameName = name               
                eachCustomField.gameDir = gamePath
                
            path = []

        elif self.tag == 1: #Icons Picker
            path = []
            try:
                path = filechooser.open_file(title="Choose an icon file...", 
                                filters=[("Icons", "*.jpg","*.jpeg","*.ico")])            
            except Exception as e:
                print(e)
            if len(path)!=0:          
                iconPath = path[0]                      
                icon = os.path.split(iconPath)[1]  
                self.nameLabel.text = icon
                
                eachCustomField.gameIcon = iconPath
                
            path = []                
        
    def returnInfo(self,mode,*args):     
        if mode==1:   
            print("Current self.gameName: "+self.gameName)         
            return self.gameName
        elif mode==2:    
            print("current self.gameDir:"+self.gameDir)        
            return self.gameDir
        else:          
            print("self.gameicon:" +self.gameIcon)  
            return self.gameIcon
    def resetInfo(self,*args):
        self.gameName = ''
        self.gameIcon = ''
        self.gameDir = ''




class notification(MDDialog):
    customDialogText = ""    
    def __init__(self,inputText,**kwargs):
        super().__init__(**kwargs)
        self.customDialogText = inputText
        self.dialog = MDDialog(
            text="[color=#FFFFFF][size=28][font=Calibri]"
                  +self.customDialogText+"[/color][/size][/font]",
            title="[color=#FFFFFF][size=32][font=Quicksand]"
                  +"Information"+"[/color][/size][/font]",
            md_bg_color=(32/255,42/255,68/255),
            radius=[20,7,20,7],
            size_hint=(None,None),
            width=760,
            height=80,
            buttons=[
                MDFlatButton(
                    text='Okay',
                    on_release=self.closeDialog,
                    theme_text_color='Custom',
                    text_color=(1,1,1,1),
                    font_size=23,
                    pos=(-30,0)
                )
            ]
        )      
        self.add_widget(self.dialog) 
    def closeDialog(self,*args):
        self.dialog.dismiss()

class ItemConfirm(OneLineAvatarIconListItem):
    divider = None
    theme_text_color = 'Custom'
    text_color = (1,1,1,1)
    
    def set_icon(self, instance_check):
        custResButton.custRes = self.text    
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False

       
        
#------------------BUTTONS + CARDS----------------------#
class gameCard(MDCard,RoundedRectangularElevationBehavior,RectangularRippleBehavior):
    deleteMode = 0
    deleteOrCancel = 0
    def __init__(self,gameName,gameIcon,gameDir,**kwargs):
        super().__init__(**kwargs)        
        self.ripple_behavior = True
        self.ripple_duration_in_fast = .1
        self.padding = 16
        self.size_hint = (None,None)
        self.size = ("212dp","110dp")
        self.radius = [20]
        self.elevation = 15
        self.md_bg_color = (86/255,72/255,139/255,0.2)

        
        self.gameDir = gameDir
        self.gameName = gameName
        self.gameIcon = gameIcon
        layout = RelativeLayout(size=self.size)
        img = Image(source=gameIcon,allow_stretch=True,keep_ratio=False,
                    size_hint_x=None,size_hint_y=None,width=60,height=60,pos=(0,8))
        layout.add_widget(img)
        boxLayout = BoxLayout(size=(110,100),pos=(75,-15))
        label = Label(text=gameName,font_name='Sans Serif',
                      pos=(160,-40),font_size=19,size_hint=(None,None),
                      text_size=[100,90],valign='middle',
                      color=(255/255,255/255,255/255,255/255))        
        boxLayout.add_widget(label)
        layout.add_widget(boxLayout)                   
        self.add_widget(layout)

    def on_release(self,*args):
        #Trigger set by allGames screen's delete button, 
        # allowing each icon to change color (to red, indicating delete).               
        if self.deleteMode != 0:
            Clock.schedule_once(self.changeDeleteBG,0.1)        
        else: #If not, everything runs normally.
            Clock.schedule_once(self.newThreads,0.1)  
    #1: Create new game thread + checkGameAlive thread.
    def newThreads(self,*args):     
        gameThread = threading.Thread(target=self.startGame)
        gameThread.daemon = True
        gameThread.start()        

        timerThread = threading.Thread(target=self.checkGameAlive)
        timerThread.daemon = True
        timerThread.start()
    
    #2: Checks if the game is still alive.
    def startGame(self,*args):    
        os.chdir("C:\\qres")
        targetRes = configData["targetResolution"]        
        os.system('qres.exe '+ '/x:' + str(targetRes[0]) + ' /y:' + str(targetRes[1]))       
        location,fileName = os.path.split(self.gameDir)        
        os.chdir(location)   
        os.system(fileName)

    #3: Checks if game is still alive. If not, restore to original res, else, keep running.
    def checkGameAlive(self,*args):                
        #Default resolution
        resCheckRoot = tkinter.Tk()
        defWidth = resCheckRoot.winfo_screenwidth()    
        defHeight = resCheckRoot.winfo_screenheight()
        
        while True:
            print("Game hasn't run yet!")
            gameIsRunning = self.process_exists(self.gameName)
            if gameIsRunning==True:        
                print("Game is now running!")
                break
            time.sleep(3)
        while True:
            print("I am still alive!")
            gameIsRunning = self.process_exists(self.gameName)
            if gameIsRunning==False:   
                os.chdir("C:\\qres")
                os.system('qres.exe '+ '/x:'+str(defWidth)+' /y:'+str(defHeight))    
                print("I am bay màu!")                     
                break
            time.sleep(3)
  
    def process_exists(self,process_name):
        call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
        # use buildin check_output right away
        output = subprocess.check_output(call).decode()
        # check in last line for process name
        last_line = output.strip().split('\r\n')[-1]
        # because Fail message could be translated
        return last_line.lower().startswith(process_name.lower())
    
    def changeDeleteBG(self,*args):      
        if self.deleteOrCancel == 0:
            self.md_bg_color = (255/255,0/255,0/255,0.3)
            self.deleteOrCancel = 1
            gameToDeleteList.append(self.gameName)
            print(gameToDeleteList)
        else:
            self.md_bg_color = (86/255,72/255,139/255,0.2)    
            self.deleteOrCancel = 0
            self.gameNameForDelete = ''
            gameToDeleteList.remove(self.gameName)
            print(gameToDeleteList)


class newGameButton(MDIconButton):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.icon = './images/add.png'
        self.size_hint_x = None
        self.size_hint_y = None
        self.pos_hint = {'center_x':0.80,'center_y':0.88}
        self.user_font_size = "40sp"
        self.ripple_duration_in_fast = 0.1
        self.ripple_scale = 1
        self.ripple_alpha = 0.9
    def on_release(self,*args):
        Clock.schedule_once(self.switchScreen,0.1)
    def switchScreen(self,*args):
        App.get_running_app().root.current='customInfo'


class custResButton(MDIconButton):
    custRes = StringProperty()
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.icon = './images/resolution.png'
        self.size_hint_x = None
        self.size_hint_y = None
        self.pos_hint = {'center_x':0.91,'center_y':0.88}
        self.user_font_size = "60sp"
        self.ripple_duration_in_fast = 0.1
        self.ripple_scale = 1
        self.ripple_alpha = 0.9
    def on_release(self,*args):
        Clock.schedule_once(self.openMenu,0.3)
    def openMenu(self,*args):
        i=0
        res=set()
        try:
            while True:
                ds=win32api.EnumDisplaySettings(None, i)
                res.add(f"{ds.PelsWidth}x{ds.PelsHeight}")
                i+=1
        except: pass
        resList = list(res)
        resListDialogVer = []
        resListDialogVer.sort(reverse=True)
        for res in resList:
            resObj = ItemConfirm(text="[size=23]"+res+"[/size]")
            resListDialogVer.append(resObj)
        
        self.dialog = MDDialog(
                title="[color=#FFFFFF][size=28][font=Calibri]"+"Custom Resolutions"
                       +"[/color][/size][/font]",
                type="confirmation",
                md_bg_color=(32/255,42/255,68/255,1),
                radius=[20,7,20,7],
                items=resListDialogVer,
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=(1,1,1,1),
                        font_size=21,
                        on_release=self.dismiss
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=(1,1,1,1),
                        font_size=21,
                        on_release=self.saveInfo
                    ),
                ],
            )
        self.dialog.open()
    
    def dismiss(self,*args):
        self.dialog.dismiss()
    
    def saveInfo(self,*args):    
        self.dialog.dismiss()            
        regex = re.compile(r'(\d{4}|\d{3})x(\d{4}|\d{3})')
        
        #Updates resolution data into json file
        widthHeightList = list(regex.findall(self.custRes)[0])
        #widthHeightList.remove('x')
        for index in range(0,len(widthHeightList)):
            specInteger = int(widthHeightList[index])
            widthHeightList[index] = specInteger
        configData["targetResolution"] = widthHeightList
        with open(configLocation,"w") as configFile:
            json.dump(configData,configFile)

gameToDeleteList = []        
class removeGameButton(MDIconButton):
    removeMode = 1    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.icon = './images/eraser.png'
        self.size_hint_x = None
        self.size_hint_y = None
        self.pos_hint = {'center_x':0.68,'center_y':0.88}
        self.user_font_size = "40sp"
        self.ripple_duration_in_fast = 0.1
        self.ripple_scale = 1
        self.ripple_alpha = 0.9    
        

    def on_release(self,*args):
        Clock.schedule_once(self.removeGames,0.1)
    
    def removeGames(self,*args):
        gridLayoutTarget = App.get_running_app().root.get_screen('allGames').ids.listOfGames
        gameCardList = gridLayoutTarget.children                
        self.checkbox = CheckBox() 
        if self.removeMode == 1: #If user wants to delete (at first click of this button)
            dialog = notification("Delete Active!\n"+
                                  "Tap on each game until it turns red, then "+
                                  "press Proceed Button to remove."+
                                  " Hit Remove Button once more to cancel."
                                )
            dialog.open()
            for eachGameCard in gameCardList:                               
                eachGameCard.deleteMode = 1                       
            self.removeMode = 0 
            proceedButton = Button(background_normal = './images/next.png',  
                                   background_down = './images/nextDark.png',                                      
                                        size_hint_x = None,
                                        size_hint_y = None,
                                        pos_hint = {'center_x':0.56,'center_y':0.88},
                                        width=75,height=75,        
                                        border=(0,0,0,0),                                                                   
                                        on_release=self.deleteGame)                  
            App.get_running_app().root.get_screen("allGames").add_widget(proceedButton)

        else: #If user doesn't want to delete (second click of this button)
            dialog = notification("Delete Inactive!")
            dialog.open()
            for eachGameCard in gameCardList:                
                eachGameCard.deleteMode = 0  
            self.removeMode = 1    
            objectList = App.get_running_app().root.get_screen("allGames").children                
            App.get_running_app().root.get_screen("allGames").remove_widget(objectList[0])
   
    def deleteGame(self,*args):                
        gameList = App.get_running_app().root.get_screen('allGames').ids.listOfGames.children             
        for delName in gameToDeleteList:           
            for index in range(0,len(gameList)):         
                try:
                    game = gameList[index]        
                    tempName = game.gameName
                    if delName == tempName:
                        #Deletes the game on the GUI's screen
                        print('Game Found!')
                        App.get_running_app().root.get_screen('allGames').ids.listOfGames.remove_widget(game)
                
                        #Updates the json file
                        presavedGames = configData["gameCards"]
                        for index in range(0,len(presavedGames)-1):
                            eachGameDict = presavedGames[index]
                            eachName = eachGameDict["GameName"]
                            if delName==eachName:
                                presavedGames.pop(index)
                        with open(configLocation,"w") as configFile:
                            json.dump(configData,configFile)
                except:
                    print("Lmao")
        
                
#----------------------SCREENS ONLY---------------------#
class WelcomeScreen(Screen):
    def on_enter(self,*args):
        Clock.schedule_once(self.nextScreen,1.5)
    def nextScreen(self,*args):
        self.manager.current = 'allGames'

class AllGamesScreen(Screen):     
    def __init__(self,**kwargs):
        super().__init__(**kwargs)        
        self.addButton = newGameButton()
        self.add_widget(self.addButton)        
        self.customReso = custResButton()       
        self.add_widget(self.customReso)
        self.deleteButton = removeGameButton()
        self.add_widget(self.deleteButton)

        Clock.schedule_once(self.loadGames,0.1)
    
    def loadGames(self,*args):
        #Loads previously added games
        gameList = self.ids.listOfGames        
        gameData = configData["gameCards"]
        for index in range(0,len(gameData)):                        
            eachDataDict = gameData[index]
            gameName = eachDataDict["GameName"]
            gameIcon = eachDataDict["IconDir"]
            gameDir = eachDataDict["GameDir"]
            print(str(gameName+' '+gameIcon+' '+gameDir))
            eachGame = gameCard(gameName,gameIcon,gameDir)
            gameList.add_widget(eachGame)
    
       

class CustomGameInfo(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)           
        field1 = eachCustomField("Step 1. Add Game File",
                                 "./images/console.png",[100,200],40,0,0)
        self.add_widget(field1)
        field2 = eachCustomField("Step 2. Add Icon File",
                                 "./images/image.png",[100,40],30,0,1)            
        self.add_widget(field2)
        
        confirmButton = Button(background_normal="./images/next.png",
                               background_down="./images/nextDark.png",
                               size_hint=(None,None),size=(65,65),border=(0,0,0,0),
                               pos_hint={'center_x':0.91,'center_y':0.88})
        confirmButton.bind(on_release=self.addGame)        
        self.add_widget(confirmButton)
        
        cancelButton = Button(background_normal="./images/xButton.png",
                              background_down="./images/xButtonDark.png",
                              size_hint=(None,None),size=(65,65),border=(0,0,0,0),
                              pos_hint={'center_x':0.8,'center_y':0.88},
                              on_release=self.cancel)
        self.add_widget(cancelButton)
    
    def cancel(self,*args):
        App.get_running_app().root.current = 'allGames'

    def addGame(self,*args):
        dummyObject = eachCustomField("Step 1. Add Game File",
                                      "./images/console.png",[100,200],40,0,0)
        baseApp = App.get_running_app().root        
        baseApp.current = 'allGames'
        gameList = baseApp.get_screen('allGames').ids.listOfGames            
        
        if (len(gameList.children)<12):                        
            gameName = dummyObject.returnInfo(1)                     
            gameDir = dummyObject.returnInfo(2)             
            gameIcon = dummyObject.returnInfo(3) 
            eachGame = gameCard(gameName,gameIcon,gameDir)
            gameList.add_widget(eachGame)    
            dummyObject.resetInfo()

            #Adds new game to json file   
            gameCardData = configData["gameCards"] 
            jsonDataDict = {"GameName":gameName,"GameDir":gameDir,"IconDir":gameIcon}
            gameCardData.append(jsonDataDict)
            with open(configLocation,"w") as configFile:
                json.dump(configData,configFile)
             
        else:
            notif = notification("Only 12 games at max!")
            notif.open()


class GameLauncher(MDApp):        
    def build(self):
        screens = Builder.load_string(screenProperties)
        return screens

app = GameLauncher()
app.run()
