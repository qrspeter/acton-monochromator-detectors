import serial
import time
import datetime
import os

import pyvisa as visa
from ThorlabsPM100 import ThorlabsPM100

import matplotlib.pyplot as plt
import numpy as np

# Wavelength range
start = 300
stop = 1700
step = 10

path = './data/'
if not os.path.exists(path):
    os.makedirs(path)

def goto(nm: int) -> None:
    #mono.write(bytes(str(nm),'ascii') + b' goto\r')
    mono.write(bytes(format(nm, '.3f'),'ascii') + b' goto\r')
    
def progressbar(current, total, bar_length=20):
    fraction = current/total
    arrow = int(fraction * bar_length) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '
    ending = '\n' if current == total else '\r'
    print(f'Progress: [{arrow}{padding}] {int(fraction*100)}%', end=ending)

# connect monochromator
mono = serial.Serial('COM5', 9600, timeout=3)
if(mono.isOpen() == False):
    sys.exit('port is absent') # exit() / quit() ?

# connect Thorlabs Powermeter
address = 'USB0::0x1313::0x8078::P0013429::INSTR'
rm = visa.ResourceManager()
inst = rm.open_resource(address)
power_meter = ThorlabsPM100(inst=inst)
inst.timeout = None

mono.write(b'MODEL\r')
print(mono.readline().strip())


wavelengths = np.arange(start, stop, step)
#wavelength = [i for i in range (start, stop, step)]
results = []

goto(start)
time.sleep(5)

for n, i in enumerate(wavelengths):
    goto(i)
    mono.write(b'.READ\r')
    power = power_meter.read
    print(format(i, '.3f'), ' nm, ', format(power, '.3e'), ' W', end=' ')
    progressbar(n+1, wavelengths.shape[0])
    results.append(power)
    
    time.sleep(0.5)

#print(wavelength)
#print(results)

plt.plot(wavelengths, results)
''
time_for_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = path + 'spectrum_' + time_for_name

npresult = np.stack((wavelengths, np.array(results)))
#npresult = np.stack((np.array(wavelength, dtype='float'), np.array(results)))

np.savetxt(filename + '.csv', npresult.T, fmt='%1.4e', delimiter=',', header='# Wavelength(nm), Intensity (W)')

plt.savefig(filename + '.png')

plt.show()

mono.close()


exit(0)