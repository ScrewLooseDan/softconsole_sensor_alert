import config
import subprocess
import alerttasks
from logsupport import ConsoleDetail, ConsoleWarning, ConsoleInfo, ConsoleDebug 
import logsupport
from stores import valuestore
import smbus
import time   

'''
alert.param[0] = DimLevel low/no light
alert.param[1] = DimLevel medium light
alert.param[2] = DimLevel high light
alert.param[3] = BrightLevel low/no light
alert.param[4] = BrightLevel medium light
alert.param[5] = DiBrightLevel high light
'''

class SetDim(object):

    def __init__(self):
        pass

    @staticmethod 
    def SensorOut(alert):
        varDim = "System:DimLevel"
        varBright = "System:BrightLevel"
        try:
            bus = smbus.SMBus(1)
        except:
            logsupport.Logs.Log("Error: Issue with i2c, is it enabled?", severity=ConsoleWarning)
            raise
        # Turn on sensor
        try:
            bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
        except:
            logsupport.Logs.Log("Error: Unable to write to light sensor.", severity=ConsoleWarning)
            return
        # sets timing register, 402ms (which is default, not sure it's needed)
        bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)
        # give sensor time for reading
        time.sleep(0.5)        
        # Retrieves data
        data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
        data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)
        # This calculates visible lux (subtracts IR only from total)
        vislux = (data[1] * 256 + data[0]) - (data1[1] * 256 + data1[0])
        visluxStr = str(vislux)
        if vislux < 4:
            valuestore.SetVal(varDim, alert.param[0])
            valuestore.SetVal(varBright, alert.param[3])
            logsupport.Logs.Log("lux under 4: " + visluxStr, severity=ConsoleDebug)
        elif vislux < 15:
            valuestore.SetVal(varDim, alert.param[1])
            valuestore.SetVal(varBright, alert.param[4])
            logsupport.Logs.Log("lux under 10: " + visluxStr, severity=ConsoleDebug)
        else:
            valuestore.SetVal(varDim, alert.param[2])
            valuestore.SetVal(varBright, alert.param[5])
            logsupport.Logs.Log("lux: " + visluxStr, severity=ConsoleDebug)
        # turns off sensor
        bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
        bus.close()

alerttasks.alertprocs["SetDim"] = SetDim
