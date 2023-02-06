try:
    #kivy.require('2.1.0')  ## -2023/01/06-

    # BASELINE IMPORTS
    import threading
    import time
    import os
    import socket

    # LOCAL IMPORTS
    from file_handle import File_man

    # LOCAL SCREENS
    from mygps import MyGPS


    # KIVY IMPORTS
    from kivy.clock import Clock, mainthread
    from kivy.logger import Logger

    # KIVY_UIX IMPORTS
    #from kivy.uix.screenmanager import NoTransition, Screen, ScreenManager

    #   # LAYOUTS_&_VIEWS
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivy.uix.recycleview import RecycleView

    #   # DATA_PROPERTIES
    import kivy.properties
    from kivy.properties import ObjectProperty, StringProperty

    # UTILS => PLATFORM
    from kivy.utils import platform


    # TDD

    import plyer
    from plyer import gps


    from kivy.logger import Logger

except Exception as e:
    print(f"!![ERROR]!!\n[IMPORTS]::[>{str(e)}<]")
    File_man().write_file("IMPORT_ERROR_.txt", "ATTEMPTED", "\n", "w")


#*********************************************************************************************************
#   GPS SCREEN -> KIVY_GARDEN'N
#*********************************************************************************************************
#
#*********************************************************************************************************
##  $   ## SCREEN ##
#*********************************************************************************************************
#
class MyGPS(**kwargs):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.FM = File_man()
        self.gps_co_orts = ""
        self.gps_stats_ = ""
        

    def on_enter(self):
        What_Now = str(self.FM.read_file("WHAT_NOW.txt", "&"))
        self.ids['test_gps'].text = What_Now
        if platform == "android" or platform == "ios":
            try:
                self.gps_co_orts = str(self.FM.read_file("MY_CORTS.txt", "&"))
                try:
                    if self.gps_co_orts:
                        self.ids['stderr_1'].text = self.gps_stats_
                except:
                    self.ids['stderr_1'].text = "[NO_DATA]"
                self.gps_stats_ = str(self.FM.read_file("MY_STAT.txt", "&"))
                try:
                   if self.gps_stats_:
                       self.ids['stderr_2'].text = self.gps_co_orts
                except:
                    self.ids['stderr_2'].text = "[NO_DATA]"


                self.FM.write_file("_Going_On_", "", "\n", "w")
            except Exception as e:
                print(f"[ERROR]:[ON_ENTER]:[MyGPS]::[{str(e)}]")
                self.FM.write_file(f"No_Go__{str(e)}_OON", "", "\n", "w")
        else:
            print("[No_Comptea]")




##*********************************************************************************************************
#
    def goto_loading(self):
        MDApp.get_running_app().root.current = 'loading'
        # Clock.unschedule(self.go_on)

    def goto_test_conn(self):
        MDApp.get_running_app().root.current = 'test_conns'
        # Clock.unschedule(self.go_on)
#
#*********************************************************************************************************
#*
#*********************************************************************************************************
