import ctypes
from enum import Enum
import time
import os


class OPTErrorCode(Enum):
    OPT_SUCCEED = 0                                  #Operation succeed
    OPT_ERR_INVALIDHANDLE = 3001001                  #Invalid handle
    OPT_ERR_UNKNOWN = 3001002                        #Error unknown 
    OPT_ERR_INITSERIAL_FAILED = 3001003              #Failed to initialize a serial port
    OPT_ERR_RELEASESERIALPORT_FAILED = 3001004       #Failed to release a serial port
    OPT_ERR_SERIALPORT_UNOPENED = 3001005            #Attempt to access an unopened serial port
    OPT_ERR_CREATEETHECON_FAILED = 3001006           #Failed to create an Ethernet connection
    OPT_ERR_DESTROYETHECON_FAILED = 3001007          #Failed to destroy an Ethernet connection
    OPT_ERR_SN_NOTFOUND = 3001008                    #SN is not found
    OPT_ERR_TURNONCH_FAILED = 3001009                #Failed to turn on the specified channel(s)
    OPT_ERR_TURNOFFCH_FAILED = 3001019               #Failed to turn off the specified channel(s)
    OPT_ERR_SET_INTENSITY_FAILED = 3001011           #Failed to set the intensity for the specified channel(s)
    OPT_ERR_READ_INTENSITY_FAILED = 3001012          #Failed to read the intensity for the specified channel(s)	
    OPT_ERR_SET_TRIGGERWIDTH_FAILED = 3001013        #Failed to set trigger pulse width	
    OPT_ERR_READ_TRIGGERWIDTH_FAILED = 3001014       #Failed to read trigger pulse width
    OPT_ERR_READ_HBTRIGGERWIDTH_FAILED = 3001015     #Failed to read high brightness trigger pulse width
    OPT_ERR_SET_HBTRIGGERWIDTH_FAILED = 3001016      #Failed to set high brightness trigger pulse width
    OPT_ERR_READ_SN_FAILED = 3001017                 #Failed to read serial number
    OPT_ERR_READ_IPCONFIG_FAILED = 3001018           #Failed to read IP address
    OPT_ERR_CHINDEX_OUTRANGE = 3001019               #Index(es) out of the range
    OPT_ERR_WRITE_FAILED = 3001020                   #Failed to write data
    OPT_ERR_PARAM_OUTRANGE = 3001021                 #Parameter(s) out of the range 
    OPT_ERR_READ_MAC_FAILED = 3001022 #failed to read MAC
    OPT_ERR_SET_MAXCURRENT_FAILED = 3001023   #Failed to set max current
    OPT_ERR_READ_MAXCURRENT_FAILED = 3001024  #Failed to read max current
    OPT_ERR_SET_TRIGGERACTIVATION_FAILED = 3001025   #Failed to set trigger activation
    OPT_ERR_READ_TRIGGERACTIVATION_FAILED = 3001026  #Failed to read trigger activation
    OPT_ERR_SET_WORKMODE_FAILED = 3001027    #Failed to set work mode
    OPT_ERR_READ_WORKMODE_FAILED = 3001028  #Failed to read work mode
    OPT_ERR_SET_BAUDRATE_FAILED = 3001029   #Failed to set baud rate
    OPT_ERR_SET_CHANNELAMOUNT_FAILED = 3001030    #Failed to set channel amount
    OPT_ERR_SET_DETECTEDMINLOAD_FAILED = 3001031   #Failed to set detected min load
    OPT_ERR_READ_OUTERTRIGGERFREQUENCYUPPERBOUND_FAILED = 3001032   #Failed to read outer trigger frequency upper bound
    OPT_ERR_SET_AUTOSTROBEFREQUENCY_FAILED = 3001033  #Failed to set auto-strobe frequency
    OPT_ERR_READ_AUTOSTROBEFREQUENCY_FAILED = 3001034    #Failed to read auto-strobe frequency
    OPT_ERR_SET_DHCP_FAILED = 3001035        #Failed to set DHCP
    OPT_ERR_SET_LOADMODE_FAILED = 3001036   #Failed to set load mode
    OPT_ERR_READ_PROPERTY_FAILED = 3001037  #Failed to read property
    OPT_ERR_CONNECTION_RESET_FAILED = 3001038   #Failed to reset connection
    OPT_ERR_SET_HEARTBEAT_FAILED = 3001039    #Failed to set ethe connection heartbeat
    OPT_ERR_GETCONTROLLERLIST_FAILED = 3001040    #Failed to get controler(s) list           
    OPT_ERR_SOFTWARETRIGGER_FAILED = 3001041     #Failed to software trigger                
    OPT_ERR_GET_CHANNELSTATE_FAILED = 3001042    #Failed to get channelstate          
    OPT_ERR_SET_KEEPALIVEPARAMETERS_FAILED = 3001043    #Failed to set keepalvie parameters          
    OPT_ERR_ENABLE_KEEPALIVE_FAILED = 3001044    #Failed to enable/disable keepalive
    OPT_ERR_READSTEPCOUNT_FAILED = 3001045   #Failed to read step count           
    OPT_ERR_SETTRIGGERMODE_FAILED = 3001046   #Failed to set trigger mode    
    OPT_ERR_READTRIGGERMODE_FAILED = 3001047    #Failed to read trigger mode      
    OPT_ERR_SETCURRENTSTEPINDEX_FAILED = 3001048    #Failed to set current step index          
    OPT_ERR_READCURRENTSTEPINDEX_FAILED = 3001049    #Failed to read current step index          
    OPT_ERR_RESETSEQFAILED = 3001050   #Failed to reset SEQ
    OPT_ERR_SETTRIGGERDELAY_FAILED = 3001051     #Failed to set trigger delay
    OPT_ERR_GET_TRIGGERDELAY_FAILED = 3001052     #Failed to get trigger delay
    OPT_ERR_SETMULTITRIGGERDELAY_FAILED = 3001053     #Failed to set multiple channels trigger delay
    OPT_ERR_SETSEQTABLEDATA_FAILED = 3001054     #Failed to set SEQ table data
    OPT_ERR_READSEQTABLEDATA_FAILED = 3001055     #Failed to Read SEQ table data
    OPT_ERR_READ_CHANNELS_FAILED = 3001056     #Failed to read controller#s channel
    OPT_ERR_READ_KEEPALIVE_STATE_FAILED = 3001057     #Failed to read the state of keepalive
    OPT_ERR_READ_KEEPALIVE_CONTINUOUS_TIME_FAILED = 3001058     #Failed to read the continuous time of keepalive
    OPT_ERR_READ_DELIVERY_TIMES_FAILED = 3001059     #Failed to read the delivery times of prop packet
    OPT_ERR_READ_INTERVAL_TIME_FAILED = 3001060     #Failed to read the interval time of prop packet
    OPT_ERR_READ_OUTPUTBOARD_VISION_FAILED = 3001061     #Failed to read the vision of output board
    OPT_ERR_READ_DETECT_MODE_FAILED = 3001062     #Failed to read detect mode of load
    OPT_ERR_SET_BOOT_STATE_MODE_FAILED = 3001063     #Failed to set mode of boot state
    OPT_ERR_READ_MODEL_BOOT_MODE_FAILED = 3001064     #Failed to read the specified channel boot state
    OPT_ERR_SET_OUTERTRIGGERFREQUENCYUPPERBOUND_FAILED = 3001065   #Failed to set outer trigger frequency upper bound
    OPT_ERR_SET_IPCONFIG_FAILED = 3001066   #Failed to set IP configuration of the controller
    OPT_ERR_SET_VOLTAGE_FAILEDAs = 3001067   #Failed to set voltage value
    OPT_ERR_READ_VOLTAGE_FAILEDAs = 3001068   #Failed to read voltage value
    OPT_ERR_SET_TIMEUNIT_FAILED = 3001069  #Failed to set time unit
    OPT_ERR_READ_TIMEUNIT_FAILED = 3001070   #Failed to read time unit
    OPT_ERR_FILEEXT = 3001071     #File suffix name is wrong
    OPT_ERR_FILEPATH_EMPTY = 3001072     #File path is empty
    OPT_ERR_FILE_MAGIC_NUM = 3001073    #magic number is wrong
    OPT_ERR_FILE_CHECKSUM = 3001074    #Checksum is wrong
    OPT_ERR_SEQDATA_EQUAL =  3001075     #Current SEQ table data is different from load file data
    OPT_ERR_SET_HB_TIMEUNIT_FAILED =  3001076     #Failed to set highlight time unit
    OPT_ERR_READ_HB_TIMEUNIT_FAILED = 3001077     #Failed to read highlight time unit
    OPT_ERR_SET_TRIGGERDELAY_TIMEUNIT_FAILED = 3001078     #Failed to set trigger delay time unit
    OPT_ERR_READ_TRIGGERDELAY_TIMEUNIT_FAILED = 3001079     #Failed to read trigger delay time unit
    OPT_ERR_SET_PERCENT_FAILED  =  3001080     #Failed to set percent of brightening current
    OPT_ERR_SET_HB_TRIGGER_OUTPUT_DUTY_RATIO_FAILED  = 3001084    #Failed to set high light trigger output duty limit ratio
    OPT_ERR_READ_PERCENT_FAILED  = 3001081     #Failed to read percent of brightening current
    OPT_ERR_SET_DIFF_PRESURE_LIMIT_STATE_FAILED  = 3001086     #Failed to set differential pressure limit function switch status
    OPT_ERR_SET_HB_LIMIT_STATE_FAILED  =  3001082    #Failed to set high light trigger output duty limit switch state
    OPT_ERR_READ_HB_LIMIT_STATE_FAILED  = 3001083     #Failed to read high light trigger output duty limit switch state
    OPT_ERR_READ_HB_TRIGGER_OUTPUT_DUTY_RATIO_FAILED   =  3001085     #Failed to read high light trigger output duty limit ratio

