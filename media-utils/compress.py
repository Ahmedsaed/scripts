import os
import sys
import subprocess
import json

def get_all_video_files(directory):
        video_extensions = [".mp4", ".mkv", ".avi", ".mov", ".wmv"]
        video_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(tuple(video_extensions)):
                    video_path = os.path.join(root, file)
                    print(f"[+] Discovered: {video_path}")
                    video_files.append(video_path)
        print(f"[+] Total Files: {len(video_files)}")
        return video_files

def convert_to_mp4_h264(input_file, output_file):
    try:
        # Use ffmpeg to convert the video
        ffmpeg_cmd = [
            'ffmpeg',
            '-hwaccel', 'vaapi',
            '-i', input_file,
            '-c:v', 'h264_vaapi',
            output_file
        ]
        subprocess.run(ffmpeg_cmd, check=True)

        print(f"Converted: {input_file} -> {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_file}: {e}")
    except Exception as e:
        print(f"Error converting {input_file}: {e}")

def get_video_codec(file_path):
    try:
        ffprobe_cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name', '-of', 'json', file_path]
        result = subprocess.check_output(ffprobe_cmd, universal_newlines=True)
        codec_info = json.loads(result)
        video_codec = codec_info['streams'][0]['codec_name']
        print(f"[+] file: {os.path.basename(file_path)} \t- Codec: {video_codec}")
        return video_codec
    except Exception as e:
        print(f"[-] file: {os.path.basename(file_path)} Error: ", e)
        return None

def main():
    directory = sys.argv[1]
    print(f"[+] Directory: {directory}")
    if not os.path.isdir(directory):
        print("[-] Invalid directory.")
        sys.exit(1)

    video_files = get_all_video_files(directory)
    for file in video_files:
        codec = get_video_codec(file)
        if codec != 'h264':
            print(f"[+] Converting: {file} from {codec} to h264")
            convert_to_mp4_h264(file, os.path.splitext(file)[0] + '.mp4')
        else:
            print(f"[+] Skipping: {file} - already h264")

if __name__ == "__main__":
    main()
