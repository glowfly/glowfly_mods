import sys
import time
import glob
import math
import serial
import struct
import time

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def checkAck(ser):
    response = ser.read()
    if struct.unpack('B', response)[0] == 30:
        return True
    elif struct.unpack('B', response)[0] == 31:
        return False
    else:
        print('syncBlink did not answer correctly ...')
        sys.exit()


if len(sys.argv) != 3:
    print('Usage: writeMod.py COMPORT MODFILE')
    print(serial_ports())
    sys.exit()

ser = serial.Serial(sys.argv[1], 74880, timeout=15)

print('Sending write request ...')
ser.write(struct.pack('B', 30))
checkAck(ser)

print('Reading MOD file ...')
file = open(sys.argv[2], "r") 
modContent = file.read()

modContentLen = len(modContent)
print('Sending MOD length (' + str(modContentLen) + ') ...')
ser.write(struct.pack('<I', modContentLen))
if not checkAck(ser):
    print('MOD length to high!')
    sys.exit()

print('Sending and Writing MOD ...')
modBytes = modContent.encode()
# Send in chunks to avoid serial buffer errors
# and wait ack from syncBlink before sending next chunk
for i in range(0, modContentLen, 128):
    ser.write(modBytes[i:i + 128])
    checkAck(ser)
checkAck(ser)