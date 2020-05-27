import time
from threading import Thread

# a good blog https://realpython.com/intro-to-python-threading/
    

def thread_function(name):
    print(f"Thread {name} starting")
    time.sleep(2)
    print(f"Thread {name} end")

if __name__ == '__main__':
    # to temp remove the daemon, you will see main program will wait for the 
    # non-daemonic thread to complete. Fore more detail, you can see the cource
    # https://github.com/python/cpython/blob/df5cdc11123a35065bbf1636251447d0bfe789a5/Lib/threading.py#L1263
    # the part of code
    # t = _pickSomeNonDaemonThread()
    # while t:
    #   t.join()
    # . t = _pickSomeNonDaemonThread()
    t = Thread(target=thread_function, args=(1,), daemon=True)

    print("main: before create thread")
    t.start()
    print("main: wait thread complete")

    # t.join() # this will wait the thread complete whether it is daemon or not.
    print("main: after thread complete")
