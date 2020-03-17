#include <iostream>
#include <fstream>
#include <cstdlib>
#include <string>
#include <cstring>
using namespace std;
int main(int argc, char** argv) 
{	
	char key[] = ""; // the key is stored in the source code, but is written as a file with the .key extension
	char folder_link[] = "C://ffscript/";
	char key_info_ext[] = ".keyinfo";
	char key_ext[] = ".key";
	char script_ext[] = ".bat";
	char ffmpeg_dir[] = "C://ffmpeg/bin";
	printf("Your files in C:/ffscript/ directory will be overwriten\n");
		
	system("pause");
	
	char string_name[32]; // video file name without extension
	cout << "Enter your input file name (mp4) : " << endl;
	cin >> string_name;
	
		// create a file with a key 

	
	char key_link[] = "";
	strcat(key_link, folder_link); 
	strcat(key_link, string_name); 
	strcat(key_link, key_ext);
	
	ofstream key_file(key_link); 
	if (key_file.is_open())
    {
        key_file << key << endl;
    }
	key_file.close(); 
	   
		// create a file with key information (all files should be stored in one folder)
	
	char key_info_link[] = "";
	strcat(key_info_link, folder_link);
	strcat(key_info_link, "file.keyinfo");
	
	
	ofstream key_info_stream(key_info_link); 
	if (key_info_stream.is_open())
    {
        key_info_stream << string_name << key_ext << endl;
        key_info_stream << folder_link << string_name << key_ext << endl;
    }
	key_info_stream.close(); 
	
	// generate bat
	// If the movie codec is H265 (HEVC), the command should look like this:
	//ffmpeg -i input.mp4 -c copy -bsf:v hevc_mp4toannexb -hls_time 10 -hls_key_info_file file.keyinfo -hls_list_size 0 input.m3u8	
	//
	// If the movie codec is H264, the command should look like this:
	//ffmpeg -i input.mp4 -c copy -bsf:v h264_mp4toannexb -hls_time 10 -hls_key_info_file file.keyinfo -hls_list_size 0 input.m3u8
	char ffmpeg_command[] = "ffmpeg.exe  -i ";
	char ffmpeg_h265[] = " -c copy -bsf:v hevc_mp4toannexb -hls_time 10 -hls_key_info_file file.keyinfo -hls_list_size 0 ";
	char ffmpeg_h264[] = " -c copy -bsf:v h264_mp4toannexb -hls_time 10 -hls_key_info_file file.keyinfo -hls_list_size 0 ";
	char full_command_h264_encrypt[] = "";
	char videofile_ext[] = ".mp4";
	
	// the command line
	
	strcat(full_command_h264_encrypt, ffmpeg_command); 
	strcat(full_command_h264_encrypt, string_name);  
	strcat(full_command_h264_encrypt, videofile_ext);  
	strcat(full_command_h264_encrypt, ffmpeg_h264); 
	strcat(full_command_h264_encrypt, "output.m3u8");
//	cout << endl;
//	printf(full_command_h264_encrypt);
//	cout << endl;
	
	ofstream bat_enc("C://ffscript/script_encrypt.bat");
	if (bat_enc.is_open())
    {	
    	bat_enc << "cd C:/ffmpeg/bin" << endl;
        bat_enc << full_command_h264_encrypt << endl;
    }
	bat_enc.close(); 
	return 0;
}
