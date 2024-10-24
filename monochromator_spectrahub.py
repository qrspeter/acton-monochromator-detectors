import serial
import time
ser = serial.Serial('COM20', 9600, timeout=3)
if(ser.isOpen() == False):
    sys.exit('port is absent') # exit() / quit() ?

ser_hub = serial.Serial('COM26', 9600, timeout=3)
if(ser_hub.isOpen() == False):
    sys.exit('ser_hub is absent') # exit() / quit() ?

ser_hub.write(b'VER\r')
print(ser_hub.readline())
ser_hub.write(b'MODEL\r')
print(ser_hub.readline())
ser_hub.write(b'.READ\r')
print(ser_hub.readline())

start = 200
stop = 300
step = 10
wavelength = [i for i in range (start, stop, step)]
results = []
for i in wavelength:
    ser.write(bytes(str(i),'ascii')+b' goto\r')
    print(i, ' nm')
    ser_hub.write(b'.READ\r')
    hub_answer = ser_hub.readline()
    print(hub_answer)
    print(hub_answer.decode().strip())
    result = int(hub_answer.decode().split(sep=' ')[1])
    results.append(result)
    
    time.sleep(1)
#ser.write(b'1000 goto\r')
print(wavelength)
print(results)

ser.close()

ser_hub.close()

exit(0)