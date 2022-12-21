#TODO::
#TABS                   [CONTINUOUS]
#LOGIN/REGISTER         [DONE]:[STD]:{NEXT}->{CROSS_ACCOUNT}
#CONTACT_LIST           [DONE]
#CONTACT_STATUS         [DONE]
#MESSAGING              [NEXT]:[SEND/RECV]:
    #   {ToDo} : {RollingMSG_s} && {Text_Input}
#FORMS{DYNAMIC}         []
#MAPS                   []
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
    from kivy.properties import ObjectProperty

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

    from kivy.lang import Builder

    #PROGRAM FILES IMPORTS
    from conns import connections
    from file_handle import File_man
except Exception as e:
    print("[ERROR]:[IMPORTS]", str(e))


#POPUPS
#*********************************************************************************************************
class Login_Fail(Popup):
    print("LOGIN_FAIL")
class Welcome(Popup):
    print("WELCOME")
    msg_ = "ONLINE*"+str(File_man().read_file("SOCKET_DATA/USER.txt", "*"))[2:-2]
    File_man().write_file("SOCKET_DATA/OUT_BOUND.txt", msg_, "*", "w")
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
#*********************************************************************************************************


#*********************************************************************************************************
#CHAT_PAGE
#*********************************************************************************************************
class Chat_Msgs(Button):
    root_widget = ObjectProperty()

    def on_release(self, **kwargs):
        super().on_release(**kwargs)
        self.FM = File_man()
        print("MSG:ON_R: ", str(self.text))
        #if "Home" not in self.FM.read_file("CHATS/CURRENT.txt", "&"):
        #    print("OPENING_CHATS", str(self.text))
        #    self.FM.write_file("CHATS/CURRENT.txt", str(self.text), "&", "w")
        #    MDApp.get_running_app().root.current = 'Chats'

class Scroll_Chats(RecycleView): 
    def __init__(self, **kw):
        super(Scroll_Chats, self).__init__(**kw)
        self.FM = File_man()
        print("[Scroll_Chats]:: INIT")
        Clock.schedule_interval(self.go_on, 1)

    def go_on(self, inst):
        #print("[Scroll_Me]::[Go_On]")
        cont = self.FM.read_file("CHATS/CURRENT.txt", "%")
        chat = self.FM.read_file(f"MSGS/{str(cont)[2:-2]}.txt", "*$")[:-1]
        if chat:
            #print("[ASSIGNING_CHATS]::[SCROLL_CHATS]")
            self.data = [{'text': str(x), "root_widget": self} for x in chat if x]


    def goToUpdate(self):
        print("INST:goT: ")

