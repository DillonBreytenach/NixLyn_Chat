import threading
import time

class Threading_test():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ls_threads = [1, 3, 4, 5, 2, 6, 7, 8, 9]


    def main_thread_proc(self, max_int, th):
        counts = 0
        while counts <= max_int:
            counts += 1
            print(f"TH::{str(th)}\nCOUNTS::{str(counts)}")
            time.sleep(1)

        if len(self.ls_threads) >= th:
            self.ls_threads[th] = 0
            print("THREAD_END: ", str(th), "::")


        return


    def check_and_join_threads(self, threads):
        for thread in threads:
            if isinstance(thread, threading.Thread) and thread.is_alive():
                print(str(thread), "IS_ACTIVE")
                continue  # Thread is still active, skip it
            elif isinstance(thread, threading.Thread):
                print(str(thread), "NOT_ACTIVE")
                thread.join()  # Thread is no longer active, join it
                threads.remove(thread)



    def Main(self):

        while self.ls_threads:
            for i, val in enumerate(self.ls_threads):
                if val != 0:
                    th = i
                    t1 = threading.Thread(group=None, target=self.main_thread_proc, args=(val, th))
                    t1.daemon= True
                    t1.start()
                    #self.check_and_join_threads(self.ls_threads)
                    print("[STARTING_]:: ",str(t1), ":i:", str(i), ":val:", str(val))
                else:
                    continue

                print("[NEW_THEAD]: ", str(th), "::")

            print("FOR_LOOP_DONE")

            self.check_and_join_threads(self.ls_threads)


        print("ALL_DONE")


Threading_test().Main()

