import wave
import pyaudio
def playSound(fileName):
####INITIATE####
    print("PLAYING...PLEASE WAIT...", end = "")
    wf=wave.open(fileName,'rb') # reading only
    p = pyaudio.PyAudio()
####ATTRIBUTES OF SOUND####
    FORMAT = p.get_format_from_width(wf.getsampwidth())
    CHANNELS = wf.getnchannels()
    CHUNK = 1024
    RATE = wf.getframerate()
    TIME = wf.getnframes()/wf.getframerate()
####OPEN STREAM####
    stream=p.open(format=FORMAT,
    	channels=CHANNELS, rate=RATE,output=True)
    data = wf.readframes(CHUNK)
####READ FILE####
    for i in range(int(RATE/CHUNK*TIME)):
        stream.write(data)
        data = wf.readframes(CHUNK)
####TERMINATE####
    stream.stop_stream()   
    stream.close()
    p.terminate() 
    print('FINISHED')