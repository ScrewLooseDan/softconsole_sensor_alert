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
        bus = smbus.SMBus(1)
        bus.write_byte_data(0x13, 0x80, 0x2F)
        bus.write_byte_data(0x13, 0x84, 0x9D)
        time.sleep(0.8)
        data = bus.read_i2c_block_data(0x13, 0x85, 2)
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

alerttasks.alertprocs["SetDim"] = SetDim
