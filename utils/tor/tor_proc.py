import subprocess
import time
import os
import settings

class TorProcess:
    def __init__(self):
        self.__tor_process = None

    def start_tor_background(self):
        if self.__tor_process:
            settings.logger.info("Tor process is already running")
        else:
            tor_path = os.path.expandvars(settings.tor_path)
            tor_process = subprocess.Popen([
                tor_path,
                "--SocksPort", "9150",
                "--ControlPort", "9051",
                "--CookieAuthentication", "1"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            settings.logger.info("Tor started")
            time.sleep(settings.min_time_to_sleep)
            self.__tor_process = tor_process

    def terminate(self):
        if self.__tor_process is  not None:
            self.__tor_process.terminate()
            settings.logger.info("Tor terminated")
            self.__tor_process = None
        else:
            settings.logger.info("Tor process is not running now")

    def restart_tor_process(self):
        settings.logger.info("Restarting tor process")
        if self.__tor_process is not None:
            self.terminate()
            time.sleep(settings.min_time_to_sleep)
            self.start_tor_background()
