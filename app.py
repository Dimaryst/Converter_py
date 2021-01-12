import os
import sys
import configparser as confp
import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

from modules import background_process as bp, UIToolsC, UISettingsCommand


class ToolsAppMain(QtWidgets.QMainWindow, UIToolsC.UiMainWindow):
    def __init__(self):
        # переменные
        self.originVideofilePath = None
        self.originVideofilename = None
        self.settingsWindow = None

        self.ffmpeg_path = "ffmpeg/bin"
        self.keyfile_path = "file.key"
        self.keyinfofile_path = "file.keyinfo"

        self.m3u8key = "mysecurekey"
        self.video_bitrate = 5000

        self.printCommandInTerminal = False
        self.printBanner = False

        # инициализация
        super().__init__()
        self.setupUi(self)
        self.load_config()
        self.command_selector.addItem("Конвертирование в M3U8")
        self.command_selector.addItem("Изменение битрейта видео")
        self.run_button.setDisabled(True)
        self.toolButton.setDisabled(True)
        self.command_selector.setDisabled(True)
        self.terminal.addItem("Ready...")
        self.second_process = bp.BackgroundProcess(main_window=self, commands=[])

        # обработчик действий
        self.select_file_button.clicked.connect(self.browse_videofile)
        self.ffplay_run.triggered.connect(self.run_ffplay)
        self.help_info.triggered.connect(self.help_window)
        self.run_button.clicked.connect(self.run_command)
        self.toolButton.clicked.connect(self.commands_settings)

    def load_config(self):
        config = confp.ConfigParser()
        config.read('config.ini')
        self.keyfile_path = config["Directories"]["m3u8keyfile"]
        self.keyinfofile_path = config["Directories"]["m3u8keyinfofile"]
        self.m3u8key = str(config["Variables"]["m3u8key"])
        self.video_bitrate = int(config["Variables"]["video_bitrate"])
        self.printCommandInTerminal = bool(config["Options"]["PrintCommandInTerminal"])
        self.printBanner = bool(config["Options"]["PrintBanner"])

    def run_ffplay(self):
        self.run_button.setEnabled(False)
        self.toolButton.setEnabled(False)
        self.command_selector.setEnabled(False)

        path_request = QtWidgets.QFileDialog
        options = QtWidgets.QFileDialog.Options()
        m3u8_playlist, _ = path_request.getOpenFileName(self, "Укажите путь к видео или плейлисту...", "",
                                                        "Video File (*.m3u8 *.mp4 *.avi)",
                                                        options=options)

        ffplay_command = self.ffmpeg_path + "/ffplay.exe -allowed_extensions ALL \"" + m3u8_playlist + "\""
        print(ffplay_command)
        self.second_process.commands = [ffplay_command]
        self.second_process.start()

    def run_command(self):
        print(self.command_selector.currentIndex())
        if self.originVideofilePath is not None:
            if self.command_selector.currentIndex() == 0:
                self.conversion()
            elif self.command_selector.currentIndex() == 1:
                self.change_bitrate()
            else:
                self.terminal.addItem("Command not found")
        else:
            self.terminal.addItem("Video not found")

    def commands_settings(self):
        if not self.settingsWindow:
            self.settingsWindow = Settings(self)
        self.settingsWindow.show()

    @staticmethod
    def help_window():  # TODO: Enter info
        help_message = QMessageBox()
        help_message.setIcon(QMessageBox.Information)
        help_message.setText("Как использовать?")
        help_message.setInformativeText("Этот приложение генерирует и запускает команды FFmpeg для различных "
                                        "манипуляций с видео.\n\nВыберите исходное видео, функцию, а затем запустите "
                                        "процесс. Все данные будут выводиться в консоль в основном окне.\n"
                                        "Используйте функцию ffplay для воспроизведения видео.")
        help_message.setWindowTitle("Справка")
        help_message.setStandardButtons(QMessageBox.Ok)
        help_message.exec_()

    def browse_videofile(self):

        self.run_button.setEnabled(False)
        self.toolButton.setEnabled(False)
        self.command_selector.setEnabled(False)

        path_request = QtWidgets.QFileDialog
        options = QtWidgets.QFileDialog.Options()
        self.originVideofilePath, _ = path_request.getOpenFileName(self, "Укажите путь к видеофайлу...", "",
                                                                   "Video File (*.mp4 *.avi)",
                                                                   options=options)
        self.originVideofilename = QFileInfo(self.originVideofilePath).fileName()
        print(self.originVideofilename)
        if self.originVideofilePath:
            self.terminal.addItem("Selected video: " + self.originVideofilePath)
            self.run_button.setEnabled(True)
            self.toolButton.setEnabled(True)
            self.command_selector.setEnabled(True)

    def change_bitrate(self):
        if self.originVideofilePath is None:
            self.terminal.addItem("ERROR: Videofile path incorrect.")
            self.terminal.addItem("Reselect videofile.")
        else:
            outfname = (((self.originVideofilename.split(".")[0] +
                          str(datetime.datetime.now())).replace(" ", "")).replace(".", "")).replace(":", "-") + \
                       ".mp4"
            command = self.ffmpeg_path + "/ffmpeg.exe -i \"" + \
                      self.originVideofilePath + \
                      f"\" -hide_banner -c:v libx264 -b:v {self.video_bitrate}K " \
                      f"{outfname}"
            print(command)
            self.second_process.commands = [command]
            self.second_process.start()

    def conversion(self):
        if self.originVideofilePath is None:
            self.terminal.addItem("ERROR: Videofile path incorrect.")
            self.terminal.addItem("Reselect videofile.")
        else:
            uniqueDirName = (((self.originVideofilename.split(".")[0] +
                          str(datetime.datetime.now())).replace(" ", "")).replace(".", "")).replace(":", "-")
            os.mkdir(uniqueDirName)
            kfile = open(f"{uniqueDirName}/file.key", "w")
            kfile.write(self.m3u8key)
            kfile.close()

            kinffile = open("file.keyinfo", "w")
            kinffile.truncate()
            kinffile.write(f"file.key\n{os.path.abspath(uniqueDirName)}\\file.key")
            kinffile.close()

            commandH264 = self.ffmpeg_path + "/ffmpeg.exe -i \"" + \
                          self.originVideofilePath + \
                          f"\" -c copy -bsf:v h264_mp4toannexb -hls_time 10 " \
                          f"-hls_key_info_file file.keyinfo " \
                          f"-hls_list_size 0 {uniqueDirName}/out.m3u8"
            self.second_process.commands = [commandH264]
            self.second_process.start()


