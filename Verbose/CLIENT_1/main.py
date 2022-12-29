#TODO::
#TABS                   [CONTINUOUS]
#LOGIN/REGISTER         [DONE]:[STD]:{NEXT}->{CROSS_ACCOUNT}
#CONTACT_LIST           [DONE]
#CONTACT_STATUS         [DONE]
#MESSAGING              [DONE]:
    #   {ToDo} : {NEW_LINE \n } && {Text_Input -> SHIFT UP ON FOCUS (KEYBOARD)}
#FORMS{DYNAMIC}         []
#MAPS                   [NEXT]
#CALENDER               []
#SEARCH                 [?]



#IMPORTS
try:
    #KIVY STD_UTILS IMPORTS
    import string
    import sys
    #BASELINE IMPORTS
    import threading
    import time

    #PROPERTIES
    import kivy.properties
    from kivy.properties import ObjectProperty, StringProperty

    #KIVY_UIX
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.popup import Popup
    from kivy.uix.recycleview import RecycleView
    from kivy.uix.screenmanager import NoTransition, Screen, ScreenManager
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.tabbedpanel import TabbedPanel

    #KIVY_BASE
    from kivymd.app import MDApp
    from kivy.clock import Clock
    from kivy.core.window import Window
    Window.size = (300, 560)

    from kivymd.uix.gridlayout import MDGridLayout

    from kivy.lang import Builder

    #PROGRAM FILES IMPORTS
    from conns import connections
    from file_handle import File_man


    #from kivy.garden.mapview import MapView, MarkerMap
    from kivy_garden.mapview import MapView




except Exception as e:
    print("[ERROR]:[IMPORTS]", str(e))



name_ = ""
hold_ = True


#POPUPS
#*********************************************************************************************************
class Login_Fail(Popup):
    print("LOGIN_FAIL")
class Welcome(Popup):
    print("WELCOME")
class Reg_Fail(Popup):
    print("REGISTER_FAILED")
# ADD CONT FAIL/SUCCESS
class Add_fail(Popup):
    def __init__(self, **kw):
        super().__init__(**kw)
class Add_Success(Popup):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()
        user_data = self.FM.read_file("SOCKET_DATA/USER.txt", "*")
        self.user_name = str(user_data[0])
        msg_ = "CONTS*"+str(self.user_name)
        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", msg_, "*", "w")


#*********************************************************************************************************
#FORM FUNCTIONS
#*********************************************************************************************************
class New_Log(Screen):
    def back(self):
        MDApp.get_running_app().root.current = 'Home'



class Search(Screen):
    def back(self):
        MDApp.get_running_app().root.current = 'Home'

#*********************************************************************************************************
# SCREENS/PAGES
#*********************************************************************************************************



#*********************************************************************************************************
#MAPS_PAGE
#*********************************************************************************************************

class MapsView(MDGridLayout):
    def __init__(self, **kw):
        super(MapsView, self).__init__(**kw)
        mapview = MapView(zoom=11, lat=50.6394, lon=3.057, size=(500, 400))
        #global my_map
        self.add_widget(mapview)


class Maps_Page(Screen):
    def __init__(self, **kw):
        super(Maps_Page, self).__init__(**kw)
        #global mapview
        #self.add_widget(mapview)


    def on_enter(self):
        print("[ON_ENTER]:[MAPS_SCREEN]")
        Clock.schedule_interval(self.go_on, 1)

    def go_on(self, inst):
        global name_
        #print(f"[USER]:[{name_}]")
        self.ids['USER'].text = name_


    def home(self):
        MDApp.get_running_app().root.current = 'Home'
        Clock.unschedule(self.go_on)

    def my_local(self):
        lat = "eg. 1"
        lon = "eg. 2"
        print(f"[MY_LOACL]: \n   [LAT]:[{lat}]\n  [LON]:[{lon}]")

    # MAP TOOLS
    def zoom_in(self):
        print("[ZOOM_IN]")

    def zoom_out(self):
        print("[ZOOM_OUT]")

    def look_up(self):
        pass

    
    # EXIT
    def back(self):
        MDApp.get_running_app().root.current = 'Main_WID'
        Clock.unschedule(self.go_on)

#*********************************************************************************************************
#CHAT_PAGE
#*********************************************************************************************************

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
                                'msg_dt': str(x.split('*')[2]),
                                'msg_text': str(x.split('*')[3][:-1]),
                                "side": "left" if x.split('*')[0] == self.target_user else "right",
                                "root_widget": self}
                                    for x in chat if x]
        except Exception as e:
            print("[ERROR]:[SCROLL_CHATS]:", str(e))


    def goToUpdate(self):
        print("INST:goT: ")

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

