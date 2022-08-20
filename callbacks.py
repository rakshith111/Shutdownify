import subprocess
from datetime import datetime


class callback():

    def submit(self, seconds):

        self.basetime = datetime.now()

        subprocess.run(["shutdown", "-s", "-t", f"{seconds}"],  shell=False,
                       stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def extend(self, seconds):

        if (self.basetime is None):  # Fails if the user tries to extend the timer before starting it

            return False
        else:
            print(self.basetime)
            subprocess.run(["shutdown", "-a"],  shell=False, stdout=subprocess.PIPE,
                           stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.elapsedtime = (datetime.now() - self.basetime).seconds

            self.submit(self.elapsedtime+seconds)
            return True

    def cancel(self):
        # if you want to cancel
        subprocess.run(["shutdown", "-a"],  shell=False, stdout=subprocess.PIPE,
                       stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
