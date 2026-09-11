"""Original quiet synthesized score; no samples or third-party music."""
import numpy as np
import wave
from pathlib import Path
rate=48000;duration=121
track=np.zeros((rate*duration,2),dtype=np.float64)
chords=[(48,55,60,64),(45,52,57,60),(41,48,53,57),(43,50,55,59)]
for beat in range(0,120,6):
    notes=chords[(beat//6)%4]
    n=min(rate*9,len(track)-beat*rate);t=np.arange(n)/rate
    envelope=(1-np.exp(-t/1.4))*np.exp(-t/3.6)*np.minimum(1,(n/rate-t)/.7)
    for j,note in enumerate(notes):
        f=440*2**((note-69)/12)
        tone=(np.sin(2*np.pi*f*t)+.2*np.sin(2*np.pi*f*2*t))*.022*envelope
        track[beat*rate:beat*rate+n,0]+=tone*(.8 if j%2 else 1)
        track[beat*rate:beat*rate+n,1]+=tone*(1 if j%2 else .8)
    bell=np.sin(2*np.pi*(440*2**((notes[2]+12-69)/12))*t)*np.exp(-t*1.4)*.025
    track[beat*rate:beat*rate+n,:]+=bell[:,None]
fade=np.minimum(1,np.arange(len(track))/rate/3)*np.minimum(1,(len(track)-np.arange(len(track)))/rate/5)
pcm=(np.clip(track*fade[:,None],-1,1)*32767).astype('<i2')
Path('media/raw').mkdir(parents=True,exist_ok=True)
with wave.open('media/raw/director-score.wav','wb') as out:
    out.setnchannels(2);out.setsampwidth(2);out.setframerate(rate);out.writeframes(pcm.tobytes())
print('Original stereo score written.')
