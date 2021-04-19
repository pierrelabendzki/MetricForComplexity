import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as io
import os
from IPython.display import clear_output
import audiotools

def normaliser_son_mono(x):
    M = np.max(abs(x)); ## la plus grande valeur absolue du signal
    return  x/M;

def ConvertirWav(name_file,signal,rate):
    signal = 0.5*normaliser_son_mono(signal)  ##pour protéger vos oreilles des saturations de vos enceintes 
    scaled = np.round(32767*signal)
    signal = scaled.astype(np.int16)
    io.write(name_file, rate, signal)

def wavtoflac(filepath_wav,mode):
    mode = 8 #default  
    filepath_flac = filepath_wav.replace(".wav", ".flac")
    audiotools.open(filepath_wav).convert(filepath_flac,audiotools.FlacAudio,compression=audiotools.FlacAudio.COMPRESSION_MODES[mode])
    return filepath_flac

def fenetre_glissante(filename,duree):
    rate, x_total  = io.read(filename) 
    D =int (duree * rate) #nb ech d'1 bloc
    N= len(x_total)
    size = int(len(x_total)/rate)
    liste_ratio = np.zeros(size)
    print(size)
    for k in range (size):
        t_in1 = k  
        n1 = int(t_in1*rate)
        n2 = n1+D
        if (n2<N):
            x= x_total[n1:n2]
            avancement = (n2)/len(x_total)
            clear_output(wait=True)
            print(str(n1+D)+ ' / '+ str(len(x_total))+' === '+str(avancement),flush=True)
            filepath_wav = "trash_chunk.wav"
            ConvertirWav(filepath_wav,x ,44100)
            size_wav = os.path.getsize(filepath_wav)
            filepath_flac = wavtoflac(filepath_wav,8)
            size_flac = os.path.getsize(filepath_flac)
            liste_ratio[k] = size_flac/size_wav
        if (n2>=N):
            ecart = (n2-N)
            n2 = n2 - ecart
            x= x_total[n1:n2]
            avancement = (n2)/len(x_total)
            #clear_output(wait=True)
            print(str(n1+D)+ ' / '+ str(len(x_total))+' === '+str(avancement),flush=True)
            filepath_wav = "trash_chunk.wav"
            ConvertirWav(filepath_wav,x ,44100)
            size_wav = os.path.getsize(filepath_wav)
            filepath_flac = wavtoflac(filepath_wav,8)
            size_flac = os.path.getsize(filepath_flac)
            liste_ratio[k:] = size_flac/size_wav 
            break
    print(str(duree) + ' done ')     
    return liste_ratio

def fenetre_cumul(filename,step):
    rate, x_total  = io.read(filename) 
    D =int (step * rate) #nb ech d'1 bloc
    N= len(x_total)
    size = int(len(x_total)/rate)
    liste_ratio = np.zeros(size)
    print(size)
    for k in range (size):
        t_in1 = k  
        n0 = 0
        n1 = int(t_in1*rate)
        if ((n1+D)<N):
            x= x_total[n0:(n1+D)]
            avancement = n1/N
            clear_output(wait=True)
            print(str(n1+D)+ ' / '+ str(len(x_total))+' === '+str(avancement),flush=True)
            filepath_wav = "trash_chunk.wav"
            ConvertirWav(filepath_wav,x ,44100)
            size_wav = os.path.getsize(filepath_wav)
            filepath_flac = wavtoflac(filepath_wav,8)
            size_flac = os.path.getsize(filepath_flac)
            liste_ratio[k] = size_flac/size_wav 
    print(str(step) + ' done ')    
    return liste_ratio
  
filename = 'TheWellTemperedClavier.wav'
list_slide_5 = fenetre_glissante(filename,5)
list_slide_10 = fenetre_glissante(filename,10)
list_cumul_1 = fenetre_cumul(filename,1)

plt.figure(figsize=(15,6))
plt.plot(list_slide_5, label = 'sliding window 5s' )
plt.plot(list_slide_10, label = 'sliding window 10s' )
plt.plot(liste_cumul_1, label = 'cumulative window 1s' )

plt.legend(fontsize = 16)
plt.legend(loc="lower center", bbox_to_anchor=(0.2, 0.0, 0.5, 0.1),ncol = 3)
plt.show()
