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
        self.main_window.terminal.clear()
        self.main_window.run_button.setEnabled(False)
        self.main_window.select_file_button.setEnabled(False)
        self.main_window.ffplay_run.setEnabled(False)
        self.main_window.terminal.addItem("Thread running...")
        for command in self.commands:
            self.main_window.terminal.addItem(f"Trying command...")
            self.main_window.terminal.addItem(command)
            proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, universal_newlines=True, bufsize=2)
            self.main_window.terminal.addItem("")
            for line in proc.stdout:
                self.main_window.terminal.clear()
                self.main_window.terminal.addItem(line.rstrip())
                print(line.rstrip())
            self.main_window.terminal.addItem(f"Done")
            self.main_window.run_button.setEnabled(True)
            self.main_window.select_file_button.setEnabled(True)
            self.main_window.ffplay_run.setEnabled(True)