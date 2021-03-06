"""
This file is used to move the mel spectrogram data
in a fashion that is easy to work with in a keras
image generator. The data is split into train and
validation folders with the train and validation folder
having subfolders for each class to put the data in.
"""

import os, shutil
import random

DATA_STORED_IN = "melSpecs/"
TRAIN_LOCATION = "data/train/"
VALIDATION_LOCATION = "data/validation/"
VALIDATION_PERCENT = .20
NUMBER_CLASSES = 37

def main():
    """
    This function copies over the data to a new format and
    splits it into train and validation sets.

    Parameters:
    none

    Returns:
    none
    """
    
    os.mkdir(TRAIN_LOCATION)
    os.mkdir(VALIDATION_LOCATION)

    
    # make a directory for each of the classes
    file_arrays = []
    for i in range(NUMBER_CLASSES):
        os.mkdir(TRAIN_LOCATION + str(i))
        os.mkdir(VALIDATION_LOCATION + str(i))
        file_arrays.append([])

    # Store the file names into an array of arrays for each class
    for file_name in os.listdir("melSpecs"):
        file_arrays[int(file_name.split("#")[0])].append(
            file_name)

    # Loop for each class array
    for class_num, class_array in enumerate(file_arrays):
        # Shuffle to ensure randomness
        random.shuffle(class_array)
        
        # Copy all the validation data over
        for i in range(int(VALIDATION_PERCENT * len(class_array))):
            shutil.copyfile(DATA_STORED_IN + class_array[i],
                            VALIDATION_LOCATION + str(class_num) + "/" + class_array[i])

        # Copy all the train data over
        for i in range(int(VALIDATION_PERCENT * len(class_array)),
                       len(class_array)):
            shutil.copyfile(DATA_STORED_IN + class_array[i],
                            TRAIN_LOCATION + str(class_num) + "/" + class_array[i])
            
if __name__ == "__main__":
    main()



