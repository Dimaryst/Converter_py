encrypter_v2_ffmpeg

This utility is used to fasten the process of encryption (cutting an mp4 videofile into m3u8 + multiple ts format)
by script generation, accessing the ffmpeg-utility. 

How to Use:
1. First of all, download FFmpeg from their official website and add it to PATH's environment variables list
https://ffmpeg.zeranoe.com/builds/ - FFmpeg project's website;
https://www.wikihow.com/Install-FFmpeg-on-Windows - Installation instruction;
2. Next, download this repository and unzip it into convenient directory. 
3. Then, create input_folder and output_folder in project directory (the folders must be named like this only).
4. Open settings.conf by text editor (notepad or smth) and rewrite the encription key field with your key.
5. Then, place the videofile that has to be encrypted (H.264 or HEVC codec only) into input_folder. 
6. Start encrypter_v2_ffmpeg.exe and enter full videofile name without extention, 
then choose the codec.
7. After that the encryption process starts automatically. Ready m3u8, ts files and the key file will be placed in output_folder.

The setup might seem a little complicated. But, if you need to encrypt an enormous amount of video or you're going to do it regulary, this script can save you a lot of time and simplify interacting with ffmpeg framework.
