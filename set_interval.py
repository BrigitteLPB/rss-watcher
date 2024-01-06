import time, threading


class SetInterval:
    def __init__(self, interval: float, action, start_immediatly: bool = False):
        """
        interval : in second
        start_immediatly : true, start by executing the action
        """
        self.interval = interval
        self.action = action
        self.start_immediatly = start_immediatly
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval

        if self.start_immediatly:
            self.action()

        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()
