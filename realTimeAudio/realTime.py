import pyaudio
import numpy as np
import time
from scipy import signal
import struct
import matplotlib.pyplot as plt
from keras import models
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from keras.preprocessing import image


THRESHOLD = 40 # dB
RATE = 44100
INPUT_BLOCK_TIME = 0.25 # 30 ms
INPUT_FRAMES_PER_BLOCK = int(RATE * INPUT_BLOCK_TIME)

TRAIN_DATA_PATH = "C:/Users/nblas/Desktop/selfstudy/deepLearning/projects/BaKeTa/bassTranscriber/dataPreprocessing/data/train"


def makeStream():
    """
    This function will make a pyaudio stream object
    to be used in reading audio from the systems default
    input

    Parameters:
    none

    Returns:
    A stream object
    A pyaudio object so it can be closed when the program is done
    """
    
    p = pyaudio.PyAudio()

    stream = p.open(format = pyaudio.paInt16,
                             channels = 1,
                             rate = RATE,
                             input = True,
                             #input_device_index = device_index,
                             frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

    return stream, p    

def makeClassIndexToFname(model):
    """
    This function makes an dictonary to convert between
    the class indexes the model predictions and the file
    names of the notes

    Parameters:
    model: A keras model to get the class information from

    Returns:
    A dictonary mapping class indexes to file names of notes
    """
    
    train_datagen = ImageDataGenerator(rescale=1./255)
    
    train_generator = train_datagen.flow_from_directory(
            TRAIN_DATA_PATH,
            target_size= (150, 150),
            batch_size= 20,
            class_mode= 'sparse')

    class_index_to_fname = {v: k for k, v in train_generator.class_indices.items()}

    return class_index_to_fname

def makeMelFromStream(stream, fileNum):
    """
    This function will turn the stream information into a mel
    spectogram that will later be used in predicting in the model

    Parameters:
    stream: A stream object to read in from
    fileNum: The number to title the file name

    Returns:
    none
    """
    
    raw_block = stream.read(INPUT_FRAMES_PER_BLOCK, exception_on_overflow = False)
    count = len(raw_block) / 2
    format = '%dh' % (count)
    snd_block = np.array(struct.unpack(format, raw_block))

    f, t, Sxx = signal.spectrogram(snd_block, RATE)
    plt.axis("off")
    plt.pcolormesh(t, f, Sxx, cmap = "inferno")
    plt.savefig('data/spec{}.png'.format(fileNum), bbox_inches='tight')

def getMidiFreqFromMel(model, fileNum, class_indexes_to_fname):
    """
    This function will predict on a given mel spectogram and
    tell the midi freq of the note it thinks it is. Note if it returns 64
    that means the model predicted silence

    Parameters:
    model: A keras model to predict with
    fileNum: The file number of the mel spectogram to predict with
    class_indexes_to_fname: A dictonary mapping the
        class indexes to file names of notes

    Returns:
    none
    """
    
    img = image.load_img("data/spec" + str(fileNum) + ".png", target_size = (150, 150))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis = 0)
    img_tensor /= 255

    prediction = model.predict(img_tensor)
    return int(class_indexes_to_fname[np.argmax(prediction[0])]) + 28

def playMidiFreq(midiFreq):
    """
    This function will play the given midi frequency the model
    predicted.

    Parameters:
    midiFreq: The midi frequency of the note to play 64 means no note

    Returns:
    none
    """
    print(midiFreq)
    if midiFreq != 64:
        pass

def main():
    stream, p = makeStream()
    stream.start_stream()
    
    model = load_model('multiModel.h5')
    class_to_fname = makeClassIndexToFname(model)
    for i in range(100):
        makeMelFromStream(stream, i)
        midiFreq = getMidiFreqFromMel(model, i, class_to_fname)
        playMidiFreq(midiFreq)

    # Close up resources
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    main()
