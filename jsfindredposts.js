// I do not know what this does atm, 🙃

const fs = require('fs');
const path = require('path');

// Define paths
const audioFolder = 'audio';                      // Folder where audio files (.mp3) are stored
const textFolder = 'mcmodvids/reddit story finds';   // Folder where text files (.txt) are stored
const outputFolder = 'subtitles';                 // Folder where SRT files will be saved

// Duration per subtitle line in seconds
const durationPerLine = 3;  // Adjust as needed

// Ensure the output folder exists
if (!fs.existsSync(outputFolder)) {
    fs.mkdirSync(outputFolder);
}

// Function to create an SRT file
function createSRT(text, outputPath, durationPerLine) {
    // Split text into sentences for subtitle lines
    const lines = text.split('. ');  // Break at periods followed by space for shorter lines

    let srtContent = '';
    lines.forEach((line, index) => {
        const startTime = index * durationPerLine;
        const endTime = (index + 1) * durationPerLine;

        // Format start and end times as HH:MM:SS,000
        const start = new Date(startTime * 1000).toISOString().substr(11, 8) + ',000';
        const end = new Date(endTime * 1000).toISOString().substr(11, 8) + ',000';

        // Write SRT entry
        srtContent += `${index + 1}\n${start} --> ${end}\n${line.trim()}\n\n`;
    });

    // Save the SRT file
    fs.writeFileSync(outputPath, srtContent, 'utf8');
}

// Generate SRT files for each audio file
fs.readdirSync(audioFolder).forEach(audioFile => {
    if (audioFile.endsWith('.mp3')) {
        const txtFilename = audioFile.replace('.mp3', '.txt');
        const txtPath = path.join(textFolder, txtFilename);

        // Check if the corresponding text file exists
        if (fs.existsSync(txtPath)) {
            const textContent = fs.readFileSync(txtPath, 'utf8');
            
            // Remove any intro text manually if present
            const mainText = textContent.split('\n').slice(1).join('\n').trim(); // Assuming first line(s) might be intro
            
            // Generate and save SRT file
            const srtFilename = audioFile.replace('.mp3', '.srt');
            const srtPath = path.join(outputFolder, srtFilename);
            createSRT(mainText, srtPath, durationPerLine);
            console.log(`SRT file created: ${srtPath}`);
        } else {
            console.log(`Text file not found for ${audioFile}`);
        }
    }
});
