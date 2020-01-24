import glob
# import import_ipynb
# from tofLib import readFromProcessedNPY,detectHead
import numpy as np
import sys
# from ipywidgets import IntProgress
# from IPython.display import display
import time
import os
import random
import cv2
from scipy import signal
import librosa
import scipy
import sounddevice as sd
from matplotlib import pyplot as plt
from librosa import display as libdisp
import sounddevice as sd


from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
from pyqtgraph.dockarea import *
from scipy.signal import find_peaks
import scipy.signal as signal
# %matplotlib

plt.close('all')

cry, srCry = librosa.core.load('/home/vijayraj/Workspace/ai_trial/wavFiles/rec_cry.wav',sr=16000)
cry = librosa.util.normalize(cry)
cry_stft = librosa.core.stft(cry, hop_length= 1024)
print('here')


app = QtGui.QApplication([])

win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')
w1 = pg.LayoutWidget()

p2 = win.addPlot(title="green: speech, Red: cry")
curve1 = p2.plot(pen='r')
curve2 = p2.plot(pen='r')

# curve7 = p2.plot()
win.nextRow()
p3 = win.addPlot(title = 'signals')
curve3 = p3.plot(pen='r')
curve4 = p3.plot(pen='r')

win.nextRow()
p4 = win.addPlot(title="mixed")
curve5 = p4.plot(pen = 'r')
curve6 = p4.plot(pen = 'r')
# win.nextRow()
# p5 = win.addPlot(title = 'log-mixed')
# curve6 = p5.plot(pen = 'r')

win.show()
end_bin = 600
# freq = 1.0*(np.arange(1025)*(srSpeech)/(2048))
f0_bin_up = 40
f0_bin_low = 3
heat_map = np.zeros((f0_bin_up,))
peaks_array = []
for i in range(cry_stft.shape[1]):
    curCry = cry_stft[:,i][:450]
    
    curve1.setData((np.abs(curCry)[50:]),pen=(0,255,0), name="Green curve")
    print('i = ',i)
    # raw_input()
    time.sleep(0.002)
    app.processEvents()
