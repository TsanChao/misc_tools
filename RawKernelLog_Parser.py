import struct
import ctypes
import os
import sys

class StructField(object):
    '''
    Descriptor representing a simple structure field
    '''

    def __init__(self, format, offset):
        self.format = format
        self.offset = offset

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            r = struct.unpack_from(self.format, instance._buffer, self.offset)
            return r[0] if len(r) == 1 else r


class StructureMeta(type):
    '''
    Metaclass that automatically creates StructField descriptors
    '''

    def __init__(self, clsname, bases, clsdict):
        fields = getattr(self, '_fields_', [])
        byte_order = ''
        offset = 0
        for format, fieldname in fields:
            if format.startswith(('<', '>', '!', '@')):
                byte_order = format[0]
                format = format[1:]
            format = byte_order + format
            setattr(self, fieldname, StructField(format, offset))
            offset += struct.calcsize(format)
        setattr(self, 'struct_size', offset)


class Structure(object):
    __metaclass__ = StructureMeta

    def __init__(self, bytedata):
        self._buffer = bytedata

    @classmethod
    def from_file(cls, f):
        return cls(f.read(cls.struct_size))

class klog_header(Structure):
    _fields_ = [
        ('<Q', 'ts_nsec'),
        ('H', 'len'),
        ('H', 'text_len'),
        ('H', 'dict_len'),
        ('B', 'facility'),
        ('B', 'flags_level')
    ]

    def parsing_klog_header(cls, prefixdict):
        #print prefixdict
        klog_len = 0
        text_len = 0
        dict_len = 0
        fac = 0
        level = 0
        str_time = ''
        for key in prefixdict.keys():
            value = prefixdict.get(key, 0)
            if key == 'text_len':
                text_len = value
            elif key == 'dict_len':
                dict_len = value
            elif key == 'facility':
                fac = value
            elif key == 'ts_nsec':
                t = divmod(value, 1000000000)
                str_time = '[%5s.%6s]' % (t[0], t[1])
            elif key == 'flags_level':
                level = value >> 5
            elif key == 'len':
                klog_len = value
            else:
                print 'error'
        #print text_len, dict_len
        if ((((text_len + dict_len + cls.__getattribute__('struct_size') + 3) & ~3) != klog_len) and (
                    ((text_len + dict_len + cls.__getattribute__('struct_size') + 7) & ~7) != klog_len)):
            return 'alignment error'
        if klog_len > 1024:
            return 'message too long'
        prefix = '<%d>' % ((fac << 3) | level)
        return prefix + str_time

print '--------------------------------start kernel log parsing-------------------------------------'
def find_klog_raw_file():
    for root, dirs, files in os.walk(os.getcwd()):
        for f in files:
            if f.startswith("SYS_KERNEL_LOG_RAW_"):
                return f

f_raw_str = find_klog_raw_file()
f_klog_raw = open(f_raw_str, 'rb')
f_klog_text = open("SYS_KERNEL_LOG", 'w+')
start = offset =  int(f_raw_str[19:])
end = os.path.getsize(f_raw_str)
is_wrapper = 0
print 'SYS_KERNEL_LOG_RAW: start at %d, end at %d' % (offset, end)
if offset > end:
    print 'offset is invalid'
    start = offset = 0
while 1:
    prefixdict = {}
    f_klog_raw.seek(offset, 0)
    kheader = klog_header.from_file(f_klog_raw)
    for format, fieldname in klog_header._fields_:
        if hasattr(kheader, fieldname):
            dict = {fieldname:kheader.__getattribute__(fieldname)}
            prefixdict.update(dict)
    #print prefixdict
    klog_len = kheader.__getattribute__('len')
    text_len = kheader.__getattribute__('text_len')

    if klog_len == 0 and is_wrapper == 0:
        is_wrapper = 1
        offset = 0
        continue

    if is_wrapper == 1 and offset >= start:
        break

    prefix = klog_header.parsing_klog_header(kheader,prefixdict)
    if (prefix == 'alignment error') or (prefix == 'message too long'):
        #print 'receive an alignment error'
        offset += 4
        continue

    msg = f_klog_raw.read(text_len).strip('\0') + '\n'
    kmesg =  '%s%s' % (prefix,msg)
    f_klog_text.write(kmesg)
    f_klog_raw.seek(klog_len - kheader.__getattribute__('struct_size') - text_len, 1)
    offset = f_klog_raw.tell()
f_klog_raw.close()
f_klog_text.close()
print '--------------------------------end kernel log parsing-------------------------------------'