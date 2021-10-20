// JUST FOR THIS TASK, HAS DIFFERENT PREFERENCES AND IS NOT
// USER FRIENDLY AS WELL AS DIFFERENT FILE ORIENTATION
#include <bits/stdc++.h>

using namespace std;


typedef vector<string> vs;
typedef pair<string, string> pss;
typedef vector<pss> vps;


#define EB emplace_back
#define MP make_pair
#define F first
#define S second


// functions:
int getSecondsFromStr(string time);
string convertSecondsToStr(int seconds);
string getDurationCommand(string start, string time_end);
string getAndRemoveFileExtension(string &file_name);
void replaceAllSubstrings(string &str, const string &from, const string &into);
void displayInputInstructions();



int main()
{
    printf("Trimmer started\n\n");

    //printf("Do You want the file to be processed without transcoding (y/n): ");
    char do_not_transcode = 'y';
    //cin >> do_not_transcode;
    string transcoding_cmd = "-acodec copy ";  // by default it will not transcode
    if (do_not_transcode == 'n') {
        transcoding_cmd = "-c copy ";
    }

    //displayInputInstructions();
    //system("pause");

    freopen("_video_trimming_data.txt", "r", stdin);

    string file_name = "./";  // CAN NOT GET IT TO WORK WITH PATH OUTSIDE CWD

    // get the data for video trimming:
    while (getline(cin, file_name)) {  // keep going as long as there is new file trimming data
        printf("\nNew Iteration starts\n");
        // Make the file name appropriate for ffmpeg:
        string old_file_name;
        old_file_name.assign(file_name);
        string file_extension = getAndRemoveFileExtension(file_name);

        replaceAllSubstrings(file_name, ".", "_");
        replaceAllSubstrings(file_name, "-", "_");
        replaceAllSubstrings(file_name, " ", "_");
        replaceAllSubstrings(file_name, "(", "_");
        replaceAllSubstrings(file_name, ")", "_");
        replaceAllSubstrings(file_name, "[", "_");
        replaceAllSubstrings(file_name, "]", "_");
        replaceAllSubstrings(file_name, ",", "_");


        string new_file_name = string(file_name) + file_extension;
        stringstream renaming_cmd_ss;
        renaming_cmd_ss << "rename \"" << old_file_name << "\" " << new_file_name;
        string renaming_cmd = renaming_cmd_ss.str();

        printf("\nVideo file had to be renamed from:\n\n%s\n\n\tto\n\n%s\n\n", old_file_name.c_str(), new_file_name.c_str());
        printf("Command: %s\n", renaming_cmd.c_str());
        system(renaming_cmd.c_str());

        // input time segements
        int num_of_segments = 0;

        vps time_intervals;
        string cur_start, cur_end;

        while (getline(cin, cur_start) && (cur_start.compare("end") != 0 && cur_start.compare("end\n") != 0)) {  // end marks the end of current file's trimming data
            getline(cin, cur_end);
            printf("File: ");  cout << new_file_name;
            printf("\nStart: ");  cout << cur_start;
            printf("\nEnd: ");  cout << cur_end << '\n';
            ++num_of_segments;
            time_intervals.EB(MP(convertSecondsToStr(stoi(cur_start)), getDurationCommand(cur_start, cur_end)));
        }

        printf("Dividing video into: %d segments\n", num_of_segments);


        // construct command line argument
        stringstream ffmpeg_cmd_ss;
        ffmpeg_cmd_ss << "ffmpeg -y -i " << new_file_name << " -ss ";
        string basic_ffmpeg_cmd = ffmpeg_cmd_ss.str();

        // save the names of each segment of the video
        vs output_file_names_of_tmp_vids;

        // Set the correct transcoding command
        const vs audio_extensions = {".mp3", ".m4a", ".wav", ".raw", "ogg", ".flac"};
        // if current file is not only audio then add command for transcoding video too
        if (do_not_transcode == 'y' && find(audio_extensions.begin(), audio_extensions.end(), file_extension) == audio_extensions.end()) {
            transcoding_cmd = "-acodec copy -vcodec copy ";
        }

        for (int i = 0; i < num_of_segments; ++i) {
            // construct output folder
            stringstream output_file_name_ss;
            if (num_of_segments > 1) {
                output_file_name_ss << file_name << "_part" << (i + 1) << file_extension;
            } else {  // it is the only segment so rename it to output instead of _part1
                output_file_name_ss << file_name << "_output" << file_extension;
            }
            string output_file_name = output_file_name_ss.str();
            output_file_names_of_tmp_vids.EB(output_file_name);

            // construct final command line argument
            stringstream cur_ffmpeg_cmd_ss;
            cur_ffmpeg_cmd_ss << basic_ffmpeg_cmd << time_intervals[i].F << time_intervals[i].S << transcoding_cmd << output_file_name;
            string ffmpeg_cmd = cur_ffmpeg_cmd_ss.str();

            cout << "\n\nPassing argument: " << ffmpeg_cmd << "\n\n";

            // execute command
            system(ffmpeg_cmd.c_str());
        }


        // merge the segment video copies:
        if (num_of_segments <= 1) {
            printf("Done.");
            // write the names of final output files:
            ofstream out_file;
            out_file.open("outputs.txt", ios_base::app);  // make sure to append, not overwrite

            out_file << new_file_name << '\n';  // name of the original
            out_file << output_file_names_of_tmp_vids[0] << '\n';

            out_file.close();
            return 0;
        }

        // firstly create a file with the file_names of the files
        // to concatanate
        ofstream outfile ("inputs.txt");  // creating file in the cwd of this program
        for (int i = 0; i < num_of_segments; ++i) {
            // at the beginning of each line it should have file and the file_name
            // should be enclosed in ''
            outfile << "file '" << output_file_names_of_tmp_vids[i] << "'\n";  // add file_name as a new line
        }
        outfile.close();  // done writing to the file

        stringstream ffmpeg_merge_ss;
        ffmpeg_merge_ss << "ffmpeg -f concat -i inputs.txt " << transcoding_cmd << file_name << "_output" << file_extension;
        string ffmpeg_merge_cmd = ffmpeg_merge_ss.str();

        system(ffmpeg_merge_cmd.c_str());

        //system("pause");  // exitting app now would keep the separate segments undeleted


        // delete all files which contained each segment of final video
        for (int i = 0; i < num_of_segments; ++i) {
            string delete_cmd = "del " + string(output_file_names_of_tmp_vids[i]);
            system(delete_cmd.c_str());
        }

        // write the names of final output files:
        ofstream out_file;
        out_file.open("outputs.txt", ios_base::app);  // make sure to append, not overwrite

        out_file << new_file_name << '\n';  // name of the original
        out_file << file_name << "_output" << file_extension << '\n';

        out_file.close();
    }  // end of while

    return 0;
}



