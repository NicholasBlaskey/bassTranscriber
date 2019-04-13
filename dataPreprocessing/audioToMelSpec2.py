"""
This file is used to convert given
audio segments into a mel spectogram of
another type than the librosa type
to be used in the training and validation
of the bass transcriber model. 
"""

import os
import matplotlib
matplotlib.use('Agg')           # No pictures displayed 
import pylab
from scipy import signal
from scipy.io import wavfile
import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt

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
    
    save_path = PATH_TO_EXPORT + file_name + '.png'    

    sample_rate, samples = wavfile.read(PATH_TO_IMPORT + file_name + '.wav')
    frequencies, times, spectrogram = signal.spectrogram(samples[:, 0], sample_rate)

    plt.pcolormesh(times, frequencies, spectrogram, cmap = "inferno")
    plt.axis("off")
    plt.savefig(save_path, bbox_inches='tight')

def main():
    """
    Turns all the files in the directory listed into png files.

    Parameters:
    none

    Returns:
    none
    """

    all_fnames = os.listdir(PATH_TO_IMPORT)
    for i in range(len(all_fnames)):
        all_fnames[i] = all_fnames[i][:-4]

    done_fnames = os.listdir(PATH_TO_EXPORT)
    for i in range(len(done_fnames)):
        all_fnames.remove(done_fnames[i][:-4])

    #print(len(all_fnames))
    #print(all_fnames[0])
    for file_name in all_fnames:#os.listdir(PATH_TO_IMPORT):
        # Remove the .wav file extension then convert to png
        audio_to_png(file_name) #[:-4])

if __name__ == "__main__":
    main()

