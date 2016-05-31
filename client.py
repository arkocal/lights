# The MIT License (MIT)
#
# Copyright (c) 2016 Ali Rasim Kocal <arkocal@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import alsaaudio
import numpy as np
import array
from scipy import fft
import socket

# Recording constans
CHANNELS    = 1
INFORMAT    = alsaaudio.PCM_FORMAT_FLOAT_LE
RATE        = 22050
FRAMESIZE   = 1024

# Frequency bands
BASS = [0, 250]
MIDDLE = [250, 450]
TREBLE = [500, 2000]

# Convert frequencies to indices.
for tone in [BASS, MIDDLE, TREBLE]:
    for i in range(2):
        tone[i] = int(tone[i]*FRAMESIZE/RATE)

# Normalizing constants
C_BASS = 0.001
C_MIDDLE = 0.001
C_TREBLE = 0.001

# Network constants
SERVER_IP = "192.168.178.73"
PORT = 3300

# Audio setup
recorder=alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE)
recorder.setchannels(CHANNELS)
recorder.setrate(RATE)
recorder.setformat(INFORMAT)
recorder.setperiodsize(FRAMESIZE)

# Socket setup
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((SERVER_IP, PORT))


while True:
    buffer = array.array('f')
    buffer.fromstring(recorder.read()[1])
    data = np.array(buffer, dtype='f')

    ffted = abs(fft(data))

    b = sum(ffted[BASS[0]:BASS[1]]) * C_BASS
    m = sum(ffted[MIDDLE[0]:MIDDLE[1]]) * C_MIDDLE
    t = sum(ffted[TREBLE[0]:TREBLE[1]]) * C_TREBLE
    soc.send(bytes("{0:.2f};{1:.2f};{2:.2f}".format(t, m, b), "utf-8"))
