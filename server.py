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

import socket
import mraa

r = mraa.Pwm(3)
g = mraa.Pwm(5)
b = mraa.Pwm(6)

for p in [r,g,b]:
    p.enable(True)
    p.period_us(10000)


def set_leds(message):
    try:
        r_v, g_v, b_v = [float(i) for i in message.split(";")]
    except:
        print ("Ignoring error")
        return
    # Constant multipications as LED do not change
    # brightness linearly after a certain point.
    # Squares are used to increase contrast between silent
    # and loud moments.
    r.write(r_v**2 / 2)
    g.write(g_v**2 * 10)
    b.write(b_v**2/10)


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((socket.gethostname(), 3300))
serversocket.listen(1)

clientsocket, adress = serversocket.accept()

while True:
    set_leds(clientsocket.recv(256))
