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

        # self.main_window.terminal.addItem(f"{outs}")
        # while proc.poll() is None:
        #     output_line = proc.stdout.read(1)
        #     self.main_window.terminal.addItem(output_line)

        # self.main_window.terminal.addItem(f"Process ({index})"
        #                                   f"exited with code: "
        #                                   f"{exit_codes[index]}")

        # try_h264 = subprocess.Popen(self.command_h264)
        # exit_code_h264 = try_h264.wait()
        # try_hevc = subprocess.Popen(self.command_hevc)
        # exit_code_hevc = try_hevc.wait()
        # self.main_window.h264Button.setEnabled(True)
        # self.main_window.FileSelectButton.setEnabled(True)
        # if exit_code_hevc == exit_code_h264:
        #     self.main_window.listWidget.addItem("FFmpeg command error. Check FFmpeg installation or videofile codec.")
        # else:
        #     self.main_window.listWidget.addItem("Conversion was successful.")
