"""
This file is used to read in a list of notes
that the model predicted then make it into a
midi file with various effects.
"""

import csv
from midiutil import MIDIFile

SONG_NAME = "turnASquare2"
PATH_TO_CSV = "C:/Users/nblas/Desktop/selfstudy/deepLearning/projects/BaKeTa/bassTranscriber/songsToPredict/songDataStorage/" + SONG_NAME + "/" + SONG_NAME + ".csv"
PATH_TO_SAVE = "C:/Users/nblas/Desktop/selfstudy/deepLearning/projects/BaKeTa/bassTranscriber/midiEffects/midiFiles/"
SONG_TEMPO = 480

class MIDIMaker:
    def __init__(self, name_to_save):
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
        freq = _get_MIDI_freq(self)
        if freq != -1:
            self.MIDI_song.addNote(0, 0, freq, self.time, 1, 100)
        self.time += 1

    def add_major_triad(self, octaves_up = 0):
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
    
    def save_MIDI(self):
        with open(PATH_TO_SAVE + self.name_to_save + ".mid", "wb") as output_file:
            self.MIDI_song.writeFile(output_file)        
        
def main():
    midi_song = MIDIMaker("triadsUp4Octaves")
    while (len(midi_song.data) > 0):
        midi_song.add_major_triad(5)
    midi_song.save_MIDI()

if __name__ == "__main__":
    main()
