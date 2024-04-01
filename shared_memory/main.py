import time
import os
import mmap

def sharing_with_mmap():
    shared_data = mmap.mmap(-1, length=100, access=mmap.ACCESS_WRITE)

    pid = os.fork()

    if pid == 0:
        shared_data[:100] = b"a" * 100
    else:
        time.sleep(1)
        print(dir(shared_data))
        print(shared_data[:100])

    # it's amazing 


if __name__ == "__main__":
    sharing_with_mmap()
