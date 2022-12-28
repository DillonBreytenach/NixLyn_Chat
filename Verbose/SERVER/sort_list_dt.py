import time
from datetime import datetime
from dateutil import parser

class SortMsgs():
    def __init__(self, **kw):
        super(SortMsgs, self).__init__(**kw)


    def stack_msgs(self, data):
        cont_ = ""
        file_name = ""
        collected_ = ""
        data_break = []
        buff_lst = []
        temp_msg = []
        shifted = []

        if "ACCESS_DENIED" in data:
            self.FM.write_file("SOCKET_DATA/MSG_OF.txt", data, "*", "w")

        if "MSGS_OF" in data:
            try:

                print("[STACK_MSGS]:: ", str(data))
                data_break = data.split("@")
                print("[DATA_BREAK][0]:", data_break[0])
                print("[DATA_BREAK][1]:", data_break[1])

                if "*" in str(data_break[0]):
                    cont_ = str(str(data_break[0]).split("*")[1])

                if "$" in str(data_break[1]):
                     # CONVERT MSGS TO A LIST OF LISTS
                    msg_list = str(data_break[1]).split("$")
                    for i, val in enumerate(msg_list):
                        temp_msg = val.split("*")
                        if "INVITE" in str(temp_msg) or "MSGS_OF" in str(temp_msg) or len(temp_msg) < 4:
                            pass
                        else:
                            print("TEMP_MSG:: ", str(temp_msg))
                            buff_lst.append(temp_msg)


                    for msg in buff_lst:
                        print("[STACK_ED]::", str(msg))



                    file_name = f"MSGS/{cont_}.txt"
                    self.FM.write_file(file_name, "", "$", "w")
                    self.FM.write_file(file_name, str(data_break[1]), "$", "w")

                # FOR TESTING ONLY
                return buff_lst
                # ^^^^^^^^^^^^^^^^
            except Exception as e:
                print("[ERROR]::[STACK_MSGS]::",str(e))







    # TIME SHIFT
    def time_shift_0(self, buff_lst, dt_q, Q):
        try:

            if Q >= len(buff_lst):
                return buff_lst

            older_msg = []
            newer_msg = []


            # ITERATE THROUGH THE BUFFER 

            for l, val_l in enumerate(buff_lst):
                #time.sleep(5)
                dt_l = datetime.strptime(str(val_l[2]), "%Y-%m-%d-%H-%M-%S")
                print("\n[Q]::<", str(Q), "> ## [L]::<", str(l),">\n \nVal_l", str(val_l))
                if dt_q == dt_l:
                    print("[SAME]:[DT_Q]:", str(dt_q), "\n   [==]\n[SAME]:[DT_L]:", str(dt_l), "\n>>[GOOD]")
                    pass
                # CHECK THE DATETIME VALUE
                if dt_q > dt_l:
                    # DT_Q < DT_L ==>> DT_Q OLDER
                    # CURRENT_INDEX [DATE] IS NEWER THAN GIVEN INDEX [DATE] :: PASS
                    print("[OLDER]:[DT_Q]:", str(dt_q), "\n[<]\n[NEWER]:[DT_K]:", str(dt_l), "\n>>[GOOD]")# \n[J]::<", str(i), "> ## [K]::<", str(k),">\n")
                    pass
                if dt_q < dt_l:
                    # DT_Q > DT_L ==>> DT_Q NEWER
                    # CURRENT_INDEX [DATE] IS OLDER THAN GIVEN INDEX [DATE] :: FAIL
                        # SWOP VAL INDEX_s AND RECURSE
                    print("[NEWER]:[DT_J]:", str(dt_q), "\n[>]\n[OLDER]:[DT_K]:", str(dt_l), " \n>>[FIX]!!") # \n[J]::<", str(j), "> ## [K]::<", str(k),">\n")
                    older_msg = buff_lst[l]
                    newer_msg = buff_lst[Q]

                    buff_lst[l] = newer_msg
                    buff_lst[Q] = older_msg

                    print("[NEW_POS]:[OLDER]:", str(buff_lst[Q]), "\n@ ", str(Q))
                    print("[NEW_POS]:[NEWER]:", str(buff_lst[l]), "\n@ ", str(l))

                    print("VALUES_SWAPPED \n    Check >>", )
                    #time.sleep(5)
                    for i in buff_lst:
                        print("NEW_STACK: ", str(i))
                    #self.time_shift(buff_lst)
                    #time.sleep(5)
                #buff_lst = self.time_shift_0(buff_lst, dt_l, Q+1)



                #time.sleep(5)
                print("[END_ITER]\n__\n")
            print("[END_LOOP]")
            for i in buff_lst:
                print("BUFF_ITEM: ", str(i))




            return self.time_shift_0(buff_lst, dt_l, Q+1)
        except Exception as e:
            print("[ERROR]::[MSG_OF]::[RE_ORDER]::[TIME_SHIFT]", str(e))






    # USE buff[j] and buff[j-1] while j > len(buff)







    # REORDER BY DATE-TIME
    def re_order(self, data):
        try:
            ret_str = ""
            buff_lst = []
            temp_msg = []
            shifted = []
            the_dt = ""

            # CONVERT MSGS TO A LIST OF LISTS
            msg_list = data.split("$")
            for i, val in enumerate(msg_list):
                temp_msg = val.split("*")
                if "INVITE" in str(temp_msg) or "MSGS_OF" in str(temp_msg) or len(temp_msg) < 4:
                    pass
                else:
                    print("TEMP_MSG:: ", str(temp_msg))
                    buff_lst.append(temp_msg)
            try:

                for i, val_f in enumerate(buff_lst):
                    print("VAL_F: ", str(val_f))
                    dt_q = datetime.strptime(str(val_f[2]), "%Y-%m-%d-%H-%M-%S")
                    print("DT_Q: ", str(dt_q))
                    shifted = self.time_shift_0(buff_lst, dt_q, i)
                
                shifted.reverse()
                for what in shifted:
                    print("SHIFT:  ", str(what))
            
            except Exception as e:
                print("[ERROR]::[MSG_OF]::[RE_ORDER]::[START_FILT]", str(e))
            return shifted
        except Exception as e:
            print("[ERROR]::[MSG_OF]::[RE_ORDER]")






if __name__=="__main__":
    data = """
    MSGS_OF*USER$U3*INVITE_FROM*U4*TO*U3*
    $U4**2022-12-27-03-08-21*3rd_MSG
    $U3**2022-12-27-02-18-10*2nd_MSG
    $U4**2022-12-27-09-08-21*LAST_MSG
    $U4**2022-12-27-05-08-21*5th_MSG
    $U3**2022-12-27-04-18-22*4th_MSG
    $U4**2022-12-27-01-08-21*FIRST_MSG
    $U4**2022-12-28-07-08-21*7th_update\\n \n \\\n  \n
    $U3**2022-12-28-06-18-19*6th_update
    $U3**2022-12-28-02-18-19*2th_update
    $U3**2022-12-28-01-18-19*1th_update
    $U3**2022-12-28-03-18-19*3th_update
    $U3**2022-12-28-08-18-19*8th_update\n \\n \\\n\\\\n \\n \\n
    $U3**2022-12-28-04-18-19*4th_update
    $U3**2022-12-28-13-18-19*13th_update
    $U3*INVITE_FROM*U4*TO*U3*
    """
    SM = SortMsgs()
    #SM.re_order(data)
    SM.stack_msgs(data)