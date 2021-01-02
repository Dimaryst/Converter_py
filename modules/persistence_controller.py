import configparser

config = configparser.ConfigParser()
config.read("config.ini")

ffmpeg_path = config["Directories"]["ffmpeg_folder"]
keyfile_path = config["Directories"]["m3u8keyfile"]
