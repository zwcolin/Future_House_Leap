import aubio
from playsound import playSound
import threading as th
import time
#partially cited from: https://git.aubio.org/?p=aubio.git;a=blob;f=python/demos/demo_pitch.py;h=81f17cd4b3eed408abb31adbccd1ba39296dbacd;hb=c3c6305987848593034cb34501a9d3bc7afd6e8c
#original code is to detect freq, while for complex music, I modified it so it detects onset with mode 'specflux'
def detect(filename):
    result = []
    downsample = 8
    samplerate = 44100 / downsample
    win_s = 4096 / downsample # fft size
    hop_s = 512  / downsample # hop size
    s = aubio.source(filename, int(samplerate), int(hop_s))
    samplerate = s.samplerate
    tolerance = 0.8
    pitch_o = aubio.onset("specdiff", int(win_s), int(hop_s), int(samplerate))
    #pitch_o.set_unit("freq")
    #pitch_o.set_tolerance(tolerance)
    pitches = []
    confidences = []
    # total number of frames read
    total_frames = 0
    counter = 0
    while True:
        samples, read = s()
        pitch = round(pitch_o(samples)[0],2)
        confidence = 1#pitch_o.get_confidence()
        result.append((int(round((total_frames / float(samplerate)),2)*100), pitch, confidence))
        pitches += [pitch]
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break
    letterList = []
    newPitches = []
    for index in range(0, len(pitches), len(pitches)//20):
        totalFreq = 0
        if(index+5 <= len(pitches)):
            for freq in range(index, index+5):
                totalFreq += pitches[freq]
            averageFreq = totalFreq/5
            newPitches.append(averageFreq)
        else:
            counter = 0
            for index in xrange(index, len(pitches)):
                totalFreq += pitches[freq]
                counter += 1
            averageFreq = totalFreq/counter
            newPitches.append(averageFreq)

    for i in range(len(result)-1,-1,-1):
        time, freq, conf = result[i]
        if freq == 0:
            result.pop(i)
    finalSet = list()
    for i in range(len(result)):
        a,b,c = result[i]
        if a > 220:
            finalSet.append(a-220)
    return finalSet

'''i = 0
a = detect("tech.wav")
t = th.Thread(target = playSound, args = ("tech.wav",))
start = time.time()
t.start()
while True:
    currTime = time.time()
    #print (currTime-start)
    if (currTime-start) in a:
        print(i)
        i+=1'''