class IntensityItem(ctypes.Structure):
    _fields_ = [
        ("channelIndex", ctypes.c_int32),
        ("intensity", ctypes.c_int32)]

class OPTController:
    def __init__(self, dll_type='x64'):
        self.dllType = dll_type
        curFolder = os.path.split(__file__)[0]
        dllPath = os.path.join(curFolder,'OPTControllerSDK', f'{dll_type}','OPTController.dll' )
        self.dll = ctypes.cdll.LoadLibrary(dllPath)
        if dll_type == 'x64':
            self.handle = ctypes.c_longlong(0)
        else:
            self.handle = ctypes.c_int32(0)
    
    def findError(self, resp):
        return OPTErrorCode(resp).value, OPTErrorCode(resp).name
    
    def open(self, ip='192.168.1.16'):
        resp = self.dll.OPTController_CreateEthernetConnectionByIP(f'{ip}'.encode('utf-8'), ctypes.byref(self.handle))
        return self.findError(resp)
    
    def close(self):
        resp = self.dll.OPTController_DestroyEthernetConnection(self.handle)
        return self.findError(resp)

    def readSN(self):
        sn = ctypes.create_string_buffer(1024)
        resp = self.dll.OPTController_ReadSN(self.handle, ctypes.byref(sn))
        if resp == 0:
            return sn.value.decode('utf-8')
        else:
            return None

    def readIPConfig(self):
        ip = ctypes.create_string_buffer(1024)
        subnetMask = ctypes.create_string_buffer(1024)
        defaultGateway = ctypes.create_string_buffer(1024)
        resp = self.dll.OPTController_ReadIPConfig(self.handle, ctypes.byref(ip), ctypes.byref(subnetMask), ctypes.byref(defaultGateway))
        if resp == 0:
            return (ip.value.decode('utf-8'), subnetMask.value.decode('utf-8'), defaultGateway.value.decode('utf-8'))
        else:
            return None

    def turnOnChannel(self, channelIndex=0):
        resp = self.dll.OPTController_TurnOnChannel(self.handle, ctypes.c_int32(channelIndex))
        return self.findError(resp)
    
    def turnOffChannel(self, channelIndex=0):
        resp = self.dll.OPTController_TurnOffChannel(self.handle, ctypes.c_int32(channelIndex))
        return self.findError(resp)

    def turnOnMultiChannel(self, channelIndexes=[0]):
        length = len(channelIndexes)
        channels = (ctypes.c_int32 * length)(*channelIndexes)
        resp = self.dll.OPTController_TurnOnMultiChannel(self.handle, channels, ctypes.c_int32(length))
        return self.findError(resp)
    
    def turnOffMultiChannel(self, channelIndexes=[0]):
        length = len(channelIndexes)
        channels = (ctypes.c_int32 * length)(*channelIndexes)
        resp = self.dll.OPTController_TurnOffMultiChannel(self.handle, channels, ctypes.c_int32(length))
        return self.findError(resp)
    
    def setIntensity(self, channelIndex=0, intensity=0):
        intensity = 0 if intensity < 0 else 255 if intensity > 255 else intensity
        resp = self.dll.OPTController_SetIntensity(self.handle, ctypes.c_int32(channelIndex), ctypes.c_int32(intensity))
        return self.findError(resp)
    
    def setMultiIntensity(self, intensityArray=[0]):
        length = len(intensityArray)
        filterIntensityArray = []
        for ch, intensity in enumerate(intensityArray):
            filterIntsity = 0 if intensity < 0 else 255 if intensity > 255 else intensity
            filterIntensityArray.append((ch+1, filterIntsity))
        inteArr = (IntensityItem * length)(*filterIntensityArray)
        resp = self.dll.OPTController_SetMultiIntensity(self.handle, inteArr, ctypes.c_int32(length))
        return self.findError(resp)
    
    def readIntensity(self, channelIndex=0):
        intensity = ctypes.c_int32(0)
        resp = self.dll.OPTController_ReadIntensity(self.handle, ctypes.c_int32(channelIndex), ctypes.byref(intensity))
        return intensity.value

def test():
    opt = OPTController()
    resp = opt.open('192.168.1.16')
    sn = opt.readSN()
    print(sn)
    ipconfig = opt.readIPConfig()
    print(ipconfig)

    resp = opt.turnOnMultiChannel([1,2,3,4])
    print(resp)
    resp = opt.setMultiIntensity([0,0,0,0])
    print(resp)
    for i in range(100):
        resp = opt.setMultiIntensity([i,i,i,i])
        # print(f"intensity {i}, resp {resp}")
        intensity = opt.readIntensity(1)
        print(f"intensity of ch1 is {intensity}")
        time.sleep(0.01)
    resp = opt.turnOffMultiChannel([1,2,3,4])
    print(resp)
    resp = opt.close()


if __name__ == '__main__':
    test()
        
