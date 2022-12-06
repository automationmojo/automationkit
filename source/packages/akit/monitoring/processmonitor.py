
import json
import os
import shutil
import datetime

from akit.environment.system import SYSTEM_NAME
from akit.interop.agents.sshagent import SshAgent
from akit.monitoring.reportmonitor import ReportMonitor
from akit.jsos import CHAR_RECORD_SEPERATOR

DIR_MONITORING = os.path.dirname(__file__)

DIR_PROCESS_MONITOR_SCRIPT = os.path.join(DIR_MONITORING, "scripts", "platforms", SYSTEM_NAME.lower(), "monitor_pid")
HTML_TEMPLATE_PROCESS_MONITOR = os.path.join(DIR_MONITORING, "templates", "processmonitor.html")

CMD_TEMPLATE_MONITOR_PID = "REPTOPIC={topic} PROCEXP={pexp} RSERVER={rip} RPORT={rport} RINTERVAL={interval} {monitor} 2> /tmp/monitor_pid.err < /dev/null & "

class ProcessMonitor(ReportMonitor):

    def __init__(self, reporting_ip:str, process_name: str, report_leaf: str="process-monitor", interval: int=15,
                 device_id_lookup: dict=None, correspondance_ip: str=None, chk_port: int=22):
        super().__init__(reporting_ip, "monitor/process", process_name, report_leaf, "process-heartbeats.jsos", interval=interval,
                         correspondance_ip=correspondance_ip, chk_port=chk_port)
        self._process_name = process_name
        self._device_id_lookup = device_id_lookup
        self._process_exp = "[{}]{}".format(self._process_name[:1], self._process_name[1:])

        return

    def finalize_report(self):
        dest_file = os.path.join(self._report_dir, "index.html")
        shutil.copy2(HTML_TEMPLATE_PROCESS_MONITOR, dest_file)
        return

    def deploy_helper_via_ssh(self, sshagent, remote_dir):
        helper_file = self.get_helper_script()

        base_helper_file = os.path.basename(helper_file)
        remote_helper_file = os.path.join(remote_dir, base_helper_file)

        sshagent.file_push(helper_file, remote_helper_file)

        chmod_cmd = "chmod +x {}".format(helper_file)
        sshagent.run_cmd(chmod_cmd)

        run_helper_cmd = self.get_helper_command(remote_dir, remote_helper_file)

        sshagent.run_cmd(run_helper_cmd)

        return

    def get_helper_script(self) -> str:
        return DIR_PROCESS_MONITOR_SCRIPT

    def get_helper_command(self, remote_dir, remote_helper_file):

        fill_dict = {
            "rip": self._report_to_ip,
            "rport": self._report_to_port,
            "interval" : self._report_interval,
            "monitor": remote_helper_file,
            "topic": self._report_topic,
            "pexp": self._process_exp
        }

        run_helper_cmd = CMD_TEMPLATE_MONITOR_PID.format_map(fill_dict)

        return run_helper_cmd

    def process_report(self, ipaddr, rep_content):

        try:
            procid = rep_content

            now = datetime.datetime.now()
            report = {
                "ip": ipaddr,
                "pid": procid,
                "time": now.isoformat()
            }

            if self._device_id_lookup is not None:
                report["devid"] = self._device_id_lookup[ipaddr]

            with open(self._report_file, 'a') as rf:
                rf.write(CHAR_RECORD_SEPERATOR)
                json.dump(report, rf)
        except:
            import traceback
            errmsg = traceback.format_exc()
            print(errmsg)

        return
