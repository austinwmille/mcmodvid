# this script generate subtitle files (srt)

import os

# Define paths
audio_folder = "audio"                       # Folder where audio files (.mp3) are stored
text_folder = "mcmodvids/reddit story finds"    # Folder where text files (.txt) are stored
output_folder = "subtitles"                  # Folder where SRT files will be saved
os.makedirs(output_folder, exist_ok=True)

# Duration per subtitle line in seconds
duration_per_line = 3  # Adjust as needed

# Function to create an SRT file
def create_srt(text, output_path, duration_per_line):
    lines = text.split('. ')  # Break at periods followed by a space for shorter lines

    with open(output_path, "w", encoding="utf-8") as file:
        for i, line in enumerate(lines):
            start_time = i * duration_per_line
            end_time = (i + 1) * duration_per_line
            
            # Format start and end times as HH:MM:SS,000
            start = f"00:{start_time // 60:02}:{start_time % 60:02},000"
            end = f"00:{end_time // 60:02}:{end_time % 60:02},000"
            
            # Write SRT entry
            file.write(f"{i + 1}\n{start} --> {end}\n{line.strip()}\n\n")

# Generate SRT files for each audio file
for audio_file in os.listdir(audio_folder):
    if audio_file.endswith(".mp3"):
        txt_filename = audio_file.replace(".mp3", ".txt")
        txt_path = os.path.join(text_folder, txt_filename)

        # Check if the corresponding text file exists
        if os.path.exists(txt_path):
            with open(txt_path, "r", encoding="utf-8") as txt_file:
                text_content = txt_file.read()
                
                # Remove any intro text if present
                main_text = text_content.split("\n", 1)[-1].strip()
                
                # Generate and save SRT file
                srt_filename = audio_file.replace(".mp3", ".srt")
                srt_path = os.path.join(output_folder, srt_filename)
                create_srt(main_text, srt_path, duration_per_line)
                print(f"SRT file created: {srt_path}")
        else:
            print(f"Text file not found for {audio_file}")
