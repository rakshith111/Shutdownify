import subprocess
from datetime import datetime
import re
from threading import Timer


class callback():
    def __init__(self):
        # Get current power scheme guid
        current_power_scheme_cmd = subprocess.run(["powercfg ", "/GetActiveScheme"],  shell=False,
                                                  stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        self.current_power_scheme_guid = re.search(r'\w+-\w+-\w+-\w+-\w+',
                                                   str(current_power_scheme_cmd.stdout)).group()
        # Get current sleep time
        current_sleeper = subprocess.run(["powercfg", "/q",  f'{self.current_power_scheme_guid}', "SUB_VIDEO", "VIDEOIDLE"],  shell=False,
                                         stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Get current sleep time in senconds(hex)
        searchhex = re.search(
            r'AC Power Setting Index:\s\w+', str(current_sleeper.stdout)).group()
        # int value of the AC power setting index 
        self.current_sleeper_seconds = int(searchhex[24:], 16)
        # Initiate variables
        self.input_seconds = 0
        self.last_thread_state = False
        self.base_time = None
        print(self.current_sleeper_seconds)

    def sleeper_action(self, state=True):
        if state and self.input_seconds > 10:  # if the user has set a timer and the state is true
            print(f"Activated for {self.input_seconds-10} seconds")
            subprocess.run(["powercfg ", "/SETACVALUEINDEX", f'{self.current_power_scheme_guid}', "SUB_VIDEO", "VIDEOIDLE", "30"],  shell=False,
                           stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # Optimize / Update threading fo when canceled
            if not self.last_thread_state:
                self.t = Timer(self.input_seconds-10, self.sleep_reset)
                self.t.start()
                self.last_thread_state = True
            else:
                self.t.cancel()

    def sleep_reset(self):

        # TO set custom sleep time
        subprocess.run(["powercfg ", "/SETACVALUEINDEX", f'{self.current_power_scheme_guid}', "SUB_VIDEO", "VIDEOIDLE", f"{self.current_sleeper_seconds}"],  shell=False,
                       stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def submit(self, seconds):

        self.base_time = datetime.now()
        self.input_seconds = seconds
       # print("SHUTDOWN for {} seconds".format(self.input_seconds))
        subprocess.run(["shutdown", "-s", "-t", f"{self.input_seconds}"],  shell=False,
                       stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def extend(self, seconds):

        if (self.base_time is None):  # Fails if the user tries to extend the timer before starting it
            return False
        else:

            subprocess.run(["shutdown", "-a"],  shell=False, stdout=subprocess.PIPE,
                           stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.elapsedtime = (datetime.now() - self.base_time).seconds
            self.input_seconds = self.input_seconds-self.elapsedtime+seconds
           # print("SHUTDOWN for {} seconds".format(self.input_seconds))
            self.submit(self.input_seconds)
            return True

    def cancel(self):
        self.base_time = None
        # Cancel Command
        subprocess.run(["shutdown", "-a"],  shell=False, stdout=subprocess.PIPE,
                       stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
