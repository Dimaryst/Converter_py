#include <iostream>
#include <string> 
#include <fstream> 
#include <stdio.h> 
#include <direct.h>
#include <cstdlib>
#include <cstring>
#include <direct.h>
using namespace std; 

void Replace(char str[], char a[], char b[], char buffer[])
{
    int i, j, pos = 0;
    for(i = 0; str[i]; i++)
    {
        for(j = 0; str[i + j] && a[j]; j++)   
            if(str[i + j] != a[j]) break;
        if(!a[j]) 
        {
            i+=j-1; 
            for(j=0;b[j];j++) buffer[pos++]=b[j]; 
        }
        else
        {
            buffer[pos++]=str[i];   
        }
        buffer[pos]=NULL;  
    }
    strcpy(str, buffer);  
}

int main()
{  
//config upload

	string conf_buffer; 
	ifstream file("settings.conf");  
	int index = 0;
	string config_strings[20];
    
	while(getline(file, conf_buffer)) {
       config_strings[index] = conf_buffer;
       index++;
	   }
    
file.close();
//3th string - ffmpeg directory
//6th string - key
  
	char current_work_dir[FILENAME_MAX];	//current directory
	_getcwd(current_work_dir, sizeof(current_work_dir));	//why not?)
	
//	cout << current_work_dir <<endl;
	cout << "FFmpeg bat-file creation tool" << endl;
	cout << "Enter your videofile name (without extention)" << endl;
	cout << ">> ";
	char videofile_name[1024];
	cin >> videofile_name;
	cout << endl;
	mkdir("\\temp");
	int codec_index = -1;
	while ((codec_index < 0) || (codec_index > 1)) 
	{
	cout << "Choose your videofile codec: " << endl << "(0) - H.264" << endl << "(1) - H.265 / HEVC" <<endl;
	cin >> codec_index;
	
	if ((codec_index < 0) || (codec_index > 1)) cout << "Incorrect codec parameters" << endl;
	}
	cout << endl;
	char h264_command[1024]; //h264 codec command
	strcpy(h264_command, config_strings[9].c_str());
	
	char replace_star[32] = "*", buffer1[1024], buffer2[1024];
	char replace_symbol[32] = "#", buffer3[1024], buffer4[1024];
	Replace(h264_command, replace_star, videofile_name, buffer1);
	Replace(h264_command, replace_symbol, videofile_name, buffer3);
	
	cout << h264_command << endl;
	//cout << current_work_dir << endl;
	
	
	
	
	
	
	
	char hevc_command[1024]; //hevc codec command
	strcpy(hevc_command, config_strings[12].c_str());
	Replace(hevc_command, replace_star, videofile_name, buffer2);
	Replace(hevc_command, replace_symbol, videofile_name, buffer4);
	
	
	
	
	
	cout << hevc_command << endl;
	
	char bat_file_dir[256];
	strcpy(bat_file_dir, current_work_dir);
	strcat(bat_file_dir, "/command.bat");
	
	ofstream bat_enc(bat_file_dir);
	if (bat_enc.is_open())
    {	
    	bat_enc << "cd ";
    	bat_enc << current_work_dir << endl;
    	bat_enc << "mkdir " << current_work_dir << "\\output_folder\\" << videofile_name << endl; 
    	if (codec_index == 0) bat_enc << h264_command << endl;
    	if (codec_index == 1) bat_enc << hevc_command << endl;
    }
	bat_enc.close();
	
	char key_file_dir1[256];
	strcpy(key_file_dir1, current_work_dir);
	strcat(key_file_dir1, "/input_folder/");
	strcat(key_file_dir1, videofile_name);
	strcat(key_file_dir1, ".key");
	
	char key_file_dir2[512];
	strcpy(key_file_dir2, current_work_dir);
	strcat(key_file_dir2, "\\output_folder\\");
	strcat(key_file_dir2, videofile_name);
	strcat(key_file_dir2, "\\");
	strcat(key_file_dir2, videofile_name);
	strcat(key_file_dir2, ".key");
	
	cout<<endl<<key_file_dir2<<endl;
	
	ofstream key1_enc(key_file_dir1);
	if (key1_enc.is_open())
    {	
		key1_enc << config_strings[6];
    }
	key1_enc.close(); 
	

	
	char keyinfo_dir[256];
	strcpy(keyinfo_dir, current_work_dir);
	strcat(keyinfo_dir, "/file.keyinfo");
	
	
	ofstream keyinfo_enc(keyinfo_dir);
	if (keyinfo_enc.is_open())
    {	
		keyinfo_enc << videofile_name;
		keyinfo_enc << ".key" << endl;
		keyinfo_enc << key_file_dir1;
		
    }
	keyinfo_enc.close(); 
	
	system("command.bat");
	
	ofstream key2_enc(key_file_dir2);
	if (key2_enc.is_open())
    {	
		key2_enc << config_strings[6];
    }
	key2_enc.close(); 
	
	system("pause");
	
    return 0;
}
