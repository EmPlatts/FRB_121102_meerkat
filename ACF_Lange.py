# Based on code by Manisha Caleb
import numpy as np
import os
import glob
import argparse
import logging

pulse_name = '02'

#set up  logging
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

#setting up parser
logging.info('Starting structure analysis...')

parser = argparse.ArgumentParser()

parser.add_argument('-s','--suffix', action='store',type=str, dest='suffix',
        help='suffix of all files to process')
parser.add_argument('-o1', '--on1', action='store', type=float, dest='on1',
        help='Start of the pulse (bin no.)')
parser.add_argument('-o2', '--on2', action='store', type=float, dest='on2',
        help='End of the pulse (bin no.)')
parser.add_argument('-t', '--tsamp', action='store', type=float, dest='sample_interval',
        help='sample interval in seconds')

#Parse args
logging.info('Parsing arguments')
args = parser.parse_args()

filestring = args.suffix
on1 = args.on1
on2 = args.on2
tsamp = args.sample_interval

# Glob the txt files
files = glob.glob('pulse_data/'+pulse_name+'/*.'+filestring)
filesorted = sorted(files)

# Calculate structure parameter for each file
iffts = []
dms = []
for f in filesorted:
   data = np.loadtxt(f, comments='File')
   dms_ = data[int(on1):int(on2),3]
   dms.append(dms_)
   fft = np.abs(np.fft.fft(data[int(on1):int(on2),3]))
   iffts.append(np.abs(np.fft.ifft(pow(fft,2)))) #ACF

# Extract front of ACF
min_idx = 0
max_idx = 120
t_grid = tsamp*np.arange(len(iffts[1]))[min_idx:max_idx] #bins to time in ms

np.save('output_data/iffts_'+pulse_name+'.npy',iffts)
np.save('output_data/time_lag_'+pulse_name+'.npy',t_grid)
np.save('output_data/dms_'+pulse_name+'.npy',dms)


