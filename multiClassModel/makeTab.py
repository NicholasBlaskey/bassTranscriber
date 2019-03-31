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
from midiutil import MIDIFile
import csv

SONG_TEMPO = 480
SONG_NAME = "actualBeatboxing"
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
    prediction_array = model.predict_generator(song_generator, verbose=1, steps = len(os.listdir(dir_to_data + "/images/")))

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
        predictions[file_index] = fname_to_note[int(class_indexes_to_notes[np.argmax(prediction_array[file_index])])]

    print(predictions)
    return predictions

CHARS_PER_LINE = 60
def outputTab(predictions):
    """
    This file outputs a bass tab for the song given
    based on the predictions of the model.

    Parameters:
    predictions: A list containing the models prediction for each note

    Returns:
    none
    """

    line1 = line2 = line3 = line4 = ""
    output = ""
    for i, note in enumerate(predictions):
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

def createMIDI(predictions):
    """
    This function will create a midi file of the
    notes predicted by the model.

    Parameters:
    predictions: A list containing all the predictions in order

    Returns:
    none
    """
    
    song_MIDI = MIDIFile(1) # Make the midi file with one track

    # Track 0, time 0, tempo is the song tempo
    song_MIDI.addTempo(0, 0, SONG_TEMPO)

    for i, prediction in enumerate(predictions):
        # if the prediction is silence go to next note
        if prediction[0] == "-":
            continue
        # Otherwise get the midi frequency for the open string
        elif prediction[0] == "E":
            midi_freq = 28
        elif prediction[0] == "A":
            midi_freq = 33
        elif prediction[0] == "D":
            midi_freq = 38
        elif prediction[0] == "G":
            midi_freq = 43

        # track is 0, channel is 0, midi_freq + number of frets, time is just i
        # time is assumed to be one quarter note for now, volume 100/127
        song_MIDI.addNote(0, 0, midi_freq + int(prediction[1:]), i, 1, 100)

    # Write the midi data to a file with the same name as our song    
    with open(PATH_TO_STORE_DATA + SONG_NAME + "/" + SONG_NAME + ".mid", "wb") as output_file:
        song_MIDI.writeFile(output_file)

def saveAsCSV(predictions):
    """
    This function will save the prediction array as
    one row of a csv file to be used in later

    Parameters:
    predictions: A list of note predictions

    Returns:
    none
    """
    
    myFile = open(PATH_TO_STORE_DATA + SONG_NAME + "/" + SONG_NAME + '.csv', 'w', newline = "")
    with myFile:
        writer = csv.writer(myFile)
        writer.writerow(predictions)

def main():
    """
    This function will preproccess the data, make the tab,
    make a midi file of the tab, and save the predictions as a
    CSV file.

    Parameters:
    none

    Returns:
    none
    """

    os.mkdir(PATH_TO_STORE_DATA + SONG_NAME + "/")
    splitNoteByNote()
    makeNotesIntoMelSpecs()
    predictions = predictMelSpecs()
    outputTab(predictions)
    createMIDI(predictions)
    saveAsCSV(predictions)

if __name__ == "__main__":
    main()

    
    