class Chats(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()
        self.state = ""



    def on_enter(self):
        print("[ON_ENTER]:CHATS_SCREEN")
        if "Home" not in self.FM.read_file("CHATS/CURRENT.txt", "&"):
            Clock.schedule_interval(self.go_on, 1)

    def go_on(self, inst):
        #print("[CHATS]::[Go_On]")
        self.target_user = ""
        user_data = self.FM.read_file("CHATS/CURRENT.txt", "*")
        self.target_user = str(user_data[0])
        self.ids['TARGET_USER'].text = str(self.target_user)
        self.chat_info()


    def send_it(self):
        user_data = self.FM.read_file("SOCKET_DATA/USER.txt", "*")
        self.user_name = str(user_data[0])
        to_send = "MSG_TO$%:"+str(self.target_user)+"$%:"+self.user_name+"$%:"+str(self.ids['MSG_OUT'].text)
        print("\nSEND:\n >> ", to_send)
        self.FM.write_file("SOCKET_DATA/MSG_OF.txt", to_send, "$%:", "w")

    def chat_info(self):
        #print("[CHAT_INFO]")
        msg_ = "GET_STATE*"+str(self.target_user)+"*"+str(self.FM.read_file("CHATS/CURRENT.txt", "&")[0])
        #print("[GET_STATE]:: ", str(msg_))

        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", msg_, "*", "w")
        #print("CHATS_TO_BE_DONE")
        self.state = self.FM.read_file("CHATS/TARGET_STATE.txt", "*")
        #print("SELF.STATE:: ", str(self.state))
        try:
            self.ids['USER_STATUS'].text = str(self.state[1])
        except:
            print("TARGET_STATE_NOT_YET_LOADED")

    def home(self):
        MDApp.get_running_app().root.current = 'Home'
        self.FM.write_file("CHATS/CURRENT.txt", "Home", "&", "w")
        Clock.unschedule(self.go_on)

    def contacts(self):
        MDApp.get_running_app().root.current = 'Contacts'
        self.FM.write_file("CHATS/CURRENT.txt", "Home", "&", "w")
        Clock.unschedule(self.go_on)

    def back(self):
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
        time.sleep(1)
        ret_val = str(File_man().read_file("SOCKET_DATA/IN_BOUND.txt", "*"))
        if "KHONA" in ret_val or "FAIL" in ret_val:
            added_cont = '1'
            print("ADDING_CONTACT_FAILED")
            Add_fail().open()

        elif "ADDED" in ret_val:
            added_cont = '1'
            print("CONTACT_ADDED_SUCCESSFULLAI")
            Add_Success().open()


    def back(self):
        MDApp.get_running_app().root.current = 'Home'


#*********************************************************************************************************
#CONTACTS_PAGE
#*********************************************************************************************************
class Contacts(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()

    def on_enter(self):
        print("[ON_ENTER]:CONTACTS_SCREEN")
        Clock.schedule_interval(self.go_on, 1)

    def go_on(self, inst):
        #print("GO_ON::CONTACTS:", str(inst))
        #self.user_name = ""
        user_data = self.FM.read_file("SOCKET_DATA/USER.txt", "*")
        self.user_name = str(user_data[0])
        #print("USER: ", str(user_data))
        self.ids['USER'].text = str(self.user_name)
        self.get_conts()

    def get_conts(self):
        #print("[GET_CONTS]")
        msg_ = "CONTS*"+str(self.user_name)
        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", msg_, "*", "w")

    def add_c(self):
        print("ADDING_CONTACT -> SCREEN")
        MDApp.get_running_app().root.current = 'add_c'


    def home(self):
        MDApp.get_running_app().root.current = 'Home'
        Clock.unschedule(self.go_on)

    def back(self):
        user_data = self.FM.read_file("SOCKET_DATA/USER.txt", "*")
        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", "LOGOUT*"+str(user_data)[2:-2]+"*OFFLINE", "*", "w")
        MDApp.get_running_app().root.current = 'Main_WID'
        Clock.unschedule(self.go_on)

#CONTACT_BUTTONS
class Chat_Buttons(Button):
    root_widget = ObjectProperty()
    def on_release(self, **kwargs):
        super().on_release(**kwargs)
        self.FM = File_man()
        print("INST:ON_R: ", str(self.text))
        if "Home" not in self.FM.read_file("CHATS/CURRENT.txt", "&"):
            if self.text:
                self.FM.write_file(f"MSGS/{str(self.text)}.txt", time, "", "a+")
            print("OPENING_CHATS", str(self.text))
            self.FM.write_file("CHATS/CURRENT.txt", str(self.text), "&", "w")
            MDApp.get_running_app().root.current = 'Chats'

#CONTACT_LIST_SCROLLER
class Scroll_Me(RecycleView):
    def __init__(self, **kw):
        super(Scroll_Me, self).__init__(**kw)
        self.FM = File_man()
        print("[Scroll_Me]:: INIT")
        Clock.schedule_interval(self.go_on, 1)
    

    def go_on(self, inst):
        #print("[Scroll_Me]::[Go_On]")
        contacts = self.FM.read_file("CHATS/CONTS.txt", "%")[:-1]
        if contacts:
            #print("[ASSIGNING_CONTS]::[SCROLL_CONTS]")
            self.data = [{'text': str(x), "root_widget": self} for x in contacts if x]

    def goToUpdate(self):
        print("INST:goT: ")

#*********************************************************************************************************
#INITIAL SET_UPs
#*********************************************************************************************************
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

    def back(self):
        user_data = self.FM.read_file("SOCKET_DATA/USER.txt", "*")
        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", "LOGOUT*"+str(user_data)[2:-2]+"*OFFLINE", "*", "w")
        MDApp.get_running_app().root.current = 'Main_WID'

#LOGIN
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
#REGISTER
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
            if "PLEASE_LOGIN" in Reg_Confirm:
                print("PLAESE_LOGIN")
                MDApp.get_running_app().root.current = 'Login'
            if "FAILED_REG" in Reg_Confirm:
                Reg_Fail().open()
        except Exception as e:
            print("REG_ERROR: ", str(e))


    def back(self):
        MDApp.get_running_app().root.current = 'Main_WID'


    #LOGIN_REGISTER_&& WHATEVER_ELSE...
#MAIN_WID
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.FM = File_man()
        self.start_up()

    def start_up(self):
        #SOCKET_DATA
        self.FM.write_file("SOCKET_DATA/IN_BOUND.txt", "", "*", "w")
        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", "", "*", "w")
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

if __name__=="__main__":
    M = MyMDApp()
    M.run()
