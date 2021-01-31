import os
import subprocess
import sys
import time
import qdarkstyle

from PyQt5 import QtWidgets
from PyQt5.QtCore import QFileInfo, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

from assets.Converter import Ui_ffmpegConverterMain


class MainConverter(QtWidgets.QMainWindow, Ui_ffmpegConverterMain):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.video_name = None
        self.labelStatus.setText("Status: Waiting...")
        self.pushButtonConvert.setDisabled(True)
        self.thread = ConvThread(self, None)
        self.lineEditKey.setText("ffdsffdsffdsffds")  # Example
        self.pushButtonAdd.clicked.connect(self.browse_video)
        self.pushButtonConvert.clicked.connect(self.convert)
        self.actionFfplay.triggered.connect(self.play)
        self.actionInfo.triggered.connect(self.show_help)
        self.lineEditPath.setReadOnly(True)


    def browse_video(self):
        path_request = QtWidgets.QFileDialog
        options = QtWidgets.QFileDialog.Options()
        video_path, _ = path_request.getOpenFileName(self, "Select the video...", "",
                                                     "Video File (*.mp4 *.avi)",
                                                     options=options)

        self.video_name = QFileInfo(video_path).fileName()
        if video_path:
            self.lineEditPath.setText(str(video_path))
            self.pushButtonConvert.setEnabled(True)

    def convert(self):
        print(self.lineEditPath.text())
        if not os.path.exists(self.lineEditPath.text()):
            print("ERROR: Video not selected")
            self.labelStatus.setText("Video not found")
        else:
            DirName = (self.video_name + f"{time.ctime()}").replace(" ", "_").replace(".", "").replace(":", "")

            os.mkdir(DirName)
            keyfile = open(f"{DirName}/file.key", "w")
            keyfile.write(self.lineEditKey.text())
            keyfile.close()

            key_info_file = open("file.keyinfo", "w")
            key_info_file.truncate()
            key_info_file.write(f"file.key\n{os.path.abspath(DirName)}/file.key")
            key_info_file.close()

            cmd264 = ("ffmpeg", "-i", self.lineEditPath.text(),
                      "-c", "copy", "-bsf:v", "h264_mp4toannexb",
                      "-hls_time", "10", "-hls_key_info_file",
                      "file.keyinfo", "-hls_list_size", "0", f"{DirName}/out.m3u8")

            cmdhevc = ("ffmpeg", "-i", self.lineEditPath.text(),
                       "-c", "copy", "-bsf:v", "hevc_mp4toannexb",
                       "-hls_time", "10", "-hls_key_info_file",
                       "file.keyinfo", "-hls_list_size", "0", f"{DirName}/out.m3u8")

            self.thread.commands = [cmd264, cmdhevc]
            self.thread.start()

    def play(self):
        path_request = QtWidgets.QFileDialog
        options = QtWidgets.QFileDialog.Options()
        video_path, _ = path_request.getOpenFileName(self, "Select the playlist...", "",
                                                     "File (*.m3u8)",
                                                     options=options)

        if video_path and os.path.exists(video_path):
            # ffplay -allowed_extensions ALL out.m3u8
            cmdplay = ("ffplay", "-allowed_extensions", "ALL", video_path)
            self.thread.commands = [cmdplay]
            self.thread.start()

    @staticmethod
    def show_help():
        help_message = QMessageBox()
        help_message.setIcon(QMessageBox.Information)
        help_message.setText("Instruction")
        help_message.setInformativeText("This small utility is made to convert to M3U8 with a given key.\n"
                                        "First you need to make sure that FFMpeg is installed.\n\n"
                                        "FFmpeg installation:\n"
                                        "\n1. In terminal: \"/bin/bash -c "
                                        "$(curl -fsSL "
                                        "https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
                                        "\n2. Then in terminal: \"brew install ffmpeg\"")
        help_message.setWindowTitle("Info")
        help_message.setStandardButtons(QMessageBox.Ok)
        help_message.exec_()


class ConvThread(QThread):
    def __init__(self, main_window, commands=None):
        super().__init__()
        if commands is None:
            commands = [("echo", "Empty")]
            self.main_window = main_window
            self.commands = commands

    def run(self):
        for command in self.commands:
            self.main_window.setDisabled(True)
            proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, universal_newlines=True, bufsize=2)
            self.main_window.labelStatus.setText("Status: Running...")

            for line in proc.stdout:
                print(line)

            self.main_window.setEnabled(True)
            self.main_window.labelStatus.setText("Status: Done")
        self.quit()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon('assets/logo.png'))
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = MainConverter()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
