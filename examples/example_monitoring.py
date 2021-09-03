
import os
import time

from akit.integration.agents.sshagent import SshAgent
from akit.monitoring.processmonitor import ProcessMonitor
from akit.monitoring.reportingservice import ReportingService

def example_monitoring_main():

    password = os.environ["THEPASSWORD"]

    sshagent = SshAgent("192.168.1.50", "root", password, primitive=True)

    service = ReportingService()
    service.start()

    pmon = ProcessMonitor(sshagent.ipaddr, "anacapad")
    service.register_monitor(pmon)

    pmon.deploy_helper_via_ssh(sshagent, "/jffs")

    while True:
        print("tick")
        time.sleep(5)

    return

if __name__ == "__main__":
    example_monitoring_main()
