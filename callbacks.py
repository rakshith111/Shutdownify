import subprocess
from datetime import datetime
import re


class callback():
    def __init__(self):
        current_power_scheme_cmd = subprocess.run(["powercfg ", "/GetActiveScheme"],  shell=False,
                                                  stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        current_power_scheme_guid = re.search(r'\w+-\w+-\w+-\w+-\w+',
                                              str(current_power_scheme_cmd.stdout)).group()

        current_sleeper = subprocess.run(["powercfg", "/q",  f'{current_power_scheme_guid}', "SUB_VIDEO", "VIDEOIDLE"],  shell=False,
                                         stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        searchhex = re.search(
            r'AC Power Setting Index:\s\w+', str(current_sleeper.stdout)).group()
        # int value of the AC power setting index
        current_sleeper_seconds = int(searchhex[24:], 16)
        # TO set custom sleep time
        subprocess.run(["powercfg ", "/SETACVALUEINDEX", f'{current_power_scheme_guid}', "SUB_VIDEO", "VIDEOIDLE", "800"],  shell=False,
                       stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def submit(self, seconds):

        self.base_time = datetime.now()

        subprocess.run(["shutdown", "-s", "-t", f"{seconds}"],  shell=False,
                       stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def extend(self, seconds):

        if (self.base_time is None):  # Fails if the user tries to extend the timer before starting it
            return False
        else:
            print(self.base_time)
            subprocess.run(["shutdown", "-a"],  shell=False, stdout=subprocess.PIPE,
                           stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.elapsedtime = (datetime.now() - self.base_time).seconds

            self.submit(self.elapsedtime+seconds)
            return True

    def cancel(self):
        # if you want to cancel
        subprocess.run(["shutdown", "-a"],  shell=False, stdout=subprocess.PIPE,
                       stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
