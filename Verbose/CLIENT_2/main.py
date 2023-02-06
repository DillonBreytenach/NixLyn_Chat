try:
    #kivy.require('2.1.0')  ## -2023/01/06-

    #   BASELINE IMPORTS
    import threading
    import time
    import os
    import socket

    #   LOCAL IMPORTS
    #from conns import connections
    from file_handle import File_man

    #   KIVY IMPORTS
    import kivymd
    from kivymd.app import MDApp
    from kivy.clock import Clock, mainthread
    from kivy.lang import Builder
    from kivy.logger import Logger

    #   KIVY_UIX_BASE
    from kivy.uix.screenmanager import NoTransition, Screen, ScreenManager
    from kivy.uix.popup import Popup

    #   KIVY_UIX
    from kivy.uix.button import Button
    from kivy.uix.popup import Popup


    #   # LAYOUTS_&_VIEWS
    from kivy.uix.recycleview import RecycleView
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.gridlayout import GridLayout
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivymd.uix.gridlayout import MDGridLayout



    #   # DATA_PROPERTIES
    import kivy.properties
    from kivy.properties import ObjectProperty, StringProperty

    # UTILS => PLATFORM
    from kivy.utils import platform

    # TDD
    import plyer
    from plyer import gps

    # UNSURE-DON'T-TOUCH
    from jnius import autoclass
    from kivy.logger import Logger



except Exception as e:
    print(f"!![ERROR]!!\n[IMPORTS]::[>{str(e)}<]")
    File_man().write_file("IMPORT_ERROR_.txt", "ATTEMPTED", "\n", "w")

#
#*********************************************************************************************************
#   GLOBAL_VARIABLES
#*********************************************************************************************************
#
name_ = ""
hold_ = True
zoom_ = 12
co_orts_ = ""
connected_ = False
#
#*********************************************************************************************************
#
#*********************************************************************************************************
#

#*********************************************************************************************************
#   #   CONNECTION_ERROR-@-POPUP
#*********************************************************************************************************
#
class CONNECTION_FAIL(Popup):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()
        msg_ = "[CONNECTION_ERROR]"
        self.FM.write_file("SOCKET_DATA/USER.txt", msg_, "*", "w")
#
#*********************************************************************************************************
#
#*********************************************************************************************************
#
#*********************************************************************************************************
#   #   CONNECTION_ERROR-@-POPUP
#*********************************************************************************************************
#
class CONNECTION_MADE(Popup):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()
        msg_ = "[CONNECTION_MADE]"
        self.FM.write_file("SOCKET_DATA/USER.txt", msg_, "*", "w")
        MDApp.get_running_app().root.current = 'Main_WID'
#
#*********************************************************************************************************
#
#*********************************************************************************************************
#   @POPUPS
#*********************************************************************************************************
#   AUTHS-ALERTS*
#*********************************************************************************************************
#   #   AUTH-SUCCESS
#*********************************************************************************************************
#
class Welcome(Popup):
    print("WELCOME")
#
#*********************************************************************************************************
#   #   AUTH-FAIL
#*********************************************************************************************************
#
class Login_Fail(Popup):
    print("LOGIN_FAIL")
#
#*********************************************************************************************************
#   #   REG-FAIL
#*********************************************************************************************************
#
class Reg_Fail(Popup):
    print("REGISTER_FAILED")
#
#*********************************************************************************************************
#   #   ADD_CONT-FAIL
#*********************************************************************************************************
#
class Add_fail(Popup):
    def __init__(self, **kw):
        super().__init__(**kw)
#
#*********************************************************************************************************
#   #   ADD_CONT-SUCCESS
#*********************************************************************************************************
#
class Add_Success(Popup):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()
        user_data = self.FM.read_file("SOCKET_DATA/USER.txt", "*")
        self.user_name = str(user_data[0])
        msg_ = "CONTS*"+str(self.user_name)
        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", msg_, "*", "w")
#
#*********************************************************************************************************
#
#
#*********************************************************************************************************
#*********************************************************************************************************
#   SCREENS/PAGES
#*********************************************************************************************************
#*********************************************************************************************************
#
#*********************************************************************************************************
#   @FORM FUNCTIONS
#*********************************************************************************************************
#   #   NEW_LOG
#*********************************************************************************************************
#
class New_Log(Screen):
    def back(self):
        MDApp.get_running_app().root.current = 'Home'
#
#*********************************************************************************************************
#   #   SEARCH
#*********************************************************************************************************
#
class Search(Screen):
    def back(self):
        MDApp.get_running_app().root.current = 'Home'
