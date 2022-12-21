#CONNECTION__
try:
    import socket
    import string
    from socket import error as sock_error
    import sys
    import threading
    from threading import Thread, ThreadError
    from file_handle import File_man
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
                        if data:
                            #WRITE ALL INCOMING DATA TO IN_BOUND<FILE>
                            self.FM.write_file("SOCKET_DATA/IN_BOUND.txt", data, "*", "w")
                            #UPDATE CONTACTS LIST DATA
                            if "STATE" in data:
                                #print("[GOT_TARGET_USER_STATE]::", str(data))
                                self.FM.write_file("CHATS/TARGET_STATE.txt", data, "*", "w")
                            if "CONTS" in data:
                                c_list = data.split("*")
                                if "EMPTY" not in c_list:
                                    print("C_LIST.. ", str(c_list[1]))
                                    self.FM.write_file("CHATS/CONTS.txt", str(c_list[1]), "%", "w")
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
        msg_pat = "SOCKET_DATA/MSG_OF.txt"
        #CHECK OUT_BOUND<FILE> CHANGES
        try:
            self.init_msg = str(self.FM.read_file(msg_pat, ""))
            self.init_data = str(self.FM.read_file(path, "*"))
            #print("INIT_DATA:: ", self.init_data)
        except:
            print("conns.py::send_msg():: ERROR??")
        try:
            while True:
                #UPDATE 
                try:
                    # SERVER COMMS
                    self.data = self.FM.read_file(path, "*")
                    if str(self.init_data) is str(self.data):
                        #print("[SEND_MSG]::[NO_UPDATE]")
                        #self.E.wait()
                        pass

                    elif self.init_data != self.data and len(self.data) > 1:
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

                    # MSGS
                    self.msg = self.FM.read_file(msg_pat, "$%:")
                    if str(self.init_msg) is str(self.msg):
                        pass

                    elif self.init_msg != self.msg and len(self.msg) > 1:
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
                        except Exception as e:
                            print("[FUCKUP]::SEND_MSG:TO_CONTACT:", str(e))

                except Exception as e:
                    print("[SEND_MSG]:[LOOP_ERROR] >", str(e))
        except Exception as e:
            print("SENDING_ERROR::", str(e))
            sys.exit(1)
