"""
This file will take all the recorded mp3 files of sample
bass files and split them into a file where it is just a
single note playing. We will number the frets on the fretboard
starting with 0 for open E to 33 for the 18th fret on the high G
string. The file output will be named fretNumber#sampleNumber.mp3
"""

from os import listdir
from pydub import AudioSegment

SONG_TEMPO = 240                # In bpm
PATH_TO_IMPORT = "rawAudio/"    # Where the raw audio is   
PATH_TO_EXPORT = "splitAudio/"  # Where to save the audio

def split_one_file(file_name):
    """
    This function will split one file into many files one for each
    note.

    Parameters:
    file_name: The file name of the audio to split without the .wav
    extension.

    Returns:
    none
    """
    
    audio = AudioSegment.from_mp3(PATH_TO_IMPORT + file_name + ".wav")

    note_length = (int) (60 / SONG_TEMPO * 1000)
    for i, chunk in enumerate(audio[::note_length]):
      with open(PATH_TO_EXPORT + file_name + "#%i.wav" % i, "wb") as f:
        chunk.export(f, format="wav")

def main():
    """
    This function will split all files in a directory
    into many files one for each note

    Parameters:
    none

    Returns:
    none
    """
    
    for file_name in listdir(PATH_TO_IMPORT):
        # Remove the .wav extension
        split_one_file(file_name[:-4])
        
if __name__ == "__main__":
    main()