#
#*********************************************************************************************************
#   @MAPS_PAGE-USERS_PAGE
#*********************************************************************************************************
#   #   MAP_LOADOUT
#*********************************************************************************************************
#
#class MapsView(MDGridLayout):
#    def __init__(self, **kw):
#        super(MapsView, self).__init__(**kw)
#        global zoom_
#        global co_orts_
#        print("[ZOOM]:",str(zoom_), "\n[CO_ORTS]:",str(co_orts_))
#        mapview = MapView(zoom=zoom_, lat=-26.06, lon=27.07, size=(800,800))
#        self.add_widget(mapview)
#
#*********************************************************************************************************
#   #   &SCREEN
#*********************************************************************************************************
#
class Maps_Page(Screen):
    def __init__(self, **kw):
        super(Maps_Page, self).__init__(**kw)
        self.FM = File_man()


    def on_enter(self):
        print("[ON_ENTER]:[MAPS_SCREEN]")
        Clock.schedule_interval(self.go_on, 1)


    def go_on(self, inst):
        global name_
        self.ids['USER'].text = name_


    def home(self):
        MDApp.get_running_app().root.current = 'Home'
        Clock.unschedule(self.go_on)

    def my_local(self):
        global co_orts_
        co_orts_ = str(self.FM.read_file("MY_CORTS.txt", "&"))
        lat = str(-26.06)
        lon = str(27.06)
        print(f"[MY_LOACL]: \n   [LAT]:[{lat}]\n  [LON]:[{lon}]")
        print(f"[MY_LOACL]: \n   [CO_ORTS_]:[DATA]:[{co_orts_}]")


    # MAP TOOLS     -->> FIND CORRECT WAY c!:-|
    def zoom_in(self):
        global zoom_
        zoom_-=1
        print("[ZOOM_IN]")

    def zoom_out(self):
        global zoom_
        zoom_+=1
        print("[ZOOM_OUT]")

    def look_up(self):
        pass

    
    # EXIT
    def back(self):
        MDApp.get_running_app().root.current = 'Main_WID'
        Clock.unschedule(self.go_on)
#
#*********************************************************************************************************
#*********************************************************************************************************
#   CHAT_PAGE
#*********************************************************************************************************
#   #   $SCREEN-ADD_CONTACT
#*********************************************************************************************************
class Add_C(Screen):
    added_cont = ObjectProperty(None)
    def __init__(self, **kw):
        super().__init__(**kw)

    def add_c(self):
        self.added_cont = str(0)
        msg_ = "NEW_C*"+str(File_man().read_file("SOCKET_DATA/USER.txt", "*"))[2:-2]+"*"+ str(self.ids.NEW_CONTACT.text)
        print("ADDING_C", str(msg_))
        File_man().write_file("SOCKET_DATA/OUT_BOUND.txt", msg_, "*", "w")
        time.sleep(2)
        ret_val = str(File_man().read_file("SOCKET_DATA/IN_BOUND.txt", "*"))
        if "KHONA" in ret_val or "NOT_FOUND" in ret_val:
            self.added_cont = '1'
            print("ADDING_CONTACT_FAILED")
            Add_fail().open()

        elif "ADD_C" in ret_val:
            self.added_cont = '1'
            print("CONTACT_ADDED_SUCCESSFULLAI")
            Add_Success().open()
        


    def back(self):
        MDApp.get_running_app().root.current = 'Home'
#
#*********************************************************************************************************
#   #   MSGS_LIST-ITEMS-OPTINS
#*********************************************************************************************************
#
class Chat_Msg(MDGridLayout):
    
    root_widget = ObjectProperty()
    user_m = StringProperty()
    msg_text = StringProperty()
    msg_dt = StringProperty()
    side = StringProperty()


    def on_release(self, **kwargs):
        super().on_release(**kwargs)
        self.FM = File_man()
        print("MSG_:ON_R: ", str(self.text))
#
#*********************************************************************************************************
#   #   MSGS_LIST-SCROLLER
#*********************************************************************************************************
#
class Scroll_Chats(RecycleView): 
    def __init__(self, **kw):
        super(Scroll_Chats, self).__init__(**kw)
        self.FM = File_man()
        self.init_data = ""
        self.target_user = ""

        self.user_ = ""
        self.msg_ = ""
        self.msg_dt = ""
        self.side = ""


        print("[Scroll_Chats]:: INIT")
        Clock.schedule_interval(self.go_on, 1)

        # trigger variable

    def display_msg(self, msg_stack):
        for i, msg in enumerate(msg_stack):
            print(f'[I]:[{str(i)}]:\n    >>[MSG_VAL]:[{str(msg)}]')



    def go_on(self, inst):
        global hold_
        if hold_ == True:
            return
        try:
            user_data = self.FM.read_file("CHATS/CURRENT.txt", "*")
            if user_data:
                self.target_user = str(user_data[0])
                user_data = self.FM.read_file("SOCKET_DATA/USER.txt", "*")
                user_name = str(user_data[0])
                get_msgs = "MSG_OF*"+str(user_name)+"*"+str(self.target_user)+"*^"
                self.FM.write_file("SOCKET_DATA/MSG_TO.txt", get_msgs, "*", "w")
                chat = self.FM.read_file(f"MSGS/{str(self.target_user)}.txt", "$")



                if chat:
                    self.data = [{
                                'user_m': str(x.split('*')[0]),
                                'msg_text': str(x.split('*')[2]),
                                'msg_dt': str(x.split('*')[3]),
                                "side": "left" if x.split('*')[0] == self.target_user else "right",
                                "root_widget": self}
                                    for x in chat if x]
                    self.display_msg(chat)
        except Exception as e:
            print("[ERROR]:[SCROLL_CHATS]:", str(e))


    def goToUpdate(self):
        print("INST:goT: ")