class Settings(QtWidgets.QWidget, UISettingsCommand.Ui_SettingsWindow):
    def __init__(self, parent=ToolsAppMain):
        super(Settings, self).__init__(parent, QtCore.Qt.Window)
        self.setupUi(self)
        self.config = confp.ConfigParser()
        self.config.read('config.ini')
        self.ffmpeg_path = self.config["Directories"]["ffmpeg_folder"]
        self.keyfile_path = self.config["Directories"]["m3u8keyfile"]
        self.keyinfofile_path = self.config["Directories"]["m3u8keyinfofile"]

        self.m3u8key = str(self.config["Variables"]["m3u8key"])
        self.KeyEdit.setText(self.m3u8key)

        self.video_bitrate = int(self.config["Variables"]["video_bitrate"])
        self.bitrate_settings.setValue(self.video_bitrate)
        self.banner_settings.setDisabled(True)
        self.terminal_output.setDisabled(True)
        self.OkButton.clicked.connect(self.OkAction)
        self.CancelButton.clicked.connect(self.CancelAction)

    def OkAction(self):
        self.WriteChanges()
        self.parent().load_config()
        self.hide()

    def CancelAction(self):
        self.hide()

    def WriteChanges(self):
        if self.KeyEdit.text() != "":
            self.m3u8key = self.KeyEdit.text()
            self.config["Variables"]["m3u8key"] = self.KeyEdit.text()
        else:
            self.config["Variables"]["m3u8key"] = "defaultkey"

        self.video_bitrate = str(self.bitrate_settings.value())
        self.config["Variables"]["video_bitrate"] = self.video_bitrate

        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)


def main():
    print(datetime.datetime.now())
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    # app.setStyle('Fusion')
    app.setWindowIcon(QIcon('assets/logo.png'))
    window = ToolsAppMain()  # Создаём объект
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
