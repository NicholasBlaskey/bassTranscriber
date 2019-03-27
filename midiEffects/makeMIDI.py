"""
This file is used to read in a list of notes
that the model predicted then make it into a
midi file with various effects.
"""

import csv
from midiutil import MIDIFile

SONG_NAME = "turnASquare"
PATH_TO_CSV = "C:/Users/nblas/Desktop/selfstudy/deepLearning/projects/BaKeTa/bassTranscriber/songsToPredict/songDataStorage/" + SONG_NAME + "/" + SONG_NAME + ".csv"
PATH_TO_SAVE = "C:/Users/nblas/Desktop/selfstudy/deepLearning/projects/BaKeTa/bassTranscriber/midiEffects/midiFiles/"
SONG_TEMPO = 240

class MIDIMaker:
    """
    This object will make a midi file based on a list of notes.
    The various methods can add effects to the notes to make a
    better sound.
    """

    def __init__(self, name_to_save):
        """
        This is the constructor of MIDIMaker. It will read in
        the note files and make the track to start adding notes
        to.

        Parameters:
        name_to_save: The name of the file to save when the midi file
                      is done

        Returns:
        none
        """
        
        with open(PATH_TO_CSV) as f:
            reader = csv.reader(f)
            # Get the data from the file and remove the nested list
            self.data = [r for r in reader][0]

        # Make a midi file with one track
        self.MIDI_song = MIDIFile(1)
        # Track 0, time 0, tempo is the song tempo
        self.MIDI_song.addTempo(0, 0, SONG_TEMPO)
        self.time = 0
        self.name_to_save = name_to_save

    def _get_MIDI_freq(self):
        """
        This method is private and will give you the frequency
        of the note from the prediction from the model. -1 means
        there is silence.

        Parameters:
        none

        Returns:
        An int representing a midi frequency cooresponding to the note
        """
        note = self.data.pop()
        if note[0] == "-":
            return -1
        elif note[0] == "E":
            midi_freq = 28
        elif note[0] == "A":
            midi_freq = 33
        elif note[0] == "D":
            midi_freq = 38
        elif note[0] == "G":
            midi_freq = 43
        return midi_freq + int(note[1:])
    
    def add_dry_note(self):
        """
        This method adds just the note to the midi file
        with no effects to it.

        Parameters:
        none

        Returns:
        none
        """
        
        freq = _get_MIDI_freq(self)
        if freq != -1:
            self.MIDI_song.addNote(0, 0, freq, self.time, 1, 100)
        self.time += 1

    def add_major_triad(self, octaves_up = 0):
        """
        This method adds a major triad with the midi frequency
        being the root note.

        Parameters:
        octaves_up: A number of octaves to shift the chord up

        Returns:
        none
        """
        
        freq = self._get_MIDI_freq()
        if freq != -1:
            octave_shift = octaves_up * 12
            
            # Add the root
            self.MIDI_song.addNote(0, 0, freq + octave_shift, self.time, 1, 100)
            
            # Add the major third
            self.MIDI_song.addNote(0, 0, freq + octave_shift + 4, self.time, 1, 100)

            # Add the fifth
            self.MIDI_song.addNote(0, 0, freq + octave_shift + 7, self.time, 1, 100)
        self.time += 1

    def add_minor_triad(self, octaves_up = 0):
        """
        This method adds a minor triad with the midi freq
        being the root note.

        Parameters:
        octaves_up: A number of octaves to shift the chord up

        Returns:
        none
        """
        
        freq = self._get_MIDI_freq()
        if freq != -1:
            octave_shift = octaves_up * 12
            
            # Add the root
            self.MIDI_song.addNote(0, 0, freq + octave_shift, self.time, 1, 100)
            
            # Add the minor third
            self.MIDI_song.addNote(0, 0, freq + octave_shift + 3, self.time, 1, 100)

            # Add the fifth
            self.MIDI_song.addNote(0, 0, freq + octave_shift + 7, self.time, 1, 100)
        self.time += 1
        
    def add_power_chord(self, octaves_up = 0):
        """
        This method adds a power chord with the midi freq being
        a root note and adds a fifth above it.

        Parameters:
        octaves_up: A number of octaves to shift the chord up

        Returns:
        none
        """
        
        freq = self._get_MIDI_freq()
        if freq != -1:
            octave_shift = octaves_up * 12
            
            # Add the root
            self.MIDI_song.addNote(0, 0, freq + octave_shift, self.time, 1, 100)

            # Add the fifth
            self.MIDI_song.addNote(0, 0, freq + octave_shift + 7, self.time, 1, 100)
        self.time += 1

    def add_palm_mute(self, octaves_up = 0):
        """
        This method adds a kind of palm mute type effect
        in which the note is played as an eigth note and
        following by a eigth note rest

        Parameters:
        octaves_up: A number of octaves to shift the note up

        Returns:
        none
        """

        freq = self._get_MIDI_freq()
        if freq != -1:
            octave_shift = octaves_up * 12

            self.MIDI_song.addNote(0, 0, freq + octave_shift, self.time, .5, 100)
            
        self.time += 1

    def root_then_note(self, octaves_up = 0, semi_tones_up = 12):
        """
        This method will play a root note as a eigth note
        then a eigth note of how many semitones up

        Parameters:
        octaves_up: A number of octaves to shift the note up
        semi_tones_up: Number of semitones up the second note should be 

        Returns:
        none
        """

        freq = self._get_MIDI_freq()
        if freq != -1:
            octave_shift = octaves_up * 12

            # Add root note
            self.MIDI_song.addNote(0, 0, freq + octave_shift, self.time, .5, 100)

            # Add whatever next note is 
            self.MIDI_song.addNote(0, 0, freq + semi_tones_up + octave_shift, self.time + .5, .5, 100)
        self.time += 1
    #def add_delay(self, octaves_up = 0):

    
    #def add_syncopation(self, octaves_up = 0):

    #def add_jittered(self, octaves_up = 0):
        
    
    def save_MIDI(self):
        with open(PATH_TO_SAVE + self.name_to_save + ".mid", "wb") as output_file:
            self.MIDI_song.writeFile(output_file)        
        
def main():
    midi_song = MIDIMaker("rootFifthBelow")
    while (len(midi_song.data) > 0):
        midi_song.root_then_note(1, -7)
    midi_song.save_MIDI()

if __name__ == "__main__":
    main()
