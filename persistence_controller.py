import configparser

config = configparser.ConfigParser()
config.read("config.ini")

print(config["Directories"]["output_folder"])
print(config["Directories"]["ffmpeg_folder"])
