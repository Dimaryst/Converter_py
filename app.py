import os
import subprocess
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread
import UIToolsC


class SecondProcess(QThread):
    def __init__(self, main_window, commands=None):
        super().__init__()
        if commands is None:
            commands = ["echo Command not found"]
        self.main_window = main_window
        self.commands = commands

    def run(self):
        self.main_window.terminal.addItem("Thread running...")
        self.main_window.terminal.addItem(str(self.commands))
        index = 0
        exit_codes = []
        for command in self.commands:
            self.main_window.terminal.addItem(f"({index}) Trying: {command}")
            proc = subprocess.Popen(command, stdout=subprocess.PIPE)
            counter = 0
            while proc.poll() is None:
                counter += 1
            self.main_window.terminal.addItem(f"Done ({counter})")

            # self.main_window.terminal.addItem(f"{outs}")
            # while proc.poll() is None:
            #     output_line = proc.stdout.read(1)
            #     self.main_window.terminal.addItem(output_line)

            # self.main_window.terminal.addItem(f"Process ({index})"
            #                                   f"exited with code: "
            #                                   f"{exit_codes[index]}")
            self.main_window.terminal.scrollToBottom()
            index += 1

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


class ToolsAppMain(QtWidgets.QMainWindow, UIToolsC.UiMainWindow):
    def __init__(self):
        # переменные
        self.originVideofilePath = None
        self.ffmpeg_path = "ffmpeg\\bin"
        self.work_dir = os.getcwd()

        # инициализация
        super().__init__()
        self.setupUi(self)
        self.command_selector.addItem("Информация о файле")
        self.command_selector.addItem("Конвертирование")
        self.command_selector.addItem("Изменение битрейта")
        self.run_button.setDisabled(True)
        self.toolButton.setDisabled(True)
        self.command_selector.setDisabled(True)
        self.terminal.addItem("Ready...")
        self.second_process = SecondProcess(main_window=self, commands=[])

        # обработчик действий
        self.select_file_button.clicked.connect(self.browse_videofile)
        self.run_button.clicked.connect(self.start_get_info)
        self.help_info.triggered.connect(self.help_window)

    @staticmethod
    def help_window():  # TODO: Enter info
        help_message = QMessageBox()
        help_message.setIcon(QMessageBox.Information)
        help_message.setText("Инструкция по работе с конвертером")
        help_message.setInformativeText("1. Выбрать видео закодированное в H264 или H265. \n"
                                        "2. Нажать кнопку \"Конвертировать\".\n"
                                        "3. Дождаться завершения процесса. Папка с конвертированным контентом будет"
                                        " помещена в корневую директорию.\n")
        help_message.setWindowTitle("Справка")
        help_message.setStandardButtons(QMessageBox.Ok)

        help_message.exec_()

    def browse_videofile(self):
        path_request = QtWidgets.QFileDialog
        options = QtWidgets.QFileDialog.Options()
        # options |= QtWidgets.QFileDialog.

        # выбор видеофайла
        self.originVideofilePath, _ = path_request.getOpenFileName(self, "Укажите путь к видеофайлу...", "",
                                                                   "Video File (*.mp4 *.avi)",
                                                                   options=options)

        if self.originVideofilePath:  # не продолжать выполнение, если пользователь не выбрал видеофайл
            self.terminal.addItem("Selected video: " + self.originVideofilePath)
            self.run_button.setEnabled(True)
            self.toolButton.setEnabled(True)
            self.command_selector.setEnabled(True)

    def browse_workdirectory(self):
        self.work_dir = None
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.work_dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите новую рабочую директорию (в ней "
                                                                         "будут создаваться папки с "
                                                                         "конвертированным видео)")
        print(self.work_dir)

    def start_get_info(self):
        if self.originVideofilePath is None:
            self.terminal.addItem("ERROR: Videofile path incorrect.")
            self.terminal.addItem("Reselect videofile.")
        else:
            command1 = self.ffmpeg_path + \
                       "\\ffmpeg.exe -i \"" + self.originVideofilePath + "\""
            command2 = "ffmpeg -i \"" + self.originVideofilePath + "\""
            self.terminal.addItem(command1)
            self.terminal.addItem(command2)
            self.second_process.commands = [command1, command2]
            print(self.second_process.commands)
            self.second_process.start()

    def start_conversion(self):
        if self.originVideofilePath is None:
            self.terminal.addItem("ERROR: Videofile path incorrect.")
            self.terminal.addItem("Reselect videofile.")
        else:
            full_path = self.originVideofilePath  # /path/to/file.mp4
            full_name = os.path.basename(self.originVideofilePath)  # полное имя файла file.mp4
            name = os.path.splitext(full_name)[0]  # имя без расширения file
            # new_folder_name = name.replace(" ", "_")
            # path = full_path.replace(full_name, new_folder_name)
            try:
                # Создание новой output папки
                os.mkdir(self.work_dir + "\\" + name.replace(" ", "_"))

                # Создание файла key
                key_file_path = self.work_dir + "\\" + name.replace(" ", "_") + "\\" + "file.key"
                key_file = open(key_file_path, "w")
                # key_file.truncate()
                key_file.write("KEY")
                key_file.close()

                # Создание файла keyinfo
                keyinfo_file_path = self.work_dir + "\\file.keyinfo"
                keyinfo_file = open(keyinfo_file_path, 'w')
                keyinfo_file.write("file.key\n" + key_file_path)
                keyinfo_file.close()

                # Рабочие комманды для запуска стороннего процесса
                self.cmd_h264 = "ffmpeg/bin/ffmpeg.exe -i \"" + full_path + "\" -c copy -bsf:v h264_mp4toannexb -hls_time 10 " + \
                                "-hls_key_info_file \"" + keyinfo_file_path + "\" " + "-hls_list_size 0 " + \
                                name.replace(" ", "_") + "\\" + name.replace(" ", "_") + ".m3u8"

                self.cmd_hevc = "ffmpeg/bin/ffmpeg.exe -i \"" + full_path + "\" -c copy -bsf:v hevc_mp4toannexb -hls_time 10 " + \
                                "-hls_key_info_file \"" + keyinfo_file_path + "\" " + "-hls_list_size 0 " + \
                                name.replace(" ", "_") + "\\" + name.replace(" ", "_") + ".m3u8"

                self.listWidget.addItem(self.cmd_hevc)
                self.listWidget.addItem(self.cmd_h264)
                self.listWidget.addItem("...")

            except OSError:
                self.listWidget.scrollToBottom()
                self.listWidget.addItem("Command error. Video file not selected.")

            else:
                self.listWidget.addItem(f"Command ready.")
                self.External_command_thread.command_h264 = self.cmd_h264
                self.External_command_thread.command_hevc = self.cmd_hevc
                self.h264Button.setEnabled(False)
                self.FileSelectButton.setEnabled(False)
                self.launch_command()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ToolsAppMain()  # Создаём объект
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
