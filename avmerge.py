import subprocess
import os

# Paths
audio_folder = "audio_outputs"
video_folder = "minecraft_footage"
srt_folder = "subtitles"           # Folder where SRT files are stored
output_folder = "final_videos"
os.makedirs(output_folder, exist_ok=True)

# Iterate over each audio file in the audio folder
for audio_file in os.listdir(audio_folder):
    if audio_file.endswith(".mp3"):
        audio_path = os.path.join(audio_folder, audio_file)
        
        # Select a random video from the video folder
        video_file = random.choice(os.listdir(video_folder))
        video_path = os.path.join(video_folder, video_file)
        
        # Set output file name
        output_file = os.path.join(output_folder, audio_file.replace(".mp3", ".mp4"))
        
        # Match SRT file to audio file
        srt_file = os.path.join(srt_folder, audio_file.replace(".mp3", ".srt"))
        
        # FFmpeg command to combine audio, video, and subtitles
        command = [
            "ffmpeg", "-i", video_path, "-i", audio_path,
            "-c:v", "copy", "-c:a", "aac", "-shortest",
            "-vf", f"subtitles={srt_file}", output_file
        ]
        
        # Run the FFmpeg command
        subprocess.run(command)
        print(f"Video with subtitles created: {output_file}")
