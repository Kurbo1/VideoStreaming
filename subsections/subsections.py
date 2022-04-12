from authentication.authentication import Authentication
from login.login import Login
import threading

class Subsection:
    def __init__(self):
        self.authentication = Authentication()
        self.log = Login()
        self.thread = threading.Thread(target=self.threadTarget, args=(self,))

    def threadTarget(self):
        None