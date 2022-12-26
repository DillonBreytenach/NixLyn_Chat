#TODO::
#LOGIN/REGISTER         [DONE]:[STD]:
    # {NEXT}->{CROSS_ACCOUNT}
#CONTACT_LIST           [DONE]
#ADD_CONTACT            [DONE]
#CONTACT_STATUS         [DONE]
#MESSAGING              [NEXT]:[DIRECT_SEND if ONLINE]: 
    # {NEXT}->{SAVE_TILL_ONLINE}
#FORMS{DYNAMIC}         []
#MAPS                   []
#CALENDER               []
#CONNECT -> API         []
#SEARCH                 [?]


try:
    import socket
    import string
    import sys
    from threading import Thread, ThreadError
    import threading
    from File_Man import File_man
    from datetime import datetime
except Exception as e:
    print("[IPMORT]::[ERROR]:: ", str(e))

class server():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #IMPORTS
        self.FM = File_man()

        #CONNECTIONS
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 8085
        self.addr = (self.host, self.port)

        #ACTIVE USERS
        self.LOGGED_IN = []


        # THREADS 
        self.threads = []

    #SEND_METHODE
    def reply(self, conn, data):
        try:
            msg_len = len(data)
            send_len = str(msg_len).encode()
            send_len += b' ' * (64 - len(send_len))
            #print(f'[SENDING]:: {send_len}')
            #print(f'[SENDING]:: {data}')
            conn.send(send_len)
            conn.send(data.encode())
            #print("[SENT]: ", str(data))
            return
        except Exception as e:
            print('REPLY_ERROR:: ', str(e))

    #CLEAN DATA - LIST-->>STR
    def lst_to_str(self, data_lst, delim):
        try:
            data_str = ""
            #print("LIST_TO_STR:: ", str(data_lst))
            if type(data_lst) == list:
                #print("CONVERTING")
                for _ in data_lst:
                    data_str += str(_)+str(delim)
                #print("LST_TO_STR", data_str)
            return data_str
        except Exception as e:
            print("LIST_TO_STR:[ERROR]:: ", str(e))


    #GET_CONTACT_LIST
    def Get_Contacts(self, user):

        file_name = ""
        user_file = ""
        data_up = []
        user_conts = []
        p_u = ""
        u_q = ""
        u_dt = ""
        up_cont = ""
        conts_lst_str = ""

        stats_ = ""

        try:
            file_name = "CONTS/"+user+".txt"
            user_file = self.FM.check_file(file_name)
            
            if user_file == True:
                user_conts = self.FM.read_file(file_name, "%")
                if len(user_conts) > 0 and type(user_conts) == list:
                    try:
                        # FRST CHECK STATUS AND UPDATE TO USE THE CURRENT TIME
                        #   get_user_state
                        for u in user_conts:
                            print("\n\nUSER_IN_QU: ", str(u))
                            if not u:
                                pass
                            try:
                                p_u = str(u)
                                u_q = str(p_u.split("@")[0])
                                #print("GET_USER_STATUS->: ", u_q)

                                if u_q:
                                    u_dt = self.get_user_state(u_q)
                                    print("[U_DT]::", u_dt)
                                    stats_ = u_q+"*"+u_dt
                            except Exception as e:
                                print("[GET_USER_ERROR]::", str(e))

                            if stats_:
                                try:
                                    #print("[CONT]:: ", str(stats_))
                                    if stats_ not in str(data_up):
                                        data_up.append(stats_)
                                except Exception as e:
                                    print("[ERROR]::[GET_CONTS]::[STATUS]::", str(e))
                        conts_lst_str = self.lst_to_str(data_up, "%")
                        #print("CONTS:: ", str(conts_lst_str))

                        return conts_lst_str
                    except Exception as e:
                        print("RET_LIST_ERROR:: ", str(e))
                else:
                    print("CONTS_EMPTY", str(conts_lst_str))
                    return "EMPTY"

        except Exception as c_u:
            print("_ERROR::GET_CONTACTS:: ", str(c_u))

    def add_Cont(self, data):
        #data[0] = act
        #data[1] = user
        #data[2] = new_cont
        user_f_name = "CONTS/"+str(data[1])+".txt"
        new_cont_f_name = "CONTS/"+str(data[2])+".txt"
        msgs_f_name = "MSGS/"+str(data[1])
        chat_f_name = "MSGS/"+str(data[1])+"/"+str(data[2])+".txt"

        user_file = "USERS/"+str(data[2])+".txt"

        is_user = self.FM.check_file(user_file)
        print("[CHECKING_FILE]::", str(user_file))
        if is_user != True:
            print("[USER_NOT_FOUND]")
            return "NOT_FOUND"
        else:
            print("[FETCHING_DATA]::", str(data[2]))


        print("data[2]:: ", str(data[2]))
        new_cont_c = self.FM.check_file(new_cont_f_name)
        if new_cont_c == True:
            try:
                #GET_OLD_LIST
                c_list = self.FM.read_file(user_f_name, "%")
                print("C_LIST:: ", str(c_list))
                #CHECK IF ALREADY THERE
                n_list = []
                if str(data[2]) in c_list:
                    print("KHONA") # CONTACT ALREADY EXISTS
                    return "KHONA"
                if len(c_list) > 0: 
                    for _ in c_list:
                        if "EMPTY" not in str(_) and len(_) > 0: # IF THERE ARE CONTACTS (NOT_EMPTY)
                            n_list.append(str(_))
                            print("ADDING TO NEW LIST:: ", str(_), "\n\
                            *******************************")

                if str(data[2]) not in str(n_list): # IF CONT IN QUESTION NOT IN LIST 
                    n_list.append(str(data[2])+"@OFFLINE") # ADD TO LIST  
                                                    # BUT ADD THE STATUS OF THAT CONT, FIRST AS 
                                                            # OFFLINE, UPDATE ON REFRESH (GET_CONTS)
                    print("N_LIST:: ", str(n_list))
                    self.FM.write_file(user_f_name, n_list, "%", "w")
                    # CREATE CHAT DIRECTORY
                    self.FM.make_dir(msgs_f_name)
                    self.FM.write_file(chat_f_name, "INVITE_FROM*"+str(data[1])+"*TO*"+str(data[2])+"*", "&", "w")

                    return str(n_list)
            except Exception as e:
                print("ADDING_CONT_ERROR", str(e))

    #GET_STATUS
    def get_user_state(self, user):
        #TARGET_USER...
        #print("GET_USER_STATE:: ", str(user))

        now = datetime.now()
        # Format the date and time as a string in the desired format
        date_time_str = now.strftime("%Y-%m-%d-%H-%M")

        f_name = "USERS/"+str(user)+".txt"
        user_data = self.FM.read_file(f_name, "*")
        last_seen = ""

        use_less = ""
        status_ = ""
        ret_val = ""

        if len(user_data) >= 6:
            for i, u_ in enumerate(user_data):
                #print("[WTF::]::", str(i),"::",str(u_), "<--")
                if i == 3:
                    last_seen = str(u_)
                    print("LAST_SEEN:: ", str(u_))
                if i == 4:
                    status_ = str(u_)
                    print("STATUS:: ", str(u_))

            ret_val = last_seen+"*"+status_
            print("[GET_STATUS]::[RET_VAL]::", ret_val)
            return ret_val




    #PROFILE_UPDATE
    def update_User(self, client, user, state):
        # ->get_file_data -> fileter to list
        # data[0] = action
        # data[1] = USER

        #USER_FILE::
        #   >[0] = action
        #   >[1] = user_name
        #   >[2] = pswd
        #   >[3] = client_data....(NOT_NOW){TO_MUCH_BS}
        #   >[4] = status
        #   >[5] = contact_list{FILE_NAME}
        #   >[6] = msgs{FILE_NAME} : delim = "%"


        try:
            now = datetime.now()
            # Format the date and time as a string in the desired format
            date_time_str = now.strftime("%Y-%m-%d-%H-%M")


            if "OFFLINE" in state:
                print(f"[UPDATE_USER]::{str(user)}::[OFFLINE]")
            if not user:
                return


            f_name = "USERS/"+str(user)+".txt"
            user_data = self.FM.read_file(f_name, "*")
            # user_data[4] = ONLINE/OFFLINE
            user_update = []
            #print(f"LEN(USER_DATA) > {str(len(user_data))}")
            if len(user_data) >= 6:
                for i, _ in enumerate(user_data):
                    if _ and i != 4 and i != 3:
                        user_update.append(str(_))
                    if i == 3:
                        user_update.append(str(date_time_str))
                    if i == 4:
                        user_update.append(str(state))
                self.FM.write_file(f_name, user_update, "*", "w")



        except Exception as r:
            print("USER_UPDATE_ERROR: ", str(r))

    #LOGIN
    def Login_User(self, data):
        try:
            print("ATTEMPTING_LOGIN:: ", str(data))
            user = data.split("*")
            if len(user) >= 3:
                User = str(user[1]).translate(str.maketrans('','',string.punctuation))
                PSWD = str(user[2]).translate(str.maketrans('','',string.punctuation))
                print("USER   ::", User)
                print("PSWD   ::", PSWD)
                file_name = "USERS/"+User+".txt"

                try:
                    f_ret = self.FM.check_file(file_name)
                except Exception as e:
                    print("CHECK_FILE_ERROR", str(e))

                if f_ret != True:
                    print("USER_NOT FOUND")
                    return "NEW"
                elif f_ret == True:
                    print("F_RET", str(f_ret))
                    f_data = self.FM.read_file(file_name, "*")
                    #print("F_DATA:: ", str(f_data), "\nLEN:: ", str(len(f_data)))
                    if len(f_data) >= 3:
                        f_User = str(f_data[1])
                        f_pswd = str(f_data[2])
                        if str(f_pswd) == str(PSWD) and str(f_User) == str(User):
                            print("WELCOME_BACK: ", str(User))
                            return "OLD"
                        elif str(f_pswd) != str(PSWD) and str(f_User) == str(User):
                            print("CHECK_USER_ERROR")
                            return "PSWD_FAIL"
        except Exception as e:
            print("CHECK_USER_ERROR::: ", str(e))
            return "PSWD_FAIL"

    #REGISTER
    def Reg_User(self, data, client):
        try:
            print("ATTEMPTING_REGISTER:: ", str(data))
            user = data.split("*")
            if len(user) > 1:
                User = str(user[1]).translate(str.maketrans('','',string.punctuation))
                print("USER   ::", User)
                file_name = "USERS/"+User+".txt"
                f_ret = self.FM.check_file(file_name)
                if f_ret != True:
                    print("USER_NOT FOUND")
                    try:
                        return "NEW"
                    except Exception as e:
                        print("[FAILED_TO_REGISTER_USER]:", str(data), "\n>>", str(e))
                        return "FAILED"

                else:
                    print("WELCOME_BACK", str(User))
                    return "OLD"


        except Exception as e:
            print("CHECK_USER_ERROR::: ", str(e))

    #CREATE_USER_FILE
    def create_pl(self, data, client):
        #USER_FILE:: 
        #   >[0] = action
        #   >[1] = user_name
        #   >[2] = pswd
        #   >[3] = client_data....(NOT_NOW){TO_MUCH_BS}
        #   >[4] = status
        #   >[5] = contact_list{FILE_NAME}
        #   >[6] = msgs{FILE_NAME} : delim = "%"

        #print("CHECKING_USER", data)
        user = data.split("*")
        User = str(user[1]).translate(str.maketrans('','',string.punctuation))
        PSWD = str(user[2]).translate(str.maketrans('','',string.punctuation))

        try:
            file_name = "USERS/"+User+".txt"
            msgs_folder = "MSGS/"+User
            contacts_file = "CONTS/"+User+".txt"
            new_ = "USER*"+User+"*"+PSWD+"*"+"__CLIENT__"+"*"+"ONLINE"+"*"+contacts_file+"*"+msgs_folder+"*"
            print("NEW__:: ", str(new_))
            self.FM.make_dir(msgs_folder)
            self.FM.write_file(file_name, new_, "*", "w")
            self.FM.write_file(contacts_file, "EMPTY", "%", "w")
            return new_
        except Exception as e:
            print("CREATE_USER_ERROR:", str(e))
            return "FAIL"

    # MESSAGING
    def msg_to(self, data):
        ###
        #	|-MSGS/
    	#    	|-User1/
    	#   		|-User2.txt -> "<date_time_1>$<msg_1>$<received_1>$&<date_time_2>$<msg_2>$<received_2>$&"

        file_name = ""
        to_user = ""
        of_user = ""
        the_msg = ""
        to_send =  ""
        check_file =  False
        ret_ = ""

        print("\n\nGET_MSG\n\n>>>", str(data))
        break_msg = data.split("*")
        if len(break_msg) > 3:
            print("TO : ", str(break_msg[1]))
            to_user = str(break_msg[1])
            print("OF : ", str(break_msg[2]))
            of_user = str(break_msg[2])
            print("MSG: ", str(break_msg[3]))
            the_msg = str(break_msg[3])

            # DATE_TIME_STAMP
            # Get the current date and time
            now = datetime.now()

            # Format the date and time as a string in the desired format
            date_time_str = now.strftime("%Y-%m-%d-%H-%M")
            to_send = "*"+date_time_str+"*"+the_msg
            print("TO_SAVE:: ", str(to_send))


            file_name = "MSGS/"+to_user+"/"+of_user+".txt"
            print("FILE-> ", str(file_name))

        check_file = self.FM.check_file(file_name)
        if check_file == True:
            print("[ACCESS_GRANTED]")
            self.FM.write_file(file_name, to_send, "&", "a")
            ret_ = "MSG*SAVED*"+to_user+"*"+to_send+"*"
            return ret_

        else:
            print("[ACCESS_DENIED]")
            return "MSG*ACCESS_DENIED*"+to_user+"*"+to_send+"*"

        # CONFIGURE THE 






        # WRITE MSG TO FILE

        # CHECK IF CLIENT IS ONLINE
            # SEND MSG ["DELIM","OF", "MSG"]
        #uc_state = self.get_user_state(str(break_msg[1]))
        #if "ONLINE" in uc_state:
        #    # GET CURRENT IP ADDRESS
        #    f_name = f"USERS/{to_user}.txt"
        #    to_data = self.FM.read_file(f_name, "*")
        #    if len(to_data) >= 6:
        #        msgs_file = f"MSGS/{str(to_user)}.txt"
        #        self.write_file(msgs_file, to_send, "&", "a")
        #        return "SAVED"
        #    else:
        #        return "FAILED"


    def msg_of(self, data):
        print("MSG_OF:: ", str(data))
        dataLs = data.split("*")
        ret_lst = []

        dir_of = "MSGS/"+str(dataLs[1])+"/"
        dir_to = "MSGS/"+str(dataLs[2])+"/"


        print(f"DIR_OF:: {dir_of} \n DIR_TO:: {dir_to}")

        if "ALL" in str(dataLs[2]):
            msgs_all = self.FM.get_file_data(dir_of)
            if msgs_all:
                return "MSGS_ALL*"+str(msgs_all)
            else:
                return "MSGS&ERROR"

        if "ALL" not in data and len(dataLs) >= 3:
            # COLLECT RECV MSGS
            file_name = dir_of+str(dataLs[2])+".txt"
            msg_from = self.FM.read_file(file_name, "&")
            if msg_from:
                for m_ in msg_from:
                    ret_lst.append(str(dataLs[2]) + "*" + str(m_) + "&")
                    print("[MSG_OF]:", str(dataLs[2]) + "*" + str(m_) + "&")

            # CELLECT SENT MSGS
            my_file = dir_to+str(dataLs[1])+".txt"
            msg_to = self.FM.read_file(my_file, "&")
            if msg_to:
                for m_ in msg_to:
                    ret_lst.append(str(dataLs[1]) + "*" + str(m_) + "&")
                    print("[MSG_TO]:", str(dataLs[1]) + "*" + str(m_) + "&")
            ret_ = self.lst_to_str(ret_lst, "&")
            return "MSGS_OF*USER$"+ret_
        else:
             return "MSGS&ERROR"


    #CLIENT_THREAD_HANDLE
    def handle_client(self, conn, addr):
        try:
            connections = True
            self.user = ""
            user = ""
            self.active = False
            get_conts = False
            client = []
            client = [conn, addr]
            print("[Client]:[CONNECTED]:", str(client))
            data = ""
            self.data = ""
            data_len = 0
            pl = ""
            self.E = threading.Event()
            self.reply(conn, "WELCOME")
        except Exception as e:
            print("[ERROR_SETTING_VARIABLES]: ", str(e))
        while connections == True:
            #print("[CURRENT_USER] :: ", str(self.user))
            #if len(user) > 0:
            #    self.update_User(client, user, "ONLINE")
            #    print(f"[SELF.USER]::{addr}::[ONLINE]::{user}")
            try:
                try:
                    try: # GET IN_BOUND
                        data_len = int(conn.recv(64).decode())
                        if not data_len:
                            #print("WAITING_DATA_LEN:: ")
                            self.E.wait()
                        #print("[DATA_LEN]: ", str(data_len))
                        if data_len > 0:
                            #print("[WAITING]:>:[IN_COMM]")
                            self.data = str(conn.recv(data_len).decode())
                            if not self.data:
                                self.E.wait()                                
                            else:
                                data = self.data
                                #print("[IN_COMM]:self: ", str(self.data))
                                self.data = ''
                                #print("[IN_COMM]:data: ", str(data))
                    except:
                        print(f'[CLIENT_DISCONNECTED]: {addr} ')
                        if user:
                            self.update_User(client, user, "OFFLINE")
                            print(f"[DISCONN]::{addr}::[LOGGED_OFF]::{user}")
                            connections = False
                        sys.exit(1)


                    # MESSAGING
                    if "MSG_TO" in data:
                        print("[MSG_TO]:", str(data))
                        ret_ = self.msg_to(data)
                        if ret_:
                            self.reply(conn, ret_)
                        else:
                            self.reply(conn, "ERROR*LOGGING*MSG")
                        continue

                    if "MSG_OF" in data:
                        print("[MSG_OF]:", str(data))
                        ret_ = self.msg_of(data)
                        if ret_:
                            self.reply(conn, ret_)
                        else:
                            self.reply(conn, "ERROR*LOGGING*MSG")                            
                        continue


                    #OFFLINE
                    if "OFFLINE" in data:
                        print(f'[ATTEMPT_LOGG_OFF]::{addr}::{user}\n::[DATA]::{data}')
                        self.reply(conn, "GOODBYE")
                        self.active = False
                        data_list = str(data).split("*")
                        user = str(data_list[1])
                        if len(user) >= 1:
                            self.update_User(client, str(data_list[1]), "OFFLINE")
                            print(f"[LOGG_OFF]::{addr}::[LOGGED_OFF]::{user}::{str(data_list[1])}")
                            connections = False
                            return

                    #GET_STATE
                    if "GET_STATE" in data:
                        #print("GET_STATE::: >>")
                        data_list = str(data).split("*")
                        target_user = str(data_list[2])
                        state = self.get_user_state(target_user)
                        state_val =  "STATE*"+str(state)
                        self.reply(conn, state_val)

                    #PROFILE_HANDLE

                    #CONTACT_LOADER
                    if "NEW_C" in data: # and self.get_conts == False:
                        try:
                            data_list = str(data).split("*")
                            if len(data_list) > 2:
                                print(f"ADDING_NEW_CONT:: for {str(data_list[1])}\nReq:: {str(data_list[2])}")
                            if data_list:
                                conts_list = self.add_Cont(data_list)
                                if conts_list:
                                    if "NOT_FOUND*" in conts_list:
                                        print("NO SUCH USER", str(data_list[2]))
                                        self.reply(conn, "CONTS*FAIL"+str(data_list[2]))

                                    else:
                                        self.get_conts = True
                                        self.reply(conn, "ADD_C*"+str(conts_list))
                                    continue

                            else:
                                print("[NEW_CONTS_ERROR]::")
                                self.reply(conn, "CONTS*ERROR")
                        except Exception as e:
                            print("[CONT_LOADING]::ERROR", str(e))
                    #GET_CONTACTS
                    if "CONTS" in data and get_conts == False:
                        try:
                            if "^^" in data:
                                continue
                            #print("GETTING_CONTS:: ", str(data))
                            data_list = str(data).split("*")
                            #print("USERS_LIST:: ", str(data_list))
                            if len(data_list) > 1:
                                #print("DATA_LIST:", str(data_list))
                                try:
                                    set_ = str(data_list[1])
                                    #print("[GET_CONTS]::", str(set_))
                                    if set_:
                                        conts_list = self.Get_Contacts(set_)
                                    else:
                                        print("[FAILED]::[LOADING_CONTS]")
                                except Exception as e:
                                    print("CONTS_LIST_ERROR:: ", str(e))

                                if "EMPTY" in conts_list:
                                    print("CONTS_LIST_EMPTY")
                                    self.reply(conn, "CONTS*EMPTY%0")
                                    data_list = []
                                    get_conts = True
                                    pass

                                if "EMPTY" not in conts_list:
                                    self.reply(conn, "CONTS$"+str(conts_list))
                                    pass
                            else:
                                print("[CONTS]:[MISSING_ARGS]")
                                # MAKE REROUTE...
                                pass
                        except Exception as e:
                            print("[CONTS_GLITCH]:: ", str(e))
                            #self.reply(conn, "CONTS*ERROR")
                            pass
                    #REGISTER
                    if "REG" in data:
                        try:
                            print("REG_NEW_USER::: ", str(data))
                            t = self.Reg_User(data, client)
                            if "NEW" in t:
                                pl = self.create_pl(data, client)
                                self.reply(conn, "REG_ED")
                                print('NEW_USER:: ', str(pl))
                            if "FAILED" in t:
                                self.reply(conn, "FAILED_REG")
                                print('NEW_USER:: ', str(pl))
                            if "OLD" in t:
                                self.reply(conn, "PLEASE_LOGIN")
                                print("[SENT]: PLEASE_LOGIN:: " )

                        except Exception as e:
                            print("CHECK_PLAYER::ERROR:: ", str(e))
                    #LOGIN
                    if "LOGIN" in data and self.active == False:
                        try:
                            data_list = str(data).split("*")
                            user = str(data_list[1])
                            if user:
                                print("[SETTING]_[USER] :: ", str(user))

                            t = self.Login_User(data)
                            if "NEW" in t:
                                try:
                                    self.reply(conn, "PLEASE_REGISTER")
                                    print('NEW_USER:: ')
                                    pass
                                except Exception as e:
                                    print("NEW___EROOR", str(e))
                            elif "OLD" in t:
                                self.reply(conn, "LOGIN")
                                print("LOGGING_IN:: ", str(data))
                                self.active = True
                                self.update_User(client, user, "ONLINE")

                                pass
                            elif "PSWD_FAIL" in t:
                                self.reply(conn, "PSWD_FAIL")
                                print("PSWD_FAIL")
                                pass
                            pass
                        except Exception as e:
                            print("CHECK_PLAYER::ERROR:: ", str(e))

                except Exception as e:
                    print('CLIENT_HANDLE_ERROR: ', str(e))
                    if user:
                        self.update_User(client, user, "OFFLINE")
                        print(f"[CL_ERROR]::{addr}::[LOGGED_OFF]::{user}")
                        connections = False
                    sys.exit(1)

            
            except Exception as e:
                print("[FAILED_TO_RECEIVE]: ", str(e))
                if user:
                    self.update_User(client, user, "OFFLINE")
                    print(f"[RCV_ERROR]::{addr}::[LOGGED_OFF]::{user}")
                    connections = False
            finally:
                #print("RESETTING_LOOP")
                data = ""
                data_len = 0
                self.data = ''
        if user:
            self.update_User(client, user, "OFFLINE")
            print(f"[EXT_LOOP]::{addr}::[LOGGED_OFF]::{user}")
        print("[LOOP_EXITED]:",str(user))
        return

    # THREAD CHECKER
    def check_and_join_threads(self):
        while True:
            for thread in self.threads:
                if isinstance(thread, threading.Thread) and thread.is_alive():
                    #print(str(thread), "IS_ACTIVE")
                    continue  # Thread is still active, skip it
                elif isinstance(thread, threading.Thread):
                    print(str(thread), "NOT_ACTIVE")
                    thread.join()  # Thread is no longer active, join it
                    self.threads.remove(thread)

    #MAIN_CLIENT_HANDLE
    def Main(self):
        print("[STARTING_THREAD_CHECKER]")
        threading.Thread(group=None, target=self.check_and_join_threads).start()


        #BIND_INCOMING_CONNECTION
        try:
            self.sock.bind(('', self.port))
            print("[BINDING] ")
        except Exception as e:
            print("NOT BINDING: ", str(e))
        #LISTEN
        try:
            # CAN CURRENTLY HANDLE 50 CLIENTS 
            self.sock.listen(50)
            print("[LISTENING]:")
        except Exception as e:
            print("[ERROR_LISTENING]", str(e))
        #CONNECTION THREADING_LOOP
        while True:
            try:
                conn, addr = self.sock.accept()
            except socket.error as e:
                print("[ERROR_CONNECTING_NEW_CLIENT] :", str(e))        
            try:
                t1 = threading.Thread(group=None, target=self.handle_client, args=(conn, addr))
                #t1.daemon = True
                t1.start()
                self.threads.append(t1)
                #print("[NEW_THREAD]:", str(t1))
            except ThreadError as e:
                print(f'SERVER::MAIN:: {str(e)}')

if __name__=="__main__":
    s = server()
    s.Main()
