import subprocess
from PyQt5.QtCore import QThread
import time


class BackgroundProcess(QThread):
    def __init__(self, main_window, commands=None):
        super().__init__()
        if commands is None:
            commands = [("echo", "Empty")]
        self.main_window = main_window
        self.commands = commands
        self.max_rows = 8

    def run(self):
        logfile = open(f'logs/log{time.ctime()}', 'w')
        logfile.write(f"Start. Commands: {str(self.commands)}\n")
        self.disableUI()
        self.main_window.terminal.clear()
        self.main_window.terminal.addItem("Thread running...")
        for command in self.commands:
            # split my command string to args

            self.main_window.terminal.addItem(f"Trying command...")
            self.main_window.terminal.addItem(str(command))
            proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, universal_newlines=True, bufsize=2)
            self.main_window.terminal.addItem("")
            for line in proc.stdout:
                logfile.write(f"{str(line.rstrip())}\n")
                self.main_window.terminal.addItem(line.rstrip())
                self.cleanT()
            self.main_window.terminal.addItem(f"Done")
            self.enableUI()
            logfile.close()
            self.terminate()

    def cleanT(self):
        if self.main_window.terminal.count() > self.max_rows:
            self.main_window.terminal.clear()

    def disableUI(self):
        self.main_window.run_button.setEnabled(False)
        self.main_window.select_file_button.setEnabled(False)
        self.main_window.toolButton.setEnabled(False)
        self.main_window.command_selector.setEnabled(False)

    def enableUI(self):
        self.main_window.toolButton.setEnabled(True)
        self.main_window.run_button.setEnabled(True)
        self.main_window.select_file_button.setEnabled(True)
        self.main_window.command_selector.setEnabled(True)
