"""
This file will take an audio file then
create a bass tab off a model previously made.
"""

import os
from pydub import AudioSegment
import matplotlib
matplotlib.use('Agg')           # No pictures displayed 
import pylab
import librosa
import librosa.display
import numpy as np
from keras import models
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model


SONG_TEMPO = 240
SONG_NAME = "turnASquare"
PATH_TO_SONG = "C:/Users/nblas/Desktop/selfstudy/deepLearning/projects/BaKeTa/bassTranscriber/songsToPredict/songs/" + SONG_NAME + ".wav"
PATH_TO_STORE_DATA = "C:/Users/nblas/Desktop/selfstudy/deepLearning/projects/BaKeTa/bassTranscriber/songsToPredict/songDataStorage/"

def splitNoteByNote():
    """
    This function takes the audio and splits it into a many
    .wav files one for each note in a directory called splits.

    Parameters:
    none

    Returns:
    none
    """
    
    os.mkdir(PATH_TO_STORE_DATA + SONG_NAME + "/splits/")
    audio = AudioSegment.from_mp3(PATH_TO_SONG)
    note_length = (int) (60 / SONG_TEMPO * 1000)

    # Make note length chunks of the audio and save them all as individual files
    for i, chunk in enumerate(audio[::note_length]):
      with open(PATH_TO_STORE_DATA + SONG_NAME + "/splits/%i.wav" % i, "wb") as f:
        chunk.export(f, format="wav")

def makeNotesIntoMelSpecs():
    """
    This function takes all the audio note files and turns
    them all into mel spectograms in a directory called melSpecs.

    Parameters:
    none

    Returns:
    none
    """
    
    os.mkdir(PATH_TO_STORE_DATA + SONG_NAME + "/melSpecs/")
    os.mkdir(PATH_TO_STORE_DATA + SONG_NAME + "/melSpecs/images/")
    for file_name in os.listdir(PATH_TO_STORE_DATA + SONG_NAME + "/splits/"):
        # Load the song
        sig, fs = librosa.load(PATH_TO_STORE_DATA + SONG_NAME + "/splits/" + file_name)   
        save_path = PATH_TO_STORE_DATA + SONG_NAME + "/melSpecs/images/" + file_name.split(".")[0] + ".png"   

        # Format and make and save the mel spectogram
        pylab.axis('off') # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # Remove the white edge
        S = librosa.feature.melspectrogram(y=sig, sr=fs)
        librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
        pylab.savefig(save_path, bbox_inches=None, pad_inches=0)
        pylab.close()
             
def predictMelSpecs():
    """
    This function will predict all the notes in the song by
    using our previously trained model.

    Parameters:
    none

    Returns:
    predictions: an list of all note predictions sequentially
    starting at 0 as the first note
    """

    dir_to_data = PATH_TO_STORE_DATA + SONG_NAME + "/melSpecs"
    model = load_model('multiModel.h5')

    song_datagen = ImageDataGenerator(rescale = 1./255)

    song_generator = song_datagen.flow_from_directory(
            directory = dir_to_data,
            target_size= (150, 150),
            batch_size= 1,
            shuffle = False,
            class_mode= None)

    file_names = song_generator.filenames
    file_names_indexes = []

    song_generator.reset()
    prediction_array = model.predict_generator(song_generator, verbose=1, steps = len(dir_to_data + "/images/"))

    predictions = []
    for file_name in file_names:
        # Remove file extension and the directory info and cast to int
        file_names_indexes.append(int(file_name.split(".")[0].split("\\")[1]))

    predictions = [0] * len(file_names_indexes)
    for file_index in file_names_indexes:
        predictions[file_index] = np.argmax(prediction_array[file_index])
        print(file_index)
        
    #for prediction in prediction_array:
    #    predictions.append(np.argmax(prediction))
    
    print(predictions)
    return predictions
             
def outputTab(predictions):
    line_1 = "G|"
    line_2 = "D|"
    line_3 = "A|"
    line_4 = "E|"

def main():
    os.mkdir(PATH_TO_STORE_DATA + SONG_NAME + "/")
    splitNoteByNote()
    makeNotesIntoMelSpecs()
    predictions = predictMelSpecs()
    outputTab(predictions)

if __name__ == "__main__":
    #main()
    predictMelSpecs()




    
    
