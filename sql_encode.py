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
    if f==0:
        return '00000000'
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])[2:]

def hex2dec(h):
    ls = []
    for dim in range(len(h)):
        if h[dim]!= None:
            sub = []
            for i in range(0, len(h[dim]), 8):
                sub.append(struct.unpack('!f', h[dim][0+i:8+i].decode('hex'))[0])
            ls.append(sub)
        else:
            ls.append(None)
    return ls
