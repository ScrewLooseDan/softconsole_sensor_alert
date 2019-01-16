import config
import subprocess
import alerttasks
from logsupport import ConsoleDetail, ConsoleWarning, ConsoleInfo, ConsoleDebug 
import logsupport
from stores import valuestore
import smbus
import time   

class SetDim(object):

    def __init__(self):
        pass

    @staticmethod 
    def SensorOut(self):
        var = "System:DimLevel"
        try:
            bus = smbus.SMBus(1)
        except:
            logsupport.Logs.Log("Error when attempting to write to light sensor, is it attached?", severity=ConsoleWarning)
            return
        '''
        # For VCN4010
        bus.write_byte_data(0x13, 0x80, 0x2F)
        bus.write_byte_data(0x13, 0x84, 0x9D)
        '''
        # For TLS2561
        # Turn on sensor
        bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
        # sets timing register, 402ms (which is default, not sure it's needed)
        bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)
        # give sensor time for reading
        time.sleep(0.5)
        '''
        data = bus.read_i2c_block_data(0x13, 0x85, 2) # For VCN4010
        luminance = data[0] * 256 + data[1] 
        lumStr = str(luminance)
        if luminance < 4:
            valuestore.SetVal(var, 5)
            logsupport.Logs.Log("luminance under 4: " + lumStr, severity=ConsoleDebug)
        elif luminance < 10:
            valuestore.SetVal(var, 10)
            logsupport.Logs.Log("luminance under 10: " + lumStr, severity=ConsoleDebug)
        else:
            valuestore.SetVal(var, 25)
            logsupport.Logs.Log("luminance: " + lumStr, severity=ConsoleDebug)
        '''
        # Retrieves data
        data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
        data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)
        # This calculates visible lux (subtracts IR only from total)
        vislux = (data[1] * 256 + data[0]) - (data1[1] * 256 + data1[0])
        visluxStr = str(vislux)
        if vislux < 4:
           valuestore.SetVal(var, 5)
           logsupport.Logs.Log("lux under 4: " + visluxStr, severity=ConsoleDebug)
        elif vislux < 10:
            valuestore.SetVal(var, 10)
            logsupport.Logs.Log("lux under 10: " + visluxStr, severity=ConsoleDebug)
        else:
            valuestore.SetVal(var, 10)
            logsupport.Logs.Log("lux: " + visluxStr, severity=ConsoleDebug)
        # turns off sensor
        bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)




alerttasks.alertprocs["SetDim"] = SetDim
