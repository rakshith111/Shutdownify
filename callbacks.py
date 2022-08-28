import subprocess
from datetime import datetime
import re
from threading import Timer


class callback():
    def __init__(self):
        current_power_scheme_cmd = subprocess.run(["powercfg ", "/GetActiveScheme"],  shell=False,
                                                  stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        self.current_power_scheme_guid = re.search(r'\w+-\w+-\w+-\w+-\w+',
                                                   str(current_power_scheme_cmd.stdout)).group()

        current_sleeper = subprocess.run(["powercfg", "/q",  f'{self.current_power_scheme_guid}', "SUB_VIDEO", "VIDEOIDLE"],  shell=False,
                                         stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        searchhex = re.search(
            r'AC Power Setting Index:\s\w+', str(current_sleeper.stdout)).group()
        # int value of the AC power setting index
        self.current_sleeper_seconds = int(searchhex[24:], 16)
        self.input_seconds = 0
        print(self.current_sleeper_seconds)

    def sleeper_action(self, state=True):
        if state and self.input_seconds > 10:
            print(f"Activated for {self.input_seconds-10} seconds")
            # subprocess.run(["powercfg ", "/SETACVALUEINDEX", f'{self.current_power_scheme_guid}', "SUB_VIDEO", "VIDEOIDLE", "30"],  shell=False,
            # stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            t = Timer(self.input_seconds-10, self.sleep_reset)
            t.start()

    def sleep_reset(self):
        print("restting")
        # TO set custom sleep time
        # subprocess.run(["powercfg ", "/SETACVALUEINDEX", f'{self.current_power_scheme_guid}', "SUB_VIDEO", "VIDEOIDLE", "self.current_sleeper_seconds"],  shell=False,
        #   stdout = subprocess.PIPE, stdin = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

    def submit(self, seconds):

        self.base_time = datetime.now()
        self.input_seconds = seconds

        subprocess.run(["shutdown", "-s", "-t", f"{self.input_seconds}"],  shell=False,
                       stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def extend(self, seconds):

        if (self.base_time is None):  # Fails if the user tries to extend the timer before starting it
            return False
        else:
            print(self.base_time)
            subprocess.run(["shutdown", "-a"],  shell=False, stdout=subprocess.PIPE,
                           stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.elapsedtime = (datetime.now() - self.base_time).seconds
            self.input_seconds = self.elapsedtime+seconds
            self.submit(self.input_seconds)
            return True

    def cancel(self):
        # if you want to cancel
        subprocess.run(["shutdown", "-a"],  shell=False, stdout=subprocess.PIPE,
                       stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
