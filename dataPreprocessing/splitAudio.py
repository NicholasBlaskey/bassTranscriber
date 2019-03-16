# splitAudio.py
#
# This file will take all the recorded mp3 files of sample
# bass files and split them into a file where it is just a
# single note playing. We will number the frets on the fretboard
# starting with 0 for open E to 84 for the 20th fret on the high G
# string. The file output will be named fretNumber#sampleNumber.mp3

from os import listdir
from pydub import AudioSegment

SONG_TEMPO = 240                # In bpm
LENGTH_OF_PLAYING = 5           # In seconds
PATH_TO_IMPORT = "rawAudio/"    # Where the raw audio is   
PATH_TO_EXPORT = "splitAudio/"  # Where to save the audio


# split_one_file
#
# This function will split a file into one file for each of its
# notes.
#
# parameters:
#   file_name: The name of the file to split
#
# return: none
def split_one_file(file_name):        
    audio = AudioSegment.from_mp3(PATH_TO_IMPORT + file_name + ".wav")

    note_length = (int) (60 / SONG_TEMPO * 1000)
    # split sound in 5-second slices and export
    for i, chunk in enumerate(audio[::note_length]):
      with open(PATH_TO_EXPORT + file_name + "#%i.wav" % i, "wb") as f:
        chunk.export(f, format="wav")

def main():
    # Split all files in the directory
    for file_name in listdir(PATH_TO_IMPORT):
        split_one_file(file_name[:-4])
        
if __name__ == "__main__":
    main()



