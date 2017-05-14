# -*- coding: utf-8 -*-
"""
Created on Tue May 02 08:50:23 2017

@author: cht15
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sc

#==============================================================================
# STFT
#==============================================================================
def stft(x, fftsize = 101, overlap = 2):   
    hop = fftsize / overlap
    w = np.kaiser(fftsize+1,4)[:-1]      # better reconstruction with this trick +1)[:-1] 
    return np.array([np.fft.rfft(w*x[i:i+fftsize]) for i in range(0, len(x)-fftsize, hop)])

#==============================================================================
# STFT - optize lenght by Heisenberg
#==============================================================================
def stft_h(signal, overlap = 2):   
    fftsize = 100
    wlist = [0]
    tlist = [0]
    for k in range(1000):
        hop = fftsize / overlap
        w = np.kaiser(fftsize+1,4)[:-1]      # better reconstruction with this trick +1)[:-1]  
    
        x =  np.array([w*signal[i:i+fftsize] for i in range(0, len(signal)-fftsize, hop)])
        X =  np.array([np.fft.rfft(w*signal[i:i+fftsize]) for i in range(0, len(signal)-fftsize, hop)])    
        
        v_w = np.var(X)
        v_t = np.var(x) 
        
        wlist = np.append(wlist,[v_w]) 
        tlist = np.append(tlist,[v_t])

        if v_t*v_w < 1/4.:
            break         
        
        elif v_t*v_w > 1/4.:
            fftsize += 10
        
    
    print fftsize         
    return X,wlist,tlist,x 
  

#==============================================================================
# DFT
#==============================================================================
def dft(x,c):
    X = np.zeros(c,dtype=complex)
    for k in range(len(x)):
        a = 0+0*1j
        for n in range(c):
            a += x[n]*np.exp(-2*np.pi*1j*k*n/float(c))
            X[k] = a
    return X

#==============================================================================
# FFT
#==============================================================================
def fft(x):
    N_new = len(x)
    if N_new == 2:
        return dft(x) # Returnerer DFT naar data ikke kan deles mere op
    else:
        X_even = fft(x[::2]) # Deler rekursivt input op - lige dele
        X_odd = fft(x[1::2]) # Deler rekursivt input op - ulige dele
        factor = np.exp(-2j * np.pi * np.arange(N_new) / N_new) # Twiddlefaktor
        return np.concatenate([X_even + factor[:N_new / 2] * X_odd,
                               X_even + factor[N_new / 2:] * X_odd])

#==============================================================================
# Decibel calculation
#==============================================================================
def db(x):
    return 20*np.log10(x)