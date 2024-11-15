import subprocess
import os

# Paths for ffmpeg and ffprobe
FFMPEG_PATH = "path to ffmpeg.exe"

# Set up paths and variables
input_video = "minecraft_footage/corrected_speed.mp4"
audio_files = [
    "audio/1_1gmcg2f.mp3", "audio/2_1gmap8x.mp3", "audio/3_1gi1zbg.mp3", "audio/4_1gmnr5i.mp3",
    "audio/5_1gjjce7.mp3", "audio/6_1gmddrl.mp3", "audio/7_1gk3247.mp3", "audio/8_1gm27sg.mp3",
    "audio/9_1gikorf.mp3", "audio/10_1gl4x65.mp3"
]
subtitle_files = [
    "subtitles/1_1gmcg2f.srt", "subtitles/2_1gmap8x.srt", "subtitles/3_1gi1zbg.srt", "subtitles/4_1gmnr5i.srt",
    "subtitles/5_1gjjce7.srt", "subtitles/6_1gmddrl.srt", "subtitles/7_1gk3247.srt", "subtitles/8_1gm27sg.srt",
    "subtitles/9_1gikorf.srt", "subtitles/10_1gl4x65.srt"
]
output_folder = "final_videos"
os.makedirs(output_folder, exist_ok=True)

def get_audio_duration(audio_file):
    """Get the duration of an audio file using ffmpeg."""
    result = subprocess.run(
        [FFMPEG_PATH, "-i", audio_file, "-f", "null", "-"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = result.stderr.decode()

    # Extract duration from output
    duration_line = next((line for line in output.splitlines() if "Duration" in line), None)
    if duration_line:
        time_str = duration_line.split(",")[0].split()[1]  # Extract HH:MM:SS.MS
        hours, minutes, seconds = map(float, time_str.split(":"))
        duration = hours * 3600 + minutes * 60 + seconds
        return duration
    else:
        raise ValueError("Could not retrieve duration.")

def extend_video(input_video, output_video, duration):
    """Extend the video to a specified duration by looping."""
    subprocess.run([
        FFMPEG_PATH, "-stream_loop", "-1", "-i", input_video, "-t", str(duration),
        "-c", "copy", output_video
    ])

def create_video_with_audio_subtitle(video, audio, subtitle, output):
    """Overlay audio and centered, improved subtitles onto the video."""
    subprocess.run([
        FFMPEG_PATH, "-i", video, "-i", audio, 
        "-vf", f"subtitles={subtitle}:force_style='FontSize=24,PrimaryColour=&HFFFFFF&,BackColour=&H80000000&,Alignment=2'",
        "-c:v", "libx264", "-c:a", "aac", "-shortest", "-t", str(get_audio_duration(audio)), output
    ])

# Process each audio, subtitle pair
for i, (audio, subtitle) in enumerate(zip(audio_files, subtitle_files), start=1):
    duration = get_audio_duration(audio)
    
    # Extend the video to match each audio file's length
    extended_video = f"extended_video_{i}.mp4"
    extend_video(input_video, extended_video, duration)
    
    # Create the final video with synced audio and centered subtitles
    output_video = os.path.join(output_folder, f"final_video_{i}.mp4")
    create_video_with_audio_subtitle(extended_video, audio, subtitle, output_video)
    
    # Remove the extended video after combining
    os.remove(extended_video)

print("All videos have been created successfully, each ending exactly when the audio ends.")
