"""
This file will create a multiclass model that is
used to classify between many bass guitar notes.
It will train and save the model too.
"""

from keras import layers
from keras import models
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
import matplotlib
matplotlib.use('Agg')           # No pictures displayed 
import matplotlib.pyplot as plt
import numpy
from keras.models import load_model

TRAIN_DATA_PATH = "C:/Users/nblas/Desktop/selfstudy/deepLearning/projects/BaKeTa/bassTranscriber/dataPreprocessing/data/train"
VAL_DATA_PATH = "C:/Users/nblas/Desktop/selfstudy/deepLearning/projects/BaKeTa/bassTranscriber/dataPreprocessing/data/validation"

def make_generators():
    """
    This function will make out generators to provide our
    model with both train and validation data.

    Parameters:
    none

    Returns:
    train_generator: A generator to give our model training data
    validation_generator: A generator to give out model validation data
    """
    
    # All images will be rescaled by 1./255
    train_datagen = ImageDataGenerator(rescale=1./255)
    test_datagen = ImageDataGenerator(rescale=1./255)

    
    train_generator = train_datagen.flow_from_directory(
            TRAIN_DATA_PATH,
            target_size= (150, 150),
            batch_size= 20,
            class_mode= 'sparse')

    validation_generator = test_datagen.flow_from_directory(
            VAL_DATA_PATH,
            target_size= (150, 150),
            batch_size= 20,
            class_mode= 'sparse')

    return train_generator, validation_generator

def make_model():
    """
    This function will make and compile our model.

    Parameters:
    none

    Returns:
    none
    """
    
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu',
                            input_shape=(150, 150, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.Dense(37, activation='softmax'))
    
    #model.add(layers.Dense(1, activation='sigmoid'))
    

    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=optimizers.RMSprop(lr=1e-4),
                  metrics=['acc'])
    return model

def plotHistory(history):
    """
    This function will plot and save the history of
    the training of model to two external png file.
    One for the model loss over the epochs and one for
    the model accuracy over the epochs.

    Parameters:
    history: An object that contains the history of the model
    over training

    Returns:
    none
    """
    
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(len(acc))
    
    # Make and save the plot for our accuracy
    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()
    plt.savefig("trainValAcc.png")

    # Make and save the plots for our loss 
    plt.figure()
    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    plt.show()
    plt.savefig("trainValLoss.png")

def main():
    """
    This function will create, compile, train, plot the history of,
    and save the model that will predict between many bass guitar notes.

    Parameters:
    none

    Returns:
    none
    """
    
    model = make_model()
    train_generator, validation_generator = make_generators()
    
    history = model.fit_generator(
      train_generator,
      steps_per_epoch=350,
      epochs=15,
      validation_data=validation_generator,
      validation_steps=70)

    model.save('multiModel.h5')
    
    plotHistory(history)

def load_our_model():
    """
    This function will load our model and then continue training.

    Parameters:
    none

    Returns:
    none
    """
    
    model = load_model('multiModel.h5')
    train_generator, validation_generator = make_generators()
    
    history = model.fit_generator(
      train_generator,
      steps_per_epoch= 145,
      epochs= 30,
      validation_data=validation_generator,
      validation_steps=50)
    plotHistory(history)

    
#load_our_model()

if __name__ == "__main__":
    main()





    
    
