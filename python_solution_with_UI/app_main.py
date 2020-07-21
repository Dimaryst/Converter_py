import sys
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import subprocess

import ConverterDesign

KEY = "aadsaadsaadsaads"


class AppConverter(QtWidgets.QMainWindow, ConverterDesign.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.index = 0
        self.file_dir = None
        self.work_dir = os.getcwd()
        # обработчик действий
        self.FileSelectButton.clicked.connect(self.browse_videofile)  # Выполнить функцию browse_videofile
        self.action_2.triggered.connect(self.browse_workdir)  # выполнить browse_workdir
        self.h264Button.clicked.connect(self.start_conversion_h264)

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
            self.listWidget.addItem(self.file_dir)

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
            QMessageBox.about(self, "Ошибка", "Укажите путь к видеофайлу")
        else:
            full_path = self.file_dir  # /path/to/file.mp4
            full_name = os.path.basename(self.file_dir)  # полное имя файла file.mp4
            name = os.path.splitext(full_name)[0]  # имя без расширения file
            new_folder_name = name.replace(" ", "_")
            path = full_path.replace(full_name, new_folder_name)
            try:
                # Создание новой output папки
                os.mkdir(self.work_dir + "/" + name.replace(" ", "_"))

                # Создание файла key
                key_file_path = self.work_dir + "/" + name.replace(" ", "_") + "/" + name.replace(" ", "_") + ".key"
                key_file = open(key_file_path, "w")
                key_file.truncate()
                key_file.write(KEY)

                # Создание файла keyinfo
                keyinfo_file_path = self.work_dir + "/file.keyinfo"
                keyinfo_file = open(keyinfo_file_path, 'w')
                keyinfo_file.truncate()
                keyinfo_file.write(name.replace(" ", "_") + ".key\n" + key_file_path)

                # Запуск
                batfile = open('scrpt.bat', 'w')
                batfile.truncate()
                batfile.write("ffmpeg -i \"" + full_path + "\" -c copy -bsf:v h264_mp4toannexb -hls_time 10 "
                                                           "-hls_key_info_file \"" + keyinfo_file_path + "\" "
                                                           "-hls_list_size 0 " +
                              name.replace(" ", "_") + "/" + name.replace(" ", "_") +
                              ".m3u8")

                batfile.write("\nffmpeg -i \"" + full_path + "\" -c copy -bsf:v hevc_mp4toannexb -hls_time 10 "
                                                             "-hls_key_info_file \"" + keyinfo_file_path + "\" "
                                                             "-hls_list_size 0 " +
                              name.replace(" ", "_") + "/" + name.replace(" ", "_") +
                              ".m3u8")

            except OSError:
                print("Error: %s" % path)
            else:
                print("Success %s " % path)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = AppConverter()  # Создаём объект
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
