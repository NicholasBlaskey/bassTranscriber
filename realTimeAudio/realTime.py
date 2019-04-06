import pyaudio
import numpy as np
import time
from scipy import signal
import struct
import matplotlib.pyplot as plt

p = pyaudio.PyAudio()

CHANNELS = 1
RATE = 44100

def callback(in_data, frame_count, time_info, flag):
    # using Numpy to convert to array for processing
    # audio_data = np.fromstring(in_data, dtype=np.float32)
    return in_data, pyaudio.paContinue

THRESHOLD = 40 # dB
RATE = 44100
INPUT_BLOCK_TIME = 0.25 # 30 ms
INPUT_FRAMES_PER_BLOCK = int(RATE * INPUT_BLOCK_TIME)

stream = p.open(format = pyaudio.paInt16,
                         channels = 1,
                         rate = RATE,
                         input = True,
                         #input_device_index = device_index,
                         frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

stream.start_stream()



for i in range(10):
    raw_block = stream.read(INPUT_FRAMES_PER_BLOCK, exception_on_overflow = False)
    count = len(raw_block) / 2
    format = '%dh' % (count)
    snd_block = np.array(struct.unpack(format, raw_block))

    f, t, Sxx = signal.spectrogram(snd_block, RATE)
    plt.axis("off")
    plt.pcolormesh(t, f, Sxx, cmap = "inferno")
    plt.savefig('spec{}.png'.format(i), bbox_inches='tight')

    
stream.stop_stream()
stream.close()

p.terminate()
