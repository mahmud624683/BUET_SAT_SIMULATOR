import threading
import time, os
import algo_methods,signal

class ThreadController:
    def __init__(self,name):
        self.thread = threading.Thread(target=self.child_thread,args=(name,))
        self.pid = None

    def child_thread(self,name):
        self.pid = os.getpid()
        print("Child thread started.")
        

    def start(self):
        self.thread.start()

    def stop(self):
        if self.pid != None:
            try:
                os.kill(self.pid, signal.SIGTERM)
            except:
                print("error in terminating the process")
        self.thread.join()

def main():
    controller = ThreadController("mahmud")
    
    # Start the child thread
    controller.start()
    
    # Main thread sleeps for 20 seconds
    print("Main thread sleeping for 20 seconds...")
    time.sleep(10)
    
    # Stop the child thread
    controller.stop()
    print("Main thread exiting.")

if __name__ == "__main__":
    main()