#
#*********************************************************************************************************
#   #   $SCREEN
#*********************************************************************************************************
#
class Chats(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()
        self.state = ""
        self.target_user = ""

    def on_enter(self):
        print("[ON_ENTER]:CHATS_SCREEN")
        if "Home" not in self.FM.read_file("CHATS/CURRENT.txt", "&"):
            Clock.schedule_interval(self.go_on, 1)

    def go_on(self, inst):
        user_data = self.FM.read_file("CHATS/CURRENT.txt", "*")
        self.target_user = str(user_data[0])
        self.ids['TARGET_USER'].text = str(self.target_user)
        self.chat_info()

    def send_it(self):
        user_data = self.FM.read_file("SOCKET_DATA/USER.txt", "*")
        self.user_name = str(user_data[0])
        msg_out = str(self.ids['MSG_OUT'].text)
        to_send = "MSG_TO*"+str(self.target_user)+"*"+self.user_name+"*"+msg_out+"*"
        #print("\nSEND:\n >> ", to_send)
        self.FM.write_file("SOCKET_DATA/MSG_TO.txt", to_send, "&", "w")
        # REMEMBER TO CLEAR THE InputText
        time.sleep(0.5)
        self.ids['MSG_OUT'].text = ""

    def chat_info(self):
        global hold_
        hold_ = False
        #print("[CHAT_INFO]")
        msg_ = "GET_STATE*"+str(self.target_user)+"*"+str(self.FM.read_file("CHATS/CURRENT.txt", "&")[0])
        #print("[GET_STATE]:: ", str(msg_))

        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", msg_, "*", "w")
        #print("CHATS_TO_BE_DONE")
        self.state = self.FM.read_file("CHATS/TARGET_STATE.txt", "*")
        #print("SELF.STATE:: ", str(self.state))
        try:
            print("[GET_CONT_STAT]:", str(self.state))
            if "OFFLINE" in  str(self.state[2]):
                self.ids['USER_STATUS'].text = str(self.state[1])
            else:
                # ToDo: Check if Date isToday, if so, Calc how many min, sec, hours ago...
                self.ids['USER_STATUS'].text = str(self.state[2])
            get_msgs = "MSG_OF*"+str(name_)+"*"+str(self.target_user)+"*^^"
            self.FM.write_file("SOCKET_DATA/MSG_TO.txt", get_msgs, "&", "w")
        except:
            print("TARGET_STATE_NOT_YET_LOADED")
        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", msg_, "*", "w")

    def home(self):
        global hold_
        hold_ = True

        self.FM.write_file("CHATS/CURRENT.txt", "", "&", "w")
        MDApp.get_running_app().root.current = 'Home'
        Clock.unschedule(self.go_on)

    def contacts(self):
        global hold_
        hold_ = True

        self.FM.write_file("CHATS/CURRENT.txt", "", "&", "w")
        MDApp.get_running_app().root.current = 'Contacts'
        Clock.unschedule(self.go_on)

    def back(self):
        global hold_
        hold_ = True

        self.FM.write_file("CHATS/CURRENT.txt", "", "&", "w")
        user_data = self.FM.read_file("SOCKET_DATA/USER.txt", "*")
        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", "LOGOUT*"+str(user_data)[2:-2]+"*OFFLINE", "*", "w")
        MDApp.get_running_app().root.current = 'Main_WID'
        Clock.unschedule(self.go_on)
#
#*********************************************************************************************************
#*********************************************************************************************************
#
#*********************************************************************************************************
#   CONTACTS_PAGE
#*********************************************************************************************************
#   #   CONTACT_LIST-ITEMS
#*********************************************************************************************************
#
class TwoButtons(BoxLayout):
    # The viewclass definitions, and property definitions.
    left_text = StringProperty()
    right_text = StringProperty()

    def go_chat(self, name):
        #super().on_release(**kwargs)
        #self.FM = File_man()
        print("INST:ON_R: ", str(name))
        if len(File_man().read_file("CHATS/CURRENT.txt", "&")) == 0:
            if name:
                File_man().write_file(f"MSGS/{str(name)}.txt", time, "", "a+")
            print("OPENING_CHATS", str(name))
            File_man().write_file("CHATS/CURRENT.txt", str(name), "&", "w")
            MDApp.get_running_app().root.current = 'Chats'
        else:
            File_man().write_file("CHATS/CURRENT.txt", "", "&", "w")
#
#*********************************************************************************************************
#   #   CONTACT_LIST-SCROLLER
#*********************************************************************************************************
#
class Scroll_Me(RecycleView):
    def __init__(self, **kw):
        super(Scroll_Me, self).__init__(**kw)
        # GET SCREEN NAME HERE
        self.FM = File_man()
        print("[Scroll_Me]:: INIT")
        self.name = ""
        self.time = ""
        Clock.schedule_interval(self.go_on, 1)

    def current(self, inst):
        print("INST:: ", str(inst))


    def go_on(self, inst):

        global name_

        if name_:
            msg_ = "CONTS*"+str(name_)
            self.FM.write_file("SOCKET_DATA/CONTS.txt", msg_, "*", "w")

        #print("[Scroll_Me]::[Go_On]")
        contacts = self.FM.read_file("CHATS/CONTS.txt", "%")[:-1]
        if "EMPTY" not in str(contacts):
            try:
                self.data = [{
                            'left_text': str(x.split('*')[0]),
                            'right_text': str(x.split('*')[2]) if "OFFLINE" not in str(x.split('*')[2]) else str(x.split('*')[1]),
                            "root_widget": self}
                                for x in contacts if x]
            except Exception as e:
                print(f"[ERROR]:[LOADING_SCROLLER]:[CONTACTS]:[>{str(e)}<]")
        self.get_conts()

    def get_conts(self):
        global name_
        if name_:
            msg_ = "CONTS*"+str(name_)+"^^"
            self.FM.write_file("SOCKET_DATA/CONTS.txt", msg_, "*", "w")




    def goToUpdate(self):
        print("INST:goT: ")
#
#*********************************************************************************************************
#   #   $SCREEN
#*********************************************************************************************************
#
class Contacts(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()

    def on_enter(self):
        print("[ON_ENTER]:CONTACTS_SCREEN")
        Clock.schedule_interval(self.go_on, 1)

    def go_on(self, inst):
        global name_
        self.ids['USER'].text = name_
        self.get_conts()


    def add_c(self):
        print("ADDING_CONTACT -> SCREEN")
        MDApp.get_running_app().root.current = 'add_c'


    def get_conts(self):
        global name_
        if name_:
            msg_ = "CONTS*"+str(name_)
            self.FM.write_file("SOCKET_DATA/CONTS.txt", msg_, "*", "w")

    def home(self):
        MDApp.get_running_app().root.current = 'Home'
        Clock.unschedule(self.go_on)

    def back(self):
        user_data = self.FM.read_file("SOCKET_DATA/USER.txt", "*")
        self.FM.write_file("CHATS/CURRENT.txt", "Home", "&", "w")
        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", "LOGOUT*"+str(user_data)[2:-2]+"*OFFLINE", "*", "w")
        MDApp.get_running_app().root.current = 'Main_WID'
        Clock.unschedule(self.go_on)
#
#*********************************************************************************************************
#






#*********************************************************************************************************
#*********************************************************************************************************
#
#       ADMIN_DEV_SECT
#
#*********************************************************************************************************
#*********************************************************************************************************
#   TEST_CONNECTIONS -> IP_PORT-PING
#*********************************************************************************************************
#
#*********************************************************************************************************
####        # SCREEN
#*********************************************************************************************************
#
class Test_Conn(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()
        self.dir_test_count = 0
        self.test_ip = ""
        self.test_port = 0


    def on_enter(self):
        try:
            from conns import connections
            self.test_conns()
        except Exception as e:
            print(f"[CONN_ERROR]::[>{str(e)}<]")
            self.FM.write_file("ERRORS/CONNS_TEST.fss", str(e), "\n", "w")
            pass


    #def test_conns(self):
        #try:
        #    self.conn = connections()
        #    self.ids['conn_act'].text = f"[IMPORTED]::[CONNS]"
        #except Exception as e:
        #    self.ids['conn_act'].text = f"[FAILED]::[CONNS]&&[IMPORT]::[>{str(e)}<]"
        #    print(f"[FAILED]::[CONNS]&&[IMPORT]::[>{str(e)}<]")

    def g_ping(self):
        try:
            import socket
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except Exception as e:
            print(f"[ERROR]::[G_PING]::[SOCK_FAIL]\n !![>{str(e)}<]\n!![<{ping_ret}>]!!\n")
            self.ids['conn_act'].text = f"!![ERROR]!![G_PING]::[SOCK_FAIL]::[>{str(e)}<]"
            pass

        try:
            self.ids['conn_act'].text = f"[TESTING...]"
            ping_ret = self.check('google.com',443,timeout=1)
            print(f"[G_PING]::[<{ping_ret}>]")
            self.ids['conn_act'].text = f"[G_PING]:['GOOGLE.COM']:[443]::[<{ping_ret}>]"
        except Exception as e:
            print(f"[ERROR]::[G_PING_TEST]\n !![>{str(e)}<]\n!![<{ping_ret}>]!!\n")
            self.ids['conn_act'].text = f"!![ERROR]!![G_PING]::[>{str(e)}<]"
            pass
        self.sock.close()

    def ping_test(self):
        try:
            import socket
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except Exception as e:
            print(f"[ERROR]::[MY_PING]::[SOCK_FAIL]\n !![>{str(e)}<]\n!![<{ping_ret}>]!!\n")
            self.ids['conn_act1'].text = f"!![ERROR]!![MY_PING]::[SOCK_FAIL]::[>{str(e)}<]"
            pass
        try:
            ping_ret = False
            my_ping = False

            test_ip = str(self.ids['TEST_IP'].text)
            test_port = int(self.ids['TEST_PORT'].text)

            self.ids['test_conn'].text = f"[TEST_PING]-[IP][>{test_ip}<]-[PORT]:[>{test_port}<]"
            print(f"\n[TEST_PING]----\n-->>[IP]>>[>{test_ip}<]\n   -->>[PORT]>>[>{test_port}<]\n==================\n")


            if test_ip:
                try:
                    self.ids['conn_act1'].text = f"[TESTING...]"
                    my_ping = self.check(str(test_ip),int(test_port),timeout=1)
                    print(f"[MY_PING]::[>{str(my_ping)}<]")
                    self.ids['conn_act1'].text = f"[MY_PING]::[>{test_port}<]::[<{str(my_ping)}>]"
                except Exception as e:
                    print(f"[ERROR]::[MY_PING_TEST]::[>{str(e)}<]")
                    self.ids['conn_act1'].text = f"!![ERROR]!![MY_PING]::[>{str(e)}<]"
                    pass
            else:
                self.ids['conn_act1'].text = f"[NO]::[IP_or_DOMAIN]::[GIVEN]"
                pass


            print("\n==============================\n")
        except Exception as e:
            print(f"[ERROR]::[TEST_PING]::[>{str(e)}<]")
        self.sock.close()

    def latency_test(self):
        try:
            import socket
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            test_ip = str(self.ids['TEST_IP'].text)
            test_port = int(self.ids['TEST_PORT'].text)
            self.ids['test_conn'].text = f"[TEST_PING]-[IP][>{test_ip}<]-[PORT]:[>{test_port}<]"
            print(f"\n[TEST_PING]----\n-->>[IP]>>[>{test_ip}<]\n   -->>[PORT]>>[>{test_port}<]\n==================\n")
        except Exception as e:
            print(f"[ERROR]::[LATENCY]::[SOCK_FAIL]\n !![>{str(e)}<]\n!![<{ping_ret}>]!!\n")
            self.ids['conn_act2'].text = f"!![ERROR]!![LATENCY]::[SOCK_FAIL]::[>{str(e)}<]"
            return
        try:
            self.ids['conn_act2'].text = f"[TESTING...]"
            [my_stat_er, my_stat_re] = self.timed_stats_check(test_ip,test_port,timeout=1)
            print(f"[TEST_STAT]::[>{str(my_stat_er)}<]::[>{str(my_stat_re)}<]")
            self.ids['conn_act2'].text = f"[STATS]:[ER]:[>{my_stat_er}<]:[RT]:[>{my_stat_re}<]"
        except Exception as e:
            print(f"[ERROR]::[TEST_TIMED_STATS_CHECK]::[>{str(e)}<]")
            self.ids['conn_act2'].text = f"!![ERROR]!![MY_STATS_TEST]::[>{str(e)}<]"
            pass
        self.sock.close()

    def check(self, host,port,timeout=2):
        #self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #presumably 
        self.sock.settimeout(timeout)
        try:
           self.sock.connect((host,port))
           #self.sock.send("")
        except:
           return False
        else:
           self.sock.close()
           return True

    def timed_check(self, host,port,timeout=2):
        t0 = time.time()
        if self.check(host,port,timeout):
           return time.time()-t0 # a bit inexact but close enough

    def timed_stats_check(self, host,port,timeout=2,retries=5): 
        try:
            minimum,maximum,sumation = float('inf'),float('-inf'),0
            errors = 0
        except Exception as e:
            print(f"[ERROR]::[TIMED_STATS]::[VARS]\n[>{str(e)}<]")

        try:
            for i in range(retries):
                t = self.timed_check(host,port,timeout)
                if t is None:
                   print("ERROR Unreachable...")
                   errors += 1
                else:
                    print(f"Time {t:0.5f}s")
                    maximum = max(maximum,t)
                    minimum = min(minimum,t)
                    sumation += t
            if retries > 0:
                print(f"Max Time: {maximum:0.5f}s")
                print(f"Min Time: {minimum:0.5f}s")
                print(f"Average: {sumation/(retries-errors):0.2f}s")
            
        except Exception as e:
            print(f"[ERROR]::[TIMED_STATS]::[ALGO]\n[>{str(e)}<]")


        print(f"Failures: {errors}/{retries}")
        return [errors, retries]

    def goto_loading(self):
        MDApp.get_running_app().root.current = 'loading'
        # Clock.unschedule(self.go_on)

    def goto_gps(self):
        MDApp.get_running_app().root.current = 'myGPS'
        # Clock.unschedule(self.go_on)
#*********************************************************************************************************
#
#*********************************************************************************************************
#*********************************************************************************************************
#   LOADING -> ADMIN
#*********************************************************************************************************
#*********************************************************************************************************
####        # BUTTONS -> DYNAMIC_WIDGETS
#*********************************************************************************************************
#
class DirsButtons(BoxLayout):
    # The viewclass definitions, and property definitions.
    dir_fs = StringProperty()
    file_fs = StringProperty()


    def no_(self):
        print("[No...]")

    def read_out(self, name):
        print(f"[ITEM]::[>{str(name)}<]")
#
#*********************************************************************************************************
####        # SCROLLER -> DIRECTORY_INFO
#*********************************************************************************************************
#
class ScrollDirs(RecycleView):
    def __init__(self, **kw):
        super(ScrollDirs, self).__init__(**kw)
        self.FM = File_man()
        self.name = ""
        self.time = ""
        Clock.schedule_interval(self.go_on, 0.5)
        print("[Scroll_Dirs]::[INIT]")

    def current(self, inst):
        print("INST:: ", str(inst))


    def go_on(self, inst):
        #print("[Scroll_Me]::[Go_On]")
        checks = self.FM.read_file("CHECK_SUM.txt", "%")[:-1]

        if "EMPTY" not in str(checks) and len(checks) > 1:
            try:
                self.data = [{
                            'dir_fs': str(x.replace("$DIR#", "")) if "DIR" in str(x) else "||",
                            'file_fs': str(x.replace("$FIL#", "")) if "FIL" in str(x) else "",
                            "root_widget": self}
                                for x in checks]
            except Exception as e:
                print("[erre----]", str(e))


    def go_ToUpdate(self):
        print("INST:goT: ")
#
#*********************************************************************************************************
####        # SCREEN -> DIRECTORY_INTEGRITY_CHECK
#*********************************************************************************************************
#
class LoadingPage(Screen):
    def __init__(self, **kw):
        super(LoadingPage, self).__init__(**kw)
        print("[__INIT__]::[LOADING_SCREEN]")
        self.FM = File_man()
        self.dir_test_count = 0


    # GO_TO GPS PAGE
    def goto_gps(self):
        MDApp.get_running_app().root.current = "myGPS"

    # TEST_SCREEN_SHIFT
    def test_screen(self):
        try:
            #self.ids['load_l2'].text = "[SHIFTING_SCREEN]"
            MDApp.get_running_app().root.current = "test_conns"
        except Exception as e:
            print(f"[ERROR]::[SCREEN_SHIFT]::\n>{str(e)}<")
            self.ids['load_l2'].text = f"[ERROR]::[SCREEN_SHIFT]::\n>{str(e)}<"


    # TEST_DIRECTORY_INTEGRITY
    def test_dirs(self):
        self.ids['load_l1'].text = f"[TEST_DIR]::[CHECKING]=>[PLATFORM]::[>{str(self.dir_test_count)}<]"
        if self.dir_test_count >= 0:
            try:
                toWrite = ""
                isDir = "$DIR#"
                isFil = "$FIL#"
                delim = "%"
                toAdd = ""
                target_dir = []
                # CHECK ANDROID
                myDir = self.FM.file_list(".")
                if myDir:
                    for i, nd in enumerate(myDir):
                        self.ids['load_l2'].text = f"[FILE%DIR]::[>{str(nd)}<]"
                        toAdd = ""
                        print(f"\n###\n[RET_DIR_ITEM]:[{str(i)}]:[>{str(nd)}<]")
                        if "." not in str(nd):
                            try:
                                if self.FM.check_dir(str(nd)):
                                    toAdd = f"{isDir}{str(nd)}{delim}"
                                    print(f"[IsDir]->[>{str(nd)}<]\n[>>{toAdd}<<]\n$$$[CHECK_ITEMS_IN_DIR]\n")
                                    # ADD DIR..
                                    toWrite+=toAdd
                                    toAdd=""
                                    # GET ALL ITEMS OF DIR
                                    target_dir = self.FM.file_list(str(nd))
                                    for t in target_dir:
                                        print(f"[TARGET_DIR]::[ITEM]::[>{str(t)}<]")
                                        if self.FM.check_file(str(nd)+"/"+str(t)):
                                            toAdd = f"{isFil}{str(t)}{delim}"
                                            print(f"[IsFil]->[>{str(t)}<]\n[>>{toAdd}<<]")
                                            toWrite+=toAdd
                                            toAdd=""
                            except:
                                print(f'[NOT_DIR]::[>{str(nd)}<]')
                        else:
                            try:
                                if self.FM.check_file(str(nd)):
                                    toAdd = f"{isFil}{str(nd)}{delim}"
                                    print(f"[IsFil]->[>{str(nd)}<]\n[>>{toAdd}<<]")
                                    toWrite+=toAdd
                                    toAdd=""
                            except:
                                print(f'[NOT_FIL]::[>{str(nd)}<]')
                    

                    self.ids['load_l1'].text = f"[SCAN_COMPLETE]::[FILE%%DIR]::[>{str(myDir)}<]"
                    self.FM.write_file("CHECK_SUM.txt", toWrite, "", "w")

                if platform == "android":
                    self.ids['load_l2'].text = f"[PLATFORM]==[ANDROID]::[TEST_DIR]"
                else:
                    print("[NOT_ANDROID]")
                    self.ids['load_l2'].text = "[NOT_ANDROID]"
            except Exception as e:
                self.ids['load_l1'].text = f"[FAILED]::[DIR_TEST]::[>{str(e)}<]"
                pass

        self.dir_test_count+=1
#
#*********************************************************************************************************
#
#*********************************************************************************************************
#*********************************************************************************************************
#   @ADMIN-GPS
#*********************************************************************************************************
#   #   GPS SCREEN -> PLYER -> GPS
#*********************************************************************************************************
#
#*********************************************************************************************************
####        # SCREEN -> GPS_TEST -> DATA
#*********************************************************************************************************
#
class MyGPS(Screen):
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


    def goto_loading(self):
        MDApp.get_running_app().root.current = 'loading'
        # Clock.unschedule(self.go_on)

    def goto_test_conn(self):
        MDApp.get_running_app().root.current = 'test_conns'
        # Clock.unschedule(self.go_on)
#
#*********************************************************************************************************
#
#*********************************************************************************************************





#
#*********************************************************************************************************
# HOME
#*********************************************************************************************************
#
class Home(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()

    def on_enter(self):
        print("[ON_ENTER]:HOME_SCREEN")
        Clock.schedule_interval(self.ft__, 1)

    def on_start(self, inst):
        print("[ON_START]::[HOME]")
        pass

    def ft__(self, inst):
        user_data = self.FM.read_file("SOCKET_DATA/USER.txt", "*")
        self.ids['USER'].text = str(user_data)[2:-2]

    def chats(self):
        MDApp.get_running_app().root.current = 'Contacts'

    def search(self):
        MDApp.get_running_app().root.current = 'Search'

    def new_log(self):
        MDApp.get_running_app().root.current = 'New_Log'

    def maps_page(self):
        MDApp.get_running_app().root.current = 'Maps'



    def back(self):
        user_data = self.FM.read_file("SOCKET_DATA/USER.txt", "*")
        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", "LOGOUT*"+str(user_data)[2:-2]+"*OFFLINE", "*", "w")
        MDApp.get_running_app().root.current = 'Main_WID'
#
#*********************************************************************************************************
#   #   #AUTH_SYS
#*********************************************************************************************************
#
#*********************************************************************************************************
#   #INITIAL SET_UPs#
#*********************************************************************************************************
#
#*********************************************************************************************************
# LOGIN
#*********************************************************************************************************
#
class Login(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()
    
        

    def login_(self):
        print("LOGGINIG_IN")
        Name = str(self.ids['REP_NAME'].text)
        PSWD = str(self.ids['PSWD'].text)
        data = "LOGIN"+"*"+Name+"*"+PSWD
        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", data, "*", "w")
        self.FM.write_file("SOCKET_DATA/USER.txt", Name, "*", "w")

        global name_
        name_ = Name

        time.sleep(0.5)
        Login_Confirm = self.FM.read_file("SOCKET_DATA/IN_BOUND.txt", "*")
        if "LOGIN" in Login_Confirm:
            print("LOGGED_IN")
            MDApp.get_running_app().root.current = 'Home'
            Welcome().open()

        elif "PSWD_FAIL" in Login_Confirm:
            print("INCORRECT_PASSWORD")
            Login_Fail().open()

        elif "PLEASE_REG" in Login_Confirm:
            print("NOT_LOGGED_IN")
            MDApp.get_running_app().root.current = 'Register'

    def back(self):
        MDApp.get_running_app().root.current = 'Main_WID'
#
#*********************************************************************************************************
# REGISTER
#*********************************************************************************************************
#
class Register(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()

    def Register_(self):
        Name = str(self.ids['REP_NAME'].text)
        PSWD = str(self.ids['PSWD'].text)
        data = "REG*"+Name+"*"+PSWD
        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", data, "*", "w")
        self.FM.write_file("SOCKET_DATA/USER.txt", Name, "*", "w")

        time.sleep(1)
        try:
            Reg_Confirm = self.FM.read_file("SOCKET_DATA/IN_BOUND.txt", "*")
            if "REG_ED" in Reg_Confirm:
                print("REGISTERED")
                Welcome().open()
                MDApp.get_running_app().root.current = 'Home'
            elif "PLEASE_LOGIN" in Reg_Confirm:
                print("PLAESE_LOGIN")
                MDApp.get_running_app().root.current = 'Login'
            elif "FAILED_REG" in Reg_Confirm:
                Reg_Fail().open()
        except Exception as e:
            print("REG_ERROR: ", str(e))

    def back(self):
        MDApp.get_running_app().root.current = 'Main_WID'


    #LOGIN_REGISTER_&& WHATEVER_ELSE...
#
#*********************************************************************************************************
#
#*********************************************************************************************************
#










#
#*********************************************************************************************************
#   MAIN_SCREEN
#*********************************************************************************************************
#
#*********************************************************************************************************
##  $   ## SCREEN ##
#*********************************************************************************************************
# MAIN_WID
class Main_WID(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()

    def on_enter(self):
        print("[^INIT^]::[ON_ENTER]::[MAIN_WID]")


    def check_conn(self):
        MDApp.get_running_app().root.current = 'conn_first'

    def Login(self):
        MDApp.get_running_app().root.current = 'Login'

    def Register(self):
        MDApp.get_running_app().root.current = 'Register'


    def goto_loading(self): # ADD A ADMIN LOGIN SYS -> future..endev
        MDApp.get_running_app().root.current = 'loading'

    def Exit(self):
        sys.exit(1)








class ConnectFirst(Screen):
    #connected = StringProperty("False")
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()


    def get_conn(self):
        self.ids['test_conn'].text = "[CONNECTING..]"
        try:
            test_ip = str(self.ids['TEST_IP'].text)
            test_port = int(self.ids['TEST_PORT'].text)

            #self.ids['test_conn'].text = f"[TEST_CONN]-[IP][>{test_ip}<]-[PORT]:[>{test_port}<]"
            print(f"\n[TEST_PING]----\n-->>[IP]>>[>{test_ip}<]\n   -->>[PORT]>>[>{test_port}<]\n==================\n")


            if len(test_ip) > 1 and test_port > 1:
                print("[START_CONNECTING]..0")
                # ATTEMPT TO IMPORT CONNS_FILE
                from conns import connections
                print("[START_CONNECTING]..1")

                self.conn = connections()
                print("[START_CONNECTING]..2")

                self.conn.start_conn(test_ip, test_port)
                print("[START_CONNECTING]..3")

                self.ids['test_conn'].text = "[CONNECTED]"
                
                CONNECTION_MADE().open()
        except Exception as e:
            print(f"\n\n![!ERROR!]!\n--[CONNECTION_FAILED]--\n[>{str(e)}<]")
            #self.FM.write_file("ERRORS/CONN_MAIN_WID_.fss", str(e), "\n", "w")
            self.ids['test_conn'].text = "[CONNECTION_FAILED]"+str(e)
            time.sleep(0.5)
            CONNECTION_FAIL().open()
            pass






#
#
#*********************************************************************************************************
#
#*********************************************************************************************************
#       ##  EOS  ##
#*********************************************************************************************************
#
#
#*********************************************************************************************************
#
#
#*********************************************************************************************************
#SCREEN_MANAGER
#*********************************************************************************************************
#
class WindowManager(ScreenManager):
    pass
#
#*********************************************************************************************************
#
#
#*********************************************************************************************************
#MAIN
#*********************************************************************************************************
#
class LaunchTestApp(MDApp):
    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')
    is_droid = StringProperty('WAITING FOR GPS')
    perms_  = StringProperty('[&]')

    def __init__(self, **kw):
        super(LaunchTestApp, self).__init__(**kw)
        print("[INIT_STACK_TREE]")
        self.FM = File_man()
        try:
            self.FM.build_tree()
            print("[INIT_BUILD_TREE]")
        except Exception as e:
            print(f"[INIT_ERROR][BUILD_TREE]:[>{str(e)}<]")
        try:
            self.start_up()
            print("[INIT_CLEAN_TREE]")
        except Exception as e:
            print(f"[INIT_ERROR][START_UP]:[>{str(e)}<]")



    def start_up(self):
        # CHECK_SUM
        self.FM.write_file("CHECK_SUM.txt", "EMPTY", "*", "w")

        #SOCKET_DATA
        self.FM.write_file("SOCKET_DATA/IN_BOUND.txt", "", "*", "w")
        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", "", "*", "w")
        self.FM.write_file("SOCKET_DATA/CONTS.txt", "", "*", "w")
        self.FM.write_file("SOCKET_DATA/MSG_TO.txt", "", "*", "w")
        self.FM.write_file("SOCKET_DATA/MSG_OF.txt", "", "*", "w")

        #CHATS_DATA
        self.FM.write_file("CHATS/CONTS_STATE.txt", "", "*", "w")
        self.FM.write_file("CHATS/CURRENT.txt", "", "&", "w")
        self.FM.write_file("CHATS/TARGET_STATE.txt", "", "&", "w")


    def get_perms(self):
        if platform == "android":
            try:
                # GET PERMISSIONS
                try:
                    from android.permissions import request_permissions, Permission
                    request_permissions([Permission.ACCESS_COARSE_LOCATION,Permission.ACCESS_FINE_LOCATION])
                except Exception as e:
                    self.request_local_permission()
                    self.FM.write_file(f"ERRORS/PERMS_DENIED_0.ffs", str(e), "\n", "w")
                print("[PHASE_2]")
            except Exception as e:
                print(f"[ERROR]::[PERMS_DENIED]:[>{str(e)}<]")
                self.FM.write_file(f"ERRORS/PERMS_DENIED_1.ffs", str(e), "\n", "w")


    def request_local_permission(self):
        ask_permission("android.permission.ACCESS_FINE_LOCATION")
        ask_permission("android.permission.ACCESS_COARSE_LOCATION")


    def build(self):
        print("[BUILD_KIVY]")
        if platform == "android":
            try:
                # GPS CONFIG
                gps.configure(on_location=self.on_location, on_status=self.on_status)
                self.FM.write_file("SUCCEEDS/GPS_STARTED.ffs", "GPS", "\n", "w")
            except Exception as e:
                self.FM.write_file("ERRORS/GPS_FAILED.ffs", str(e), "\n", "w")
            try:
                # GET PERMISSIONS
                self.get_perms()
                self.perms_ = '[^]'
            except Exception as e:
                self.gps_status = 'GPS is not implemented for your platform'
                self.FM.write_file("ERRORS/GPS_FAILED.ffs", str(e), "\n", "w")

        kv = Builder.load_file("main.kv")
        return kv

    def hi(self):
        print("Hi..")
        #self.request_local_permission()

    def start(self, minTime, minDistance):
        if platform != "android":
            print("[NO_GPS_DEVICE_FOUND]")
            self.is_droid = "[NO_GPS_DEVICE_FOUND]"
        else:
            gps.start(minTime, minDistance)
            print("[PHASE_START]")

    def stop(self):
        if platform != "android":
            print("[NO_GPS_DEVICE_FOUND]")
        else:
            gps.stop()
            print("[STOPPED]")

    @mainthread
    def on_location(self, **kwargs):
        #self.FM.write_file("WHAT_NOW.txt", str(kwargs), "\n", "w")
        self.gps_location = '\n'.join(['{}={}&'.format(k, v) for k, v in kwargs.items()])


    @mainthread
    def on_status(self, stype, status):
        #self.FM.write_file("MY_STAT.txt", "@"+str(stype)+"#"+str(status), "&", "w")
        self.gps_status = 'type={}\n{}'.format(stype, status)

    def on_pause(self):
        gps.stop()
        return True

    def on_resume(self):
        gps.start()
        pass
#
#
if __name__=="__main__":
    LaunchTestApp().run()
#
#
#*********************************************************************************************************
