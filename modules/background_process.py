import subprocess
from PyQt5.QtCore import QThread


class BackgroundProcess(QThread):
    def __init__(self, main_window, commands=None):
        super().__init__()
        if commands is None:
            commands = ["whoami"]
        self.main_window = main_window
        self.commands = commands

    def run(self):
        self.main_window.terminal.addItem("Thread running...")
        index = 0
        for command in self.commands:
            counter = 0
            self.main_window.terminal.addItem(f"({index}) Trying command...")
            self.main_window.terminal.addItem(command)
            proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, universal_newlines=True)
            while proc.poll() is None:
                counter += 1
            self.main_window.terminal.addItem("")
            for line in proc.stdout:
                self.main_window.terminal.addItem(line.rstrip())
            self.main_window.terminal.addItem(f"Done ({counter})")
            index += 1