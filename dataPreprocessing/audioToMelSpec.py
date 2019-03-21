"""
This file is used to convert given
audio segments into a mel spectogram
to be used in the training and validation
of the bass transcriber model. 
"""

import os
import matplotlib
matplotlib.use('Agg')           # No pictures displayed 
import pylab
import librosa
import librosa.display
import numpy as np
from pydub import AudioSegment

PATH_TO_IMPORT = "splitAudio/"  # Where the split audio is   
PATH_TO_EXPORT = "melSpecs/"    # Where to save the png

def audio_to_png(file_name):
    """
    Turns a single audio file into a melspectrogram png

    Parameters:
    file_name: The name of the file to convert without the .wav

    Returns:
    none
    """
    
    # Load the image
    sig, fs = librosa.load(PATH_TO_IMPORT + file_name + '.wav')

    save_path = PATH_TO_EXPORT + file_name + '.png'    

    pylab.axis('off') # no axis
    pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # Remove the white edge

    # Create the melspectrogram
    S = librosa.feature.melspectrogram(y=sig, sr=fs)
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
    pylab.savefig(save_path, bbox_inches=None, pad_inches=0)
    pylab.close()

def main():
    """
    Turns all the files in the directory listed into png files.

    Parameters:
    none

    Returns:
    none
    """
    
    for file_name in os.listdir(PATH_TO_IMPORT):
        # Remove the .wav file extension then convert to png
        audio_to_png(file_name[:-4])

if __name__ == "__main__":
    main()

