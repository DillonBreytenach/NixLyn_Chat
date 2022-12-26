#CONNECTION__
try:
    import socket
    import string
    from socket import error as sock_error
    import sys
    import threading
    from threading import Thread, ThreadError
    from file_handle import File_man
    import time
except Exception as e:
    print("[IMPORT]::[ERROR]", str(e))

#CONNECTION CLASSES
class connections():
    #__INIT__
    def __init__(self, **kwargs):
        try:
            self.val = ""
            self.FM = File_man()
        except Exception as e:
            print("[ERROR]::[SETTING]::{VARS}&&{IMPORTS}::", str(e))
        try:
            self.host = '127.0.0.1'
            self.port = 8085
            self.encap = "*"
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            print('CONNECTION_INIT[ERROR]:: ', str(e))
        #SET SOCKET_CONNECTIONS
        try:
            self.sock.connect((self.host, self.port))
            print("\n[CONNECTED]\n")
        except Exception as e:
            print('SOCK_ERROR:: ', str(e))
            sys.exit(1)



    # FILTER MSG
    def msg_of(self, data):
        ls_data = []
        collected_ = []


        if "ACCESS_DENIED" in data:
            self.FM.write_file("SOCKET_DATA/MSG_OF.txt", data, "*", "w")

        if "SAVED" in data:
            ls_data = data.split("*")

            for i in ls_data:
                print("MSG:: ", str(i))

            if len(ls_data) >= 6:
                user_ = str(ls_data[2])
                dt_stamp = str(ls_data[4])
                msg_of = str(ls_data[5])
                target_file = "MSGS/"+user_+".txt"
                to_save = dt_stamp+"*"+msg_of
                self.FM.write_file(target_file, msg_of, "&", "a")
                print("[MSG]::", to_save, ":[SAVED]:", target_file)

        if "MSGS_OF" in data:
            ls_data = data.split("&")

            print("\n\n\n[CONNS]:[MSGS_OF]:\n\n  NOW FILTER THE MSG_DATA")
            for i, val in enumerate(ls_data):
                print("[MSG]:[i]:", str(i), ":[val]:", str(val))
                if len(val) == 0:
                    pass
                if "USER$" in val:
                    sender_ = str(val.split("$")[1])
                    sender__ = str(sender_.split("*")[0])
                    print("[SENDER]: ", sender__)
                if len(val) > 21:
                    check_msg = val.split("*")
                    if len(check_msg) >= 4:
                        print("LEN ,/")

                    
                    
                    #if val[0]=="*" and val[5]=="/" and val[8]=="/" and val[11]=="-" and val[14]==":":



                    print(">:-|   ->>", str(val))
                    collected_.append(val)


            for what in collected_:
                print("COL:: ", str(what))


            time.sleep(2)
            file_name = f"MSGS/{sender__}.txt"
            self.FM.write_file(file_name, collected_, "$", "w")

            print("AND NOW???")

                # eg>  *2022/12/22-05:02*MSG*
                # if:
                    # [0]=="*"
                    # [5]=="/"
                    # [8]=="/"
                    # [11]=="-"
                    # [14]==":"
            




    #RECEIVE
    def get_msg(self):
        print("[GET_MSG]:[RUNNING]")
        self.E = threading.Event()
        while True:
            data = ""
            try:
                data_len = int(self.sock.recv(64).decode())
                if not data_len:
                    self.E.wait()
                #print("DATA_LEN: ", str(data_len))
                if int(data_len) > 0:
                    data = str(self.sock.recv(data_len).decode())
                    if data:
                        #print("DATA RECVED:: ", str(data))


                        #WRITE ALL INCOMING DATA TO IN_BOUND<FILE>
                        self.FM.write_file("SOCKET_DATA/IN_BOUND.txt", data, "*", "w")
                        # LOG OFF
                        if "GOODBYE" in data:
                            print("LOGGED_OFF::", str(data))

                        # MESSAGING 
                        elif "MSG" in data:
                            print("[MSG_IN]:", str(data))
                            self.msg_of(data)

                        #UPDATE CONTACTS LIST DATA
                        elif "STATE" in data:
                            #print("[GOT_TARGET_USER_STATE]::", str(data))
                            self.FM.write_file("CHATS/TARGET_STATE.txt", data, "*", "w")

                        # CONTACTS
                        elif "CONTS" in data:
                            c_list = data.split("$")
                            if "FAIL" in data:
                                # ("SOCKET_DATA/USER.txt", "*")
                                print("ADD_USER_FAIL", str(data))
                                #self.FM.write_file("CHATS/CONTS.txt", data, "%", "w")
                                self.FM.write_file("SOCKET_DATA/IN_BOUND.txt", "FAIL", "%", "w")

                            elif "EMPTY" not in c_list:
                                #print("C_LIST.. ", str(c_list[1]))
                                self.FM.write_file("CHATS/CONTS.txt", str(c_list[1]), "%", "w")
                                self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", "", "%", "w")
                            
                    data_len = 0
            except Exception as e:
                print("[SOCKET CLOSED]")
                print(str(e)) 
                self.sock.close()
                sys.exit(1)





    #TRANSMIT
    def send_msg(self):
        self.E = threading.Event()
        self.data = ""
        self.msg = ""
        print("[SEND_MSG]:[RUNNING]")
        path = "SOCKET_DATA/OUT_BOUND.txt"
        msg_pat = "SOCKET_DATA/MSG_TO.txt"
        cont_path = "SOCKET_DATA/CONTS.txt"
        #CHECK OUT_BOUND<FILE> CHANGES
        try:
            self.init_msg = str(self.FM.read_file(msg_pat, ""))
            self.init_data = str(self.FM.read_file(path, "*"))
            self.init_conts = str(self.FM.read_file(cont_path, "*"))
            #print("INIT_DATA:: ", self.init_data)
        except:
            print("conns.py::send_msg():: ERROR??")
        try:
            while True:
                #UPDATE 
                try:

                    # PATHS
                    self.data = self.FM.read_file(path, "*")
                    self.msg = self.FM.read_file(msg_pat, "*")
                    self.conts = self.FM.read_file(cont_path, "*")


                    if self.init_data != self.data and len(self.data) > 1:
                        print(f"INIT: {self.init_data} :: DATA: {self.data} \n ")
                        toSend = ""
                        for _ in self.data:
                            toSend+=str(_)+"*"

                        msg_len = len(toSend)
                        send_len = str(msg_len).encode()
                        send_len += b' ' * (64 - len(send_len))
                        try:
                            self.sock.send(send_len)
                            self.sock.send(toSend.encode())
                            #print("toSend:: ", str(toSend))
                            #RESET DATA
                            self.init_data = self.data
                            #print(f"INIT_DATA ::\n>{self.init_data}\nN_DATA ::\n>{self.data}\n")
                            toSend = ""
                        except Exception as e:
                            print("[FUCKUP]::SEND_MSG:TO_SERVER:", str(e))
                            time.sleep(1000)
                            break



                    if self.init_conts != self.conts and len(self.conts) > 1:
                        toSend = ""
                        for _ in self.conts:
                            toSend+=str(_)+"*"

                        msg_len = len(toSend)
                        send_len = str(msg_len).encode()
                        send_len += b' ' * (64 - len(send_len))
                        try:
                            self.sock.send(send_len)
                            self.sock.send(toSend.encode())
                            #print("toSend:: ", str(toSend))
                            #RESET DATA
                            self.init_conts = self.conts
                            #print(f"INIT_DATA ::\n>{self.init_data}\nN_DATA ::\n>{self.data}\n")
                            toSend = ""
                            print("[MSG_SENT]:", str(toSend))
                        except Exception as e:
                            print("[FUCKUP]::SEND_MSG:TO_CONTACT:", str(e))
                            break




                    # MSGS

                    if self.init_msg != self.msg and len(self.msg) > 0:
                        print("[SENDING_MSG_OUT]")
                        toSend = ""
                        for _ in self.msg:
                            toSend+=str(_)+"*"

                        msg_len = len(toSend)
                        send_len = str(msg_len).encode()
                        send_len += b' ' * (64 - len(send_len))
                        try:
                            self.sock.send(send_len)
                            self.sock.send(toSend.encode())
                            #print("toSend:: ", str(toSend))
                            #RESET DATA
                            self.init_msg = self.msg
                            #print(f"INIT_DATA ::\n>{self.init_data}\nN_DATA ::\n>{self.data}\n")
                            toSend = ""
                            print("[MSG_SENT]:", str(toSend))
                        except Exception as e:
                            print("[FUCKUP]::SEND_MSG:TO_CONTACT:", str(e))
                            break

                except Exception as e:
                    print("[SEND_MSG]:[LOOP_ERROR] >", str(e))
                    break
        except Exception as e:
            print("SENDING_ERROR::", str(e))
            sys.exit(1)


