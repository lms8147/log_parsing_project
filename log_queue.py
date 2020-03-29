

'''
import threading, queue
import time


class Catcher(threading.Thread):  # Thread Extends
    def __init__(self, id, dataQueue):
        threading.Thread.__init__(self)
        self.id = id  # for print
        self.dataQueue = dataQueue  # data queue

    def run(self):
        while True:  # thread task
            data = self.dataQueue.get()  # queue element get

            print("[" + str(self.id) + " : " + str(data) + "]")

            self.dataQueue.task_done()  # work done notify to queue


def main():
    StringQueue = queue.Queue()  # create queue
    StringQueue.put(1)  # put data
    StringQueue.put(2)



    cat1 = Catcher("A", StringQueue)  # declare thread obj
    cat1.setDaemon(True)

    cat2 = Catcher("B", StringQueue)
    cat2.setDaemon(True)

    cat1.start()  # thread start
    cat2.start()

    time.sleep(5)

    StringQueue.put(3)
    StringQueue.put(4)

    cat1.dataQueue.join()  # wait for data queue empty
    cat2.dataQueue.join()

'''

#if __name__ == "__main__":
    #main()

