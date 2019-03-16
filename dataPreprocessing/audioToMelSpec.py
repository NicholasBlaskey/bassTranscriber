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

# audio_to_png
#
# This function will convert a single audio file
# to a melspectrogram and save it as a png.
#
# parameters:
#   file_name: The name of the file to convert
#
# return: none
def audio_to_png(file_name):    
    sig, fs = librosa.load(PATH_TO_IMPORT + file_name + '.wav')   
    save_path = PATH_TO_EXPORT + file_name + '.png'
    
    pylab.axis('off') # no axis
    pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # Remove the white edge
    S = librosa.feature.melspectrogram(y=sig, sr=fs)
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
    pylab.savefig(save_path, bbox_inches=None, pad_inches=0)
    pylab.close()

def main():
    for file_name in os.listdir(PATH_TO_IMPORT):
        audio_to_png(file_name[:-4])

if __name__ == "__main__":
    main()