#*********************************************************************************************************
# ADD CONTACT PAGE
#*********************************************************************************************************
class Add_C(Screen):
    added_cont = ObjectProperty(None)
    def __init__(self, **kw):
        super().__init__(**kw)

    def add_c(self):
        added_cont = ObjectProperty(None)
        added_cont = '0'
        msg_ = "NEW_C*"+str(File_man().read_file("SOCKET_DATA/USER.txt", "*"))[2:-2]+"*"+ str(self.ids.NEW_CONTACT.text)
        print("ADDING_C", str(msg_))
        File_man().write_file("SOCKET_DATA/OUT_BOUND.txt", msg_, "*", "w")
        time.sleep(2)
        ret_val = str(File_man().read_file("SOCKET_DATA/IN_BOUND.txt", "*"))
        if "KHONA" in ret_val or "NOT_FOUND" in ret_val:
            added_cont = '1'
            print("ADDING_CONTACT_FAILED")
            Add_fail().open()

        elif "ADD_C" in ret_val:
            added_cont = '1'
            print("CONTACT_ADDED_SUCCESSFULLAI")
            Add_Success().open()
        


    def back(self):
        MDApp.get_running_app().root.current = 'Home'


#*********************************************************************************************************
#CONTACTS_PAGE
#*********************************************************************************************************
# PAGE/SCREEN
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

# CONTACT_LIST__ITEMS
class TwoButtons(BoxLayout):        # The viewclass definitions, and property definitions.
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

# CONTACT_LIST_SCROLLER
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

            self.data = [{
                        'left_text': str(x.split('*')[0]),
                        'right_text': str(x.split('*')[2]) if "OFFLINE" not in str(x.split('*')[2]) else str(x.split('*')[1]),
                        "root_widget": self}
                            for x in contacts if x]
        self.get_conts()

    def get_conts(self):
        global name_
        if name_:
            msg_ = "CONTS*"+str(name_)+"^^"
            self.FM.write_file("SOCKET_DATA/CONTS.txt", msg_, "*", "w")




    def goToUpdate(self):
        print("INST:goT: ")

#*********************************************************************************************************
#INITIAL SET_UPs
#*********************************************************************************************************

# HOME
class Home(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()

    def on_enter(self):
        print("[ON_ENTER]:HOME_SCREEN")
        Clock.schedule_interval(self.ft__, 1)


    def on_start(self, inst):
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

# LOGIN
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

# REGISTER
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
# MAIN_WID
class Main_WID(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()

    def Login(self):
        MDApp.get_running_app().root.current = 'Login'

    def Register(self):
        MDApp.get_running_app().root.current = 'Register'

    def Exit(self):
        sys.exit(1)

#*********************************************************************************************************
#SCREEN_MANAGER
class WindowManager(ScreenManager):
    pass
#*********************************************************************************************************
#MAIN
class MyMDApp(MDApp):
    def __init__(self, **kw):
        super(MyMDApp, self).__init__(**kw)
        self.FM = File_man()
        self.start_up()

    def start_up(self):
        #SOCKET_DATA
        self.FM.write_file("SOCKET_DATA/IN_BOUND.txt", "", "*", "w")
        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", "", "*", "w")
        self.FM.write_file("SOCKET_DATA/CONTS.txt", "", "*", "w")
        self.FM.write_file("SOCKET_DATA/USER.txt", "", "*", "w")
        self.FM.write_file("SOCKET_DATA/MSG_TO.txt", "", "*", "w")
        self.FM.write_file("SOCKET_DATA/MSG_OF.txt", "", "*", "w")


        #CHATS_DATA
        self.FM.write_file("CHATS/CONTS.txt", "", "*", "w")
        self.FM.write_file("CHATS/CURRENT.txt", "", "&", "w")


        try:
            self.conn = connections()
            self.recv = threading.Thread(target=self.conn.get_msg)
            self.watch = threading.Thread(target=self.conn.send_msg)
            self.recv.start()
            self.watch.start()
        except Exception as e:
            print("\n\n!!INIT_CONNECTION_ERROR!!\n\n", str(e))
        pass

    def build(self):
        kv = Builder.load_file("main.kv")
        return kv
#*********************************************************************************************************

if __name__=="__main__":
    M = MyMDApp()
    M.run()
