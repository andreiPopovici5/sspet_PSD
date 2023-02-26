import os
import scipy.signal
from scipy.io.wavfile import read
import numpy as np

def calculatePSDSignal(A1,F1,A2,F2,A3,F3,A4,F4,A5,F5,A6,F6,noise):
    #define signal
    sampling_f=1000
    dt=0.001
    t=np.arange(0+dt,2+dt,dt)
    signal=A1*np.sin(2*np.pi*F1*t)+A2*np.sin(2*np.pi*F2*t)+A3*np.sin(2*np.pi*F3*t)+A4*np.sin(2*np.pi*F4*t)+A5*np.sin(2*np.pi*F5*t)+A6*np.sin(2*np.pi*F6*t)

    #add noise
    signal +=noise*np.random.randn(len(signal)) 

    #calculate PSD with welch
    freq_signal,P_signal=scipy.signal.welch(signal, sampling_f, nperseg= 2000)

    return (t,signal,freq_signal,P_signal)

def calculatePSDAudio(freq, recording):
    return scipy.signal.welch(recording, freq, nperseg= 2000)
