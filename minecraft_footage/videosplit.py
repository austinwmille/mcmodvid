# splits a given video in half to create two video files

import subprocess
import os

def get_video_duration(input_video):
    try:
        # Use ffprobe to get the video duration
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "format=duration", "-of",
             "default=noprint_wrappers=1:nokey=1", input_video],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        duration = float(result.stdout)
        return duration
    except Exception as e:
        print(f"Error retrieving duration: {e}")
        return None

def split_video_in_half(input_video, output_folder="split_videos"):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Get the video duration
    duration = get_video_duration(input_video)
    if duration is None:
        print("Could not retrieve video duration.")
        return

    # Calculate the midpoint
    midpoint = duration / 2

    # Define output file paths
    output1 = os.path.join(output_folder, "part1.mp4")
    output2 = os.path.join(output_folder, "part2.mp4")

    # Split the video into two halves
    subprocess.run([
        "ffmpeg", "-i", input_video, "-t", str(midpoint), "-c", "copy", output1
    ])
    subprocess.run([
        "ffmpeg", "-i", input_video, "-ss", str(midpoint), "-c", "copy", output2
    ])

    print(f"Video split complete. Output files: {output1}, {output2}")

# Example usage
split_video_in_half("corrected_speed.mp4")
