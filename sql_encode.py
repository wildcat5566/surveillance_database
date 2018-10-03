import numpy as np
import struct

# Datetime format
def digit_format(number):
    if number < 10:
        return '0'+str(number)
    else:
       return str(number)

def datetime_format(YYYY, MM, DD, hh, mm, ss):
    formatted = str(YYYY) + '-' + digit_format(MM) + '-' + digit_format(DD) \
    + ' ' + digit_format(hh) + ":" + digit_format(mm) + ":" + digit_format(ss)
    return formatted

# Float-hex conversion
def dec2hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])[2:]

def hex2dec(h):
    return struct.unpack('!f', h.decode('hex'))[0]

