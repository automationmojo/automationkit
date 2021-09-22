
import time

from akit.xmultiprocessing.webserverprocess import spawn_webserver_process

if __name__ == "__main__":
    rootdir = "~/akit/results/"
    mgr, wsvr = spawn_webserver_process(("", 0), rootdir)

    counter = 0
    while True:
        if counter % 5 == 0:
            print("")
            print("Server On: {}".format(wsvr.get_server_address()))
            print("")
        
        print("doing some testing...")

        time.sleep(5)
        counter += 1
