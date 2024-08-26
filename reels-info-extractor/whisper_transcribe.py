import sys
import os
import whisper
from pydub import AudioSegment
from tempfile import TemporaryDirectory
from yt_dlp import YoutubeDL

# Function to download YouTube video and convert it to audio using yt-dlp
def download_youtube_video(video_url, output_path):
    """
    Downloads a YouTube video and converts it into an audio file (MP3 format).
    This function uses yt-dlp to download the video and pydub to convert it to audio.

    :param video_url: The URL of the YouTube video to download.
    :param output_path: The path where the output audio file should be saved.
    :return: The path to the saved audio file.
    """
    print("Starting to download the YouTube video...")
    
    # yt-dlp options for extracting audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        download_path = ydl.prepare_filename(info_dict).rsplit('.', 1)[0] + '.mp3'
    
    print(f"Audio file saved at: {download_path}")
    return download_path

# Function to split audio into chunks of ≤ 25 MB
def split_audio(audio_file_path, chunk_size=25 * 1024 * 1024):
    """
    Splits an audio file into smaller chunks that are each ≤ 25 MB.
    
    :param audio_file_path: Path to the original audio file.
    :param chunk_size: The maximum size of each chunk in bytes (default is 25 MB).
    :return: A list of audio chunks.
    """
    print(f"Splitting audio file into chunks of {chunk_size / (1024 * 1024)} MB each...")
    audio = AudioSegment.from_file(audio_file_path)
    chunk_length = len(audio) * chunk_size / os.path.getsize(audio_file_path)
    chunks = [audio[i:i + chunk_length] for i in range(0, len(audio), chunk_length)]
    print(f"Audio file split into {len(chunks)} chunks.")
    return chunks

# Function to transcribe audio using Whisper
def transcribe_audio(file_path):
    """
    Transcribes an audio file using the Whisper model. If the file is larger than 25 MB, 
    it splits the audio into smaller chunks, transcribes each chunk, and combines the results.
    
    :param file_path: Path to the audio file.
    :return: The transcription text.
    """
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    
    file_size = os.path.getsize(file_path)
    print(f"Audio file size: {file_size / (1024 * 1024)} MB")

    if file_size <= 25 * 1024 * 1024:  # ≤ 25 MB
        print("Transcribing the entire audio file...")
        result = model.transcribe(file_path)
        print("Transcription completed.")
        return result['text']
    else:
        print("File is larger than 25 MB, splitting and transcribing in chunks...")
        transcription = []
        with TemporaryDirectory() as temp_dir:
            chunks = split_audio(file_path)
            for i, chunk in enumerate(chunks):
                chunk_path = os.path.join(temp_dir, f"chunk_{i}.mp3")
                print(f"Exporting chunk {i + 1} to {chunk_path}...")
                chunk.export(chunk_path, format="mp3")
                
                print(f"Transcribing chunk {i + 1}...")
                result = model.transcribe(chunk_path)
                transcription.append(result['text'])
        print("Combining transcriptions from all chunks.")
        return ' '.join(transcription)

if __name__ == "__main__":
    # Hard-coded YouTube URL for testing
    youtube_url = "https://www.youtube.com/watch?v=w2n_p81bUhs"  # Replace with your desired YouTube URL
    
    # Download the YouTube video and convert it to audio
    print("Starting the process...")
    audio_file_path = download_youtube_video(youtube_url, output_path=".")
    
    # Transcribe the audio file
    print("Starting transcription...")
    transcription = transcribe_audio(audio_file_path)
    
    # Print the transcription (this will be captured by the Obsidian plugin)
    print("Transcription complete. Here is the result:")
    print(transcription)