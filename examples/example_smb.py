
import time

from akit.xmultiprocessing.smbserverprocess import spawn_smbserver_process

if __name__ == "__main__":
    rootname = "results"
    rootdir = "~/akit/results/"
    smblogfile = "~/akit/smblog.txt"

    mgr, wsvr = spawn_smbserver_process(rootname, rootdir, endpoint=("", 54321), logfile=smblogfile)

    counter = 0
    while True:
        if counter % 5 == 0:
            print("")
            print("Server On: {}".format(wsvr.getServerAddress()))
            print("")
        
        print("doing some testing...")

        time.sleep(5)
        counter += 1
