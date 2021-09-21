
import time

from akit.xmultiprocessing.webserverprocess import spawn_webserver_process

if __name__ == "__main__":
    rootdir = "~/akit/results/testresults"
    mgr, wsvr = spawn_webserver_process(("", 0), rootdir)

    while True:
        print("Server On: {}".format(wsvr.get_server_address()))
        time.sleep(30)
