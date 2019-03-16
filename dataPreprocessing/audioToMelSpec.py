import os
import matplotlib
import pylab
import librosa
import librosa.display
import numpy as np
from pydub import AudioSegment

matplotlib.use('Agg')           # No pictures displayed 
PATH_TO_IMPORT = "splitAudio/"  # Where the split audio is   
PATH_TO_EXPORT = "melSpecs/"    # Where to save the png

# audio_to_png
#
# This function will convert a single audio file
# to a melspectrogram and save it as a png.
#
# parameters:
#   file_name: The name of the file to convert
#   output_name: The name of what the image should be saved as
#
# return: none
def audio_to_png(file_name, image_name):    
    sig, fs = librosa.load('rawAudio/test.wav')   
    save_path = 'testwav.png'
    
    pylab.axis('off') # no axis
    pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # Remove the white edge
    S = librosa.feature.melspectrogram(y=sig, sr=fs)
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
    pylab.savefig(output_name, bbox_inches=None, pad_inches=0)
    pylab.close()


        