// converts time from string format to seconds: e.g. 01:10:02 --> 4202
int getSecondsFromStr(string time) {
    int start_seconds = 0;
    for (int i = 0, cur_time_step = 3600, n = time.length(); i <= n - 2; i+=3) {
        int cur_interval = stoi(time.substr(i, 2));
        start_seconds += cur_interval * cur_time_step;
        cur_time_step /= 60;
    }
    return start_seconds;
}


// converts seconds to formatted string: e.g. 4202 --> 01:10:02
string convertSecondsToStr(int seconds) {
    string out = "00:00:00";
    for (int i = out.length() - 1; i >= 1 && seconds > 0; i-=3) {
        int cur_time = seconds % 60;
        if (cur_time < 10) {  // change one digit
            out[i] = '0' + cur_time;
        } else {
            out[i] = '0' + cur_time % 10;
            out[i - 1] = '0' + cur_time / 10;
        }
        seconds /= 60;
    }
    return out;
}


// returns ffmpeg command for duration of the part of video to keep
string getDurationCommand(string start, string time_end) {  // given times are in seconds
    int seconds_duration = stoi(time_end) - stoi(start);
    stringstream duration_ss;
    duration_ss << " -t " << convertSecondsToStr(seconds_duration) << " ";
    return duration_ss.str();
}


// returns the file extension of the given file
string getAndRemoveFileExtension(string &file_name_orignal) {
    int start_extension_idx = 0;
    string file_name = file_name_orignal;

    for (int i = file_name.length() - 1; i >= 0; --i) {
        if (file_name[i] == '.') {
            start_extension_idx = i;
            break;
        }
    }
    string extension = ".mp4";
    if (start_extension_idx) {
        file_name_orignal = file_name.substr(0, start_extension_idx);
        return file_name.substr(start_extension_idx, file_name.length() - start_extension_idx);
    }
    printf("\n\nWARNING: the file seems not to have extension. Assuming it is .mp4.\nFile name: %s\n\n", file_name.c_str());
    return extension;
}


// replaces all substrings `from` found in `str` with new string `into`
void replaceAllSubstrings(string &str, const string &from, const string &into) {
    if(from.empty()) return;

    size_t start_pos = 0;
    while((start_pos = str.find(from, start_pos)) != string::npos) {
        str.replace(start_pos, from.length(), into);
        start_pos += into.length(); // In case 'to' contains 'from', like replacing 'x' with 'yx'
    }
}


// prints the instructions on inputting all necessary data for trimming
void displayInputInstructions() {
    printf("In the file: ./_video_trimming_data.txt\ntype the following:\n");
    printf("1) In the first line type the name of the video to trim\n");
    printf("2) In the following lines type the start and end times of\neach part of the video You want to keep.\nFor example:\n");
    printf("00:00:00\n00:34:32\n01:32:34\n03:12:15\nThe time intervals are exclusive which means the last\nsecond of the interval is not included\n");
    printf("Times above translate to keeping parts of the\nvideo between: 00:00:00 and 00:34:31  along\nwith part of the video between  01:32:34 and 03:12:14\n");
    printf("\nOnce you typed the data into the file save that file and close it\n\n");
}
