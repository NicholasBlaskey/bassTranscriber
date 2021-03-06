"""
This file is a test to see if a convnet
can predict relibality based on mel spectrograms
of bass guitar recordings.
"""

from keras import layers
from keras import models
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import numpy
from keras.models import load_model

TRAIN_DATA_PATH = "C:/Users/nblas/Desktop/selfstudy/deepLearning/projects/BaKeTa/bassTranscriber/dataPreprocessing/data/train"
VAL_DATA_PATH = "C:/Users/nblas/Desktop/selfstudy/deepLearning/projects/BaKeTa/bassTranscriber/dataPreprocessing/data/validation"

def make_generators():
    """
    This function makes the generators to provide out model
    with both training and validation data.

    Parameters:
    none

    Returns:
    train_generator: The generator to give the model training data
    validation_generator: The generator to give the model validation data
    """
    
    # Rescale the RGB coefficants to make it play nicer with out model
    train_datagen = ImageDataGenerator(rescale=1./255)
    test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
            TRAIN_DATA_PATH,
            target_size= (150, 150),
            batch_size= 20,
            class_mode= 'binary')

    validation_generator = test_datagen.flow_from_directory(
            VAL_DATA_PATH,
            target_size= (150, 150),
            batch_size= 20,
            class_mode= 'binary')

    return train_generator, validation_generator

def make_model():
    """
    This function will make and compile a simple keras
    convnet to use in classifying between two notes of
    bass guitar playing

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
    model.add(layers.Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer=optimizers.RMSprop(lr=1e-4),
                  metrics=['acc'])
    return model

def plotHistory(history):
    """
    This function will make a plot of both the training
    and validation history of the model over the epochs
    to see how the model did.

    Parameters:
    history: A keras object that holds the history
    of our model during training 

    Returns:
    none
    """
    
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(len(acc))

    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()

    plt.figure()

    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()

    plt.show()

def main():
    """
    This function will create the model, the generators,
    fit the model to the data, then plot the history of the
    model during training. It will also save the model at the
    end for later use if needed.

    Parameters:
    none

    Returns:
    none
    """
    
    model = make_model()
    train_generator, validation_generator = make_generators()
    
    history = model.fit_generator(
      train_generator,
      steps_per_epoch=30,
      epochs=30,
      validation_data=validation_generator,
      validation_steps=50)

    model.save('POCModel.h5')
    
    plotHistory(history)

if __name__ == "__main__":
    main()





    
    
