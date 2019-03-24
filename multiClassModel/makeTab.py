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


SONG_TEMPO = 320
SONG_NAME = "bombtrack"
PATH_TO_SONG = "C:/Users/nblas/Desktop/selfstudy/deepLearning/projects/BaKeTa/bassTranscriber/songsToPredict/songs/" + SONG_NAME + ".wav"
PATH_TO_STORE_DATA = "C:/Users/nblas/Desktop/selfstudy/deepLearning/projects/BaKeTa/bassTranscriber/songsToPredict/songDataStorage/"
TRAIN_DATA_PATH = "C:/Users/nblas/Desktop/selfstudy/deepLearning/projects/BaKeTa/bassTranscriber/dataPreprocessing/data/train"


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

    train_datagen = ImageDataGenerator(rescale=1./255)
    
    train_generator = train_datagen.flow_from_directory(
            TRAIN_DATA_PATH,
            target_size= (150, 150),
            batch_size= 20,
            class_mode= 'sparse')
    
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

    # Reverse the dictonary for class indexes 
    class_indexes_to_notes = {v: k for k, v in train_generator.class_indices.items()}
    predictions = [0] * len(file_names_indexes)
    for file_index in file_names_indexes:
        # First take the highest value of the prediction probalities and get its index
        # Then convert that index to the note name through dictonary and finally convert to int
        predictions[file_index] = int(class_indexes_to_notes[np.argmax(prediction_array[file_index])])
        
    return predictions

CHARS_PER_LINE = 60
def outputTab(predictions):
    # Make a dictonary to convert from class name to tab
    fname_to_note = {}
    for i in range(5):
        fname_to_note[i] = "E" + str(i)
        fname_to_note[5 + i] = "A" + str(i)
        fname_to_note[10 + i] = "D" + str(i)

    # Add in the G string
    for i in range(21):
        fname_to_note[15 + i] = "G" + str(i)

    # Add in silence
    fname_to_note[36] = "-"
    

#    line1 = "G|-"
#    line2 = "D|-"
#    line3 = "A|-"
#    line4 = "E|-"
    line1 = line2 = line3 = line4 = ""
    output = ""
    for i, prediction in enumerate(predictions):
        note = fname_to_note[prediction]
        # Handle running out of characters and starting a new line
        if i % int(CHARS_PER_LINE / 3) == 0:
            if i != 0:
                output = output + line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 + "\n\n"
            line1 = "G|-"
            line2 = "D|-"
            line3 = "A|-"
            line4 = "E|-"

        # Check for the case in which the fret # is double digit and add
        # one extra line to all the notes without it so spacing is the same
        if len(note) > 2:
            if note[0] != "G":
                line1 += "-"
            if note[0] != "D":
                line1 += "-"
            if note[0] != "A":
                line1 += "-"
            if note[0] != "E":
                line1 += "-"
        
        
        # Add the correct note to the right place in the tab
        if note[0] == "G":
            line1 += "-" + note[1:] + "-"
        else:
            line1 += "---"
            
        if note[0] == "D":
            line2 += "-" + note[1:] + "-"
        else:
            line2 += "---"
            
        if note[0] == "A":
            line3 += "-" + note[1:] + "-"
        else:
            line3 += "---"
            
        if note[0] == "E":
            line4 += "-" + note[1:] + "-"
        else:
            line4 += "---"
        
    # Add remaining notes to the output
    output = output + line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 + "\n"
    print(output)
    
def main():
    os.mkdir(PATH_TO_STORE_DATA + SONG_NAME + "/")
    splitNoteByNote()
    makeNotesIntoMelSpecs()
    predictions = predictMelSpecs()
    outputTab(predictions)

if __name__ == "__main__":
    #main()
    #predictMelSpecs()
    #outputTab([1, 3, 5, 15, 16, 12, 11, 16, 19, 21, 1, 12, 11, 16, 19, 21, 1, 3, 5, 15, 16, 12, 11, 16, 19, 21])
    main()


    
    
