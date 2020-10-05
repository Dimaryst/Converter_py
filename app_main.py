import os
import subprocess
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread
import ConverterDesign

KEY = "ffdsffdsffdsffds"


class FFmpegThread(QThread):
    def __init__(self, main_window, command_h264, command_hevc):
        super().__init__()
        self.main_window = main_window
        self.command_h264 = command_h264
        self.command_hevc = command_hevc

    def run(self):
        self.main_window.listWidget.addItem("Running conversion... Please wait...")

        try_h264 = subprocess.Popen(self.command_h264)
        exit_code_h264 = try_h264.wait()
        try_hevc = subprocess.Popen(self.command_hevc)
        exit_code_hevc = try_hevc.wait()
        self.main_window.h264Button.setEnabled(True)
        self.main_window.FileSelectButton.setEnabled(True)
        if exit_code_hevc == exit_code_h264:
            self.main_window.listWidget.addItem("FFmpeg command error. Check FFmpeg installation or videofile codec.")
        else:
            self.main_window.listWidget.addItem("Conversion was successful.")


class AppConverter(QtWidgets.QMainWindow, ConverterDesign.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации UI
        self.file_dir = None
        self.work_dir = os.getcwd()
        self.cmd_h264 = None
        self.cmd_hevc = None
        self.External_command_thread = FFmpegThread(main_window=self, command_h264=self.cmd_h264,
                                                    command_hevc=self.cmd_hevc)

        # обработчик действий
        self.FileSelectButton.clicked.connect(self.browse_videofile)  # Выполнить функцию browse_videofile
        self.action_2.triggered.connect(self.browse_workdir)  # выполнить browse_workdir
        self.h264Button.clicked.connect(self.start_conversion_h264)
        self.action_3.triggered.connect(self.help_window)

    @staticmethod
    def help_window():
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
        self.file_dir = None
        # добавление опций для выбора видеофайла
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        # выбор видеофайла для последующего конвертирования в m3u8
        self.file_dir, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Укажите путь к видеофайлу", "",
                                                                 "Video File (*.mp4)",
                                                                 options=options)

        # print(self.file_dir)
        if self.file_dir:  # не продолжать выполнение, если пользователь не выбрал видеофайл
            self.listWidget.addItem("Videofile selected: " + self.file_dir)

    def browse_workdir(self):
        self.work_dir = None
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.work_dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите новую рабочую директорию (в ней "
                                                                         "будут создаваться папки с "
                                                                         "конвертированным видео)")
        print(self.work_dir)

    def start_conversion_h264(self):
        if self.file_dir is None:
            # QMessageBox.about(self, "Исходный видеофайл не выбран.", "Укажите путь к видеофайлу.")
            self.listWidget.addItem("Check videofile selection.")

        else:
            full_path = self.file_dir  # /path/to/file.mp4
            full_name = os.path.basename(self.file_dir)  # полное имя файла file.mp4
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
                key_file.write(KEY)
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

    def launch_command(self):
        self.External_command_thread.start()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = AppConverter()  # Создаём объект
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
