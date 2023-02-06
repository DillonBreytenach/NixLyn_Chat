try:
    #kivy.require('2.1.0')  ## -2023/01/06-

    # BASELINE IMPORTS
    import threading
    import time
    import os
    import sys
    import socket
    import pathlib

    # LOCAL IMPORTS
    #from server7 import Server_App
    #from conns import connections
    from File_Man import File_man

    # KIVY IMPORTS
    import kivymd
    from kivymd.app import MDApp
    from kivy.clock import Clock, mainthread
    from kivy.lang import Builder
    from kivy.logger import Logger

    # KIVY_UIX IMPORTS
    from kivy.uix.screenmanager import NoTransition, Screen, ScreenManager

    #   # LAYOUTS_&_VIEWS
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivymd.uix.floatlayout import MDFloatLayout
    from kivy.uix.recycleview import RecycleView
    from kivy.uix.widget import Widget

    #   # DATA_PROPERTIES
    import kivy.properties
    from kivy.properties import ObjectProperty, StringProperty

    # UTILS => PLATFORM
    from kivy.utils import platform

    




    # TDD

    import plyer
    from plyer import gps, vibrator

    from jnius import autoclass
    from kivy.logger import Logger

    from urllib.request import urlopen

    from OpenSSL import SSL
    import requests
    import kivy_garden
    from kivy_garden.mapview import MapSource, MapView

    #from kivy_garden.mapview.mbtsource import MBTilesMapSource


    import re as r


    from kivy.core.window import Window
    from kivy.uix.widget import Widget


    vibrator.vibrate(10)
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
class MyGPS(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.FM = File_man()
        self.gps_co_orts = ""
        self.gps_stats_ = ""
        

    def on_enter(self):
        try:
            #global myMap
            ##self.add_widget(myMap)
            #print("[MyMapp]")
            #print(myMap)

            vibrator.vibrate(10)

            pass
        except Exception as e:
            self.FM.write_file(f"ER_MAP_{str(e)}_.txt", "", "\n", "w")
            print(f"[ERROR_]::[MAPS]::[>{str(e)}<]")
        pass





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










#*********************************************************************************************************
# TEST CONNS SCREEN
#*********************************************************************************************************
#
#*********************************************************************************************************
####     # BUTTONS -> DYNAMIC_WIDGETS
#*********************************************************************************************************
class ConnButtons(MDBoxLayout):        # The viewclass definitions, and property definitions.
    serv_stat_ = StringProperty()
    serv_info_ = StringProperty()

    def go_chat(self, name):
        print(f"[ITEM]::[>{str(name)}<]")

#*********************************************************************************************************
#
#*********************************************************************************************************
####       # SCROLLER -> DIRECTORY_INFO
#*********************************************************************************************************
class ScrollServ(RecycleView):
    def __init__(self, **kw):
        super(ScrollServ, self).__init__(**kw)
        self.FM = File_man()
        self.name = ""
        self.time = ""
        Clock.schedule_interval(self.go_on, 0.8)
        print("[Scroll_Serv]::[INIT]")

    def current(self, inst):
        print("INST:: ", str(inst))


    def go_on(self, inst):
        #print("[Scroll_Me]::[Go_On]")
        checks = self.FM.read_file("SERV_STAT.txt", "%")
        if "EMPTY" not in str(checks):
            self.data = [{
                        'serv_info_': str(x) if "$[ADDR]" in str(x) else ">ADDR<",
                        'serv_stat_': str(x) if "$[STAT]" in x else ">STAT<",
                        "root_widget": self}
                            for x in checks if x]


    def goToUpdate(self):
        print("INST:goT: ")
#*********************************************************************************************************
#



#*********************************************************************************************************
##  $   ## SCREEN ##
#*********************************************************************************************************
#
class Test_Conn(Screen):
    lag_ = StringProperty("Y")
    serv_ = StringProperty("OFF")
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()
        self.dir_test_count = 0
        self.test_ip = ""
        self.test_port = 0
        self.go_server = False


    # GET ACTUAL IP
    #   -> CONNECTS_SOCKET -> GOOGLE_IP/443
    #   -> READS_RETURN -> 
    def deviceIP(self):
        try:
            myip="python3 -c 'import socket; print([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith(\"127.\")][:1], [[(s.connect((\"8.8.8.8\", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])'"
            act_ip = os.popen(myip).read()
            print(f"[ACT_IP]:[<>{str(act_ip)}<>]")
            self.ids['conn_act4'].text = "[DEV_IP]::"+str(act_ip)
            return act_ip
        except Exception as e:
            print(f"[ERROR]::[ACT_IP]:0:[>{str(e)}<]")
            self.ids['conn_act4'].text = f"[ERROR]::[ACT_IT]:0:[>{str(e)}<]"


    # HTTP-PING.. Be CareFul
    def getIP(self):
        try:
            d = str(urlopen('http://checkip.dyndns.com/').read())
            return r.compile(r'Address: (\d+\.+\d+\.+\d+\.+\d)').search(d).group(1)
        except Exception as e:
            print('[RE_FAIL]',str(e))

    def on_enter(self):
        try:
            act_IP = self.deviceIP()
            #act_IP = str([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
            print('[DEV_ADDR]::',str(act_IP))
            if len(act_IP) > 0:
                self.ids['conn_act4'].text = "[DEV_IP]::"+str(act_IP)
            #s.close()
        except Exception as e:
            print("[NO_DEV_IP]",str(act_IP))
            self.ids['conn_act4'].text = "[DEV_IP]::[ERROR]::"+str(act_IP)+f"[>{str(e)}<]"

        try:
            and_IP = self.getIP()
            print('[WiFi_ADDR]::',str(and_IP))
            self.ids['conn_act3'].text = "[WiFi_IP]::"+str(and_IP)
        except:
            print("[NO_WiFi_IP]")
            self.ids['conn_act3'].text = "[WiFi_IP]::[ERROR]::"+str(and_IP)
            pass





        try:
            #  >> NEED >> android.permission.BIND_VPN_SERVICE
            my_ip = socket.gethostbyname(socket.gethostname())
            print(f"[MY_IP]::[>{str(my_ip)}<]")
            self.ids['conn_act2'].text = "[MY_IP]::"+str(my_ip)
        except:
            print("[ERROR]::[_MY_IP_]::[ON_OPEN]")


    def my_checker_(self, inst):
        try:
            threads = str(self.FM.read_file("ACTIVE_THREADS.txt", "\n"))
            if threads:
                self.ids['conn_act'].text = "[SEVER-THREADS]::"+threads
            else:
                pass
        except Exception as e:
            self.ids['conn_act'].text = "[E]>>>"+str(e)

    def close_serv(self):
        try:
            self.ST.join()
            self.ids['conn_act1'].text = "[MY_SEVR]::[JOIN_ED]"
            self.serv_ = "OFF"
        except Exception as e:
            self.ids['conn_act1'].text = f"[MY_SEVR]::[ERROR]"
            self.serv_ = "UHM"

    def start_serv(self):
        try:
            from server7 import Server_App
        except Exception as e:
            print("[NO_SERVER_IMPORT]", str(e))

        try:
            serv_test_ip = str(self.ids['TEST_IP'].text)
            serv_test_port = int(self.ids['TEST_PORT'].text)



            print(f"[SERVER_START_AS]::[<{str(serv_test_ip)}>]::[<{str(serv_test_port)}>]")
            self.go_server = True
        except Exception as e:
            print(f"[ERROR]::[START_SERV]:0:[>{str(e)}<]")
        try:
            if self.go_server == True:
                self.Serv_Th = Server_App()
                print("[SERVR_IMPORTED]")
                self.ST = threading.Thread(  group=None,
                                        target=(self.Serv_Th.server_thread),
                                        args=(serv_test_ip, serv_test_port)
                                    )
                self.ST.start()
                self.serv_ = "ON"
                self.ids['conn_act1'].text = "[MY_SEVR]::[RUNNING]"
                Clock.schedule_interval(self.my_checker_, 1)
            else:
                print("[SERVER_NOT_RUNNING]")
                self.ids['conn_act2'].text = "[MY_SEVR]::[NOT_RUNNING]"
        except Exception as e:
            print(f"[ERROR]::[START_SERV]:1:[>{str(e)}<]")
            self.ids['conn_act2'].text = f"[MY_SEVR]::[NOT_RUNNING]::[>{str(e)}<]"

    def test_conns(self, host, port):
        try:
            serv_test_ip = str(self.ids['TEST_IP'].text)
            serv_test_port = int(self.ids['TEST_PORT'].text)
            self.FM.write_file("CONN/IP_HOS.txt", f"{serv_test_ip}*{str(serv_test_port)}", "", "w")
        except Exception as e:
            self.ids['conn_act'].text = f"[CONNECTION_FAILED]\n[>{str(e)}<]"

        try:
            self.conn = connections()
            self.ids['conn_act'].text = f"[IMPORTED]::[CONNS]"
        except Exception as e:
            self.ids['conn_act'].text = f"[FAILED]::[CONNS]&&[IMPORT]::[>{str(e)}<]"
            print(f"[FAILED]::[CONNS]&&[IMPORT]::[>{str(e)}<]")

        try:
            print("[TESTING]:[CONNECTION]:->[SERVER]")
            self.recv = threading.Thread(target=self.conn.get_msg)
            self.watch = threading.Thread(target=self.conn.send_msg)
            self.recv.start()
            self.watch.start()
            self.ids['test_conn'].text = "CONNECTED"
            print("[JUST_CHECK]")
        except Exception as e:
            self.ids['conn_act'].text = f"[CONNECTION_FAILED]\n[>{str(e)}<]"
            print("[ERROR]:[CONNECTION]:",str(e))
            pass

                    #self.FM.write_file("./SOCKET_DATA/OUT_BOUND.txt", "INIT_HELLO", "*", "w")


        #def my_ip_test(self):
            #try:
            #    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #    s.connect(("8.8.8.8", 80))
            #    ip_address = s.getsockname()[0]
            #    self.ids['conn_act1'].text = f"IP Address: {ip_address}"
            #    s.close()
            #except Exception as e:
            #    self.ids['conn_act2'].text = f"[ERROR]::>>IP Address: <<"

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
            self.ids['conn_act'].text = f"[G_PING]:['GOOGLE.COM']:[443]"
            self.ids['conn_act1'].text = f"[G_PING]:[<{ping_ret}>]"
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

            self.ids['conn_act'].text = f"[TEST_PING]-[IP][>{test_ip}<]-[PORT]:[>{test_port}<]"
            print(f"\n[TEST_PING]----\n-->>[IP]>>[>{test_ip}<]\n   -->>[PORT]>>[>{test_port}<]\n==================\n")


            if test_ip:
                try:
                    self.ids['conn_act1'].text = f"[TESTING...]"
                    my_ping = self.check(str(test_ip),int(test_port),timeout=1)
                    print(f"[MY_PING]::[>{str(my_ping)}<]")
                    self.ids['conn_act1'].text = f"[TEST_PING]::[<{str(my_ping)}>]"
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
        if self.lag_ == "N":
            self.lag_ = "Y"
            return
        else:
            self.lag_ = "N"
        try:

            serv_test_ip = str(self.ids['TEST_IP'].text)
            serv_test_port = int(self.ids['TEST_PORT'].text)

            from conns import connections
            self.conns_ = connections()
            self.client_thread = threading.Thread(
                                                    group=None,
                                                    target=(self.conns_),
                                                    args=(serv_test_ip, serv_test_port)
                                                )
            self.client_thread.start()
            self.ids['conn_act2'].text = f"[CLIENT_HIDE]:[ACTIVE]"

        except Exception as e:
            print(f"[ERROR]::[TEST_TIMED_STATS_CHECK]::[>{str(e)}<]")
            self.ids['conn_act2'].text = f"!![ERROR]!![MY_STATS_TEST]::[>{str(e)}<]"
            pass
        #self.sock.close()

    def close_test(self):
        try:
            self.sock.close()
            self.lag_ = "Y"
        except:
            self.lag_ = "N"

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

    def goto_loading(self):
        MDApp.get_running_app().root.current = 'loading'
        # Clock.unschedule(self.go_on)

    def goto_gps(self):
        MDApp.get_running_app().root.current = 'myGPS'
        # Clock.unschedule(self.go_on)
#
#
#*********************************************************************************************************
#*********************************************************************************************************





#*********************************************************************************************************
#*********************************************************************************************************
##  LOADING_PAGE
#*********************************************************************************************************
####     # BUTTONS -> DYNAMIC_WIDGETS
#*********************************************************************************************************
class TwoButtons(MDBoxLayout):        # The viewclass definitions, and property definitions.
    left_text = StringProperty()
    right_text = StringProperty()

    def go_chat(self, name):
        print(f"[ITEM]::[>{str(name)}<]")

#*********************************************************************************************************
#
#*********************************************************************************************************
####       # SCROLLER -> DIRECTORY_INFO
#*********************************************************************************************************
class ScrollDirs(RecycleView):
    def __init__(self, **kw):
        super(ScrollDirs, self).__init__(**kw)
        self.FM = File_man()
        self.name = ""
        self.time = ""
        Clock.schedule_interval(self.go_on, 0.8)
        print("[Scroll_Me]::[INIT]")

    def current(self, inst):
        print("INST:: ", str(inst))


    def go_on(self, inst):
        #print("[Scroll_Me]::[Go_On]")
        checks = self.FM.read_file("CHECK_SUM.txt", "%")[:-1]
        if "EMPTY" not in str(checks):
            self.data = [{
                        'left_text': str(x.replace("$DIR#", "")) if "DIR" in str(x) else "||",
                        'right_text': str(x.replace("$FIL#", "")) if "FIL" in str(x) else "",
                        "root_widget": self}
                            for x in checks if x]


    def goToUpdate(self):
        print("INST:goT: ")
#*********************************************************************************************************
#
#*********************************************************************************************************
##  $   ## SCREEN ##
#*********************************************************************************************************
#
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
#       ##  EOS  ##
#*********************************************************************************************************



        




#*********************************************************************************************************
#SCREEN_MANAGER
#*********************************************************************************************************
#
class WindowManager(ScreenManager):
    pass
#
#*********************************************************************************************************



#*********************************************************************************************************
#MAIN
#*********************************************************************************************************
#
class LaunchTestApp(MDApp):

    gps_location = StringProperty()
    lat_gps = StringProperty("[lat]:?")
    gps_status = StringProperty('Click Start to get GPS location updates')
    is_droid = StringProperty('WAITING FOR GPS')
    perms_  = StringProperty('[&]')

    def __init__(self, **kw):
        super(LaunchTestApp, self).__init__(**kw)
        print("[INIT_STACK_TREE]")
        self.FM = File_man()
        try:
            self.build_tree()
            self.start_up()
            print("[INIT_BUILD_TREE]")
        except:
            pass



    def start_up(self):
        self.FM.write_file("SERV_STAT.txt", "INIT", "%", "w")
        # CHECK_SUM
        self.FM.write_file("CHECK_SUM.txt", "EMPTY", "*", "w")
        self.FM.write_file("WHAT_NOW.txt", "EMPTY", "*", "w")
        self.FM.write_file("ACTIVE_THREADS.txt", "threads", "\n", "w")
        print("[INIT_CLEAN_TREE]")



    def build_tree(self):
        try:
            
            # PROJECT_DATA
            #   | -CONTS/
            #       |-U1.txt
            #       |-U3.txt
            #       |-U4.txt
            #   | -MSGS
            #       |-U1/
            #           |-U3.txt
            #           |-U4.txt
            #       |-U3/
            #           |-U1.txt
            #           |-U4.txt
            #       |-U4/
            #           |-U1.txt
            #           |-U3.txt
            #   | -USERS
            #       |-U1.txt
            #       |-U3.txt
            #       |-U4.txt

            try:
                # BASE DIRS
                self.make_dir("CONTS")
                self.make_dir("MSGS")
                self.make_dir("USERS")
                self.make_dir("FAILS")
                self.make_dir("PASSES")
            except Exception as e:
                print(f"[WHAT_THE[{str(e)}]]")

            try:
                # NESTED DIRS
                self.FM.make_dir("MSGS")
                self.FM.make_dir("MSGS/U1")
                self.FM.make_dir("MSGS/U3")
                self.FM.make_dir("MSGS/U4")
            except Exception as e:
                print(f"[WHAT_THE[{str(e)}]]")


            try:
                # SET_USERS
                self.FM.write_file("USERS/U1.txt", "USER*U1*U1*2022-12-27-01-59*OFFLINE*CONTS/U1.txt*MSGS/U1*", "\n", "w")
                self.FM.write_file("USERS/U3.txt", "USER*U3*U3*2023-01-09-13-53-52*OFFLINE*CONTS/U3.txt*MSGS/U3*", "\n", "w")
                self.FM.write_file("USERS/U4.txt", "USER*U4*U4*2022-12-29-01-41-28*OFFLINE*CONTS/U4.txt*MSGS/U4*", "\n", "w")
            except Exception as e:
                print(f"[WHAT_THE[{str(e)}]]")


            try:
                # CONNECT CONTS
                self.FM.write_file("CONTS/U1.txt", "U3%", "*", "w")
                self.FM.write_file("CONTS/U3.txt", "U4%U1%", "*", "w")
                self.FM.write_file("CONTS/U4.txt", "U3%", "*", "w")
            except Exception as e:
                print(f"[WHAT_THE[{str(e)}]]")




            try:
                # BUILD MSGS
                self.FM.write_file("MSGS/U3/U4.txt", "*2022-12-27-04-58-46*HELLO&*2022-12-27-12-59-19*LAST_SENT&*2022-12-27-22-24-30*LET_S\nDO\nSOME\nOOGLIN&*2022-12-28-03-07-50*YES&*2022-12-28-03-08-12*WHY?\nBECAUSE I CAN&*2022-12-28-03-44-08*MAYBE&*2022-12-29-01-41-20*NOW, FOR MAPS&", "*", "w")
                self.FM.write_file("MSGS/U4/U3.txt", "INVITE_FROM*U4*TO*U3*&*2022-12-27-04-18-21*HI_THERE&*2022-12-27-13-05-04*OH_FUCK&*2022-12-27-21-38-06*YEAH_BOOOI&*2022-12-27-21-54-34*TESTING\n', 'MULTI\n', 'LINE\n', '\n', 'MSGS...\n', '&*2022-12-27-22-24-55*..YOU GET THAT?&*2022-12-28-03-07-59*HELLO&*2022-12-28-03-33-41*WELLLLLLL&*2022-12-29-01-41-10*YES... &", "*", "w")
            except Exception as e:
                print(f"[WHAT_THE[{str(e)}]]")


            print("[INIT_CLEAN_TREE]")


        except Exception as e:
            print("ERROR_BUILING_TREE"+str(e))

    def make_dir(self, path):
        pathlib.Path(path).mkdir(parents=True, exist_ok=True) 
        return 0

    def get_perms(self):
        if platform == "android":
            try:
                # GET PERMISSIONS
                try:
                    from android.permissions import request_permissions, Permission
                    request_permissions([
                                            Permission.LOCATION_HARDWARE,
                                            Permission.ACCESS_BACKGROUND_LOCATION,
                                            Permission.ACCESS_COARSE_LOCATION,
                                            Permission.ACCESS_FINE_LOCATION,
                                            Permission.ACCESS_WIFI_STATE,
                                            Permission.ACCESS_NETWORK_STATE,
                                            Permission.FOREGROUND_SERVICE,
                                            Permission.BIND_ACCESSIBILITY_SERVICE,
                                            Permission.USE_SIP
                                        ])
                except Exception as e:
                    pass
                try:
                    from android import AndroidService
                    self.FM.write_file(f"A_SERVICES_0_ACCESSED.ffs", "DENIED", "\n", "w")
                except Exception as e:
                    self.FM.write_file(f"A_SERVICES_0_DENIED.ffs", "DENIED", "\n", "w")





                print("[PHASE_2]")
            except Exception as e:
                print(f"[ERROR]::[PERMS_DENIED]:[>{str(e)}<]")
                self.FM.write_file(f"PERMS_{str(e)}_DENIED.ffs", "DENIED", "\n", "w")



    def build(self):
        print("[BUILD_KIVY]")
        if platform == "android":
            try:
                # GPS CONFIG
                gps.configure(on_location=self.on_location, on_status=self.on_status)
                self.FM.write_file("GPS_STARTED.ffs", "GPS", "\n", "w")
            except Exception as e:
                self.FM.write_file("GPS_FAILED.ffs", "GPS", "\n", "w")
            try:
                # GET PERMISSIONS
                self.get_perms()
                self.perms_ = '[^]'
            except Exception as e:
                self.gps_status = 'GPS is not implemented for your platform'


        kv = Builder.load_file("main.kv")
        return kv

    def hi(self):
        print("By..")

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
        self.gps_location = '\n'.join(['{}={}&'.format(k, v) for k, v in kwargs.items()])
        
        self.lat_gps = str(self.gps_location).split("&")[0]


    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)



    def on_pause(self):
        gps.stop()
        return True

    def on_resume(self):
        gps.start()
        pass



if __name__=="__main__":
    LaunchTestApp().run()




#*********************************************************************************************************
