import espRFToolUIEN
from PyQt4 import QtCore, QtGui
import threading
import os
import sys
import time
import serial  
import serial.tools.list_ports 
import esptool

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
    
    
class write_flash_param(object):
    flash_freq = '40m'  #para_dict['FLASH_FREQ']
    flash_mode = 'qio'  #para_dict['FLASH_MODE']
    flash_size = '4MB'  #para_dict['FLASH_SIZE']
    addr_filename = ''  #{(0x0, self.filename)}
    filename = ''
    
    
class esp_dev_param(object):
    chip_type = 'ESP32' #para_dict['CHIP_TYPE']
    port = ''
    port_baud = 115200
    compress = False
    no_compress = True
    no_stub = False
    verify = False
    esp_download_mode = 1 # 1:ram, 2:flash

def startRFTest(esprftool, ser):
    while 1:
        try:
            rl = ser.readline()
        except:
            return
        if len(rl) > 0:
            esprftool._SignalTX.emit(rl)
    
    
class esp_param(write_flash_param, esp_dev_param):
    def __init__(self):
        pass
    
    
def load_ram(esp, args, esprftool):
    esprftool._SignalTX.emit('load begin')
    if(esp.CHIP_NAME == 'ESP32'):
        image = esptool.LoadFirmwareImage("esp32", args.filename)
    else:
        image = esptool.LoadFirmwareImage("esp8266", args.filename)
        
    image_size = os.path.getsize(args.filename)
    send_size = 0
    
    #print('RAM boot...')
    for seg in image.segments:
        offset = seg.addr
        data = seg.data
        size = seg.file_offs
        
        sys.stdout.flush()
        esp.mem_begin(size, esptool.div_roundup(size, esp.ESP_RAM_BLOCK), esp.ESP_RAM_BLOCK, offset)

        seq = 0
        while len(data) > 0:
            esp.mem_block(data[0:esp.ESP_RAM_BLOCK], seq)
            data = data[esp.ESP_RAM_BLOCK:]
            seq += 1
            if len(data) < esp.ESP_RAM_BLOCK:
                send_size += len(data)
            else:
                send_size += esp.ESP_RAM_BLOCK
            esprftool._Signalprb.emit(100 * send_size // image_size)
        #print('done!')

    print('All segments done, executing at %08x' % image.entrypoint)
    try:
        esp.mem_finish(image.entrypoint)
    except:
        #print "error but ignore"
        pass
    esprftool._SignalTX.emit('load bin success')
    esp._port.close()
    esprftool._Signalprb.emit(100)
    


def write_flash(esp, args, esprftool):
    flash_params = esptool._get_flash_params(esp, args)
    esprftool._SignalTX.emit('load start')

    # set args.compress based on default behaviour:
    # -> if either --compress or --no-compress is set, honour that
    # -> otherwise, set --compress unless --no-stub is set
    if args.compress is None and not args.no_compress:
        args.compress = not args.no_stub

    # verify file sizes fit in flash
    flash_end = esptool.flash_size_bytes(args.flash_size)
    for address, argfile in args.addr_filename:
        argfile.seek(0,2)  # seek to end
        if address + argfile.tell() > flash_end:
            raise FatalError(("File %s (length %d) at offset %d will not fit in %d bytes of flash. " +
                             "Use --flash-size argument, or change flashing address.")
                             % (argfile.name, argfile.tell(), address, flash_end))
        argfile.seek(0)

    for address, argfile in args.addr_filename:
        if esp.CHIP_NAME == "ESP32":
            address = 0x1000

        if args.no_stub:
            print('Erasing flash...')
            esprftool._SignalTX.emit('Erasing flash...')
        image = esptool.pad_to(argfile.read(), 4)
        image = esptool._update_image_flash_params(esp, address, flash_params, image)
        import hashlib
        calcmd5 = hashlib.md5(image).hexdigest()
        uncsize = len(image)
        if args.compress:
            uncimage = image
            image = zlib.compress(uncimage, 9)
            blocks = esp.flash_defl_begin(uncsize, len(image), address)
        else:
            blocks = esp.flash_begin(uncsize, address)
        argfile.seek(0)  # in case we need it again
        seq = 0
        written = 0
        while len(image) > 0:
            esprftool._Signalprb.emit(100 * (seq + 1) // blocks)
            #print '\rWriting at 0x%08x... (%d %%)' % (address + seq * esp.FLASH_WRITE_SIZE, 100 * (seq + 1) // blocks)
            sys.stdout.flush()
            block = image[0:esp.FLASH_WRITE_SIZE]
            if args.compress:
                esp.flash_defl_block(block, seq)
            else:
                # Pad the last block
                block = block + b'\xff' * (esp.FLASH_WRITE_SIZE - len(block))
                esp.flash_block(block, seq)
            image = image[esp.FLASH_WRITE_SIZE:]
            seq += 1
            written += len(block)
        speed_msg = ""

        try:
            res = esp.flash_md5sum(address, uncsize)
            if res != calcmd5:
                print('File  md5: %s' % calcmd5)
                print('Flash md5: %s' % res)
                print('MD5 of 0xFF is %s' % (hashlib.md5(b'\xFF' * uncsize).hexdigest()))
                raise FatalError("MD5 of file does not match data in flash!")
            else:
                print('Hash of data verified.')
                esprftool._SignalTX.emit('Hash of data verified.')
        except NotImplementedInROMError:
            pass
    print('\nLeaving...')
    esprftool._SignalTX.emit('load to flash success')

    if esp.IS_STUB:
        # skip sending flash_finish to ROM loader here,
        # as it causes the loader to exit and run user code
        esp.flash_begin(0, 0)
        if args.compress:
            esp.flash_defl_finish(False)
        else:
            esp.flash_finish(False)

    if args.verify:
        print('Verifying just-written flash...')
        print('(This option is deprecated, flash contents are now always read back after flashing.)')
        _verify_flash(esp, args)

    esprftool._SignalTX.emit('load bin success')
    esp._port.close()
    esprftool._Signalprb.emit(100)
    

def t_loadBin(esprftool, params):
    initial_baud = 115200
    esprftool._SignalTX.emit('sync...')
    esprftool._SignalLoadStatus.emit(4)
    if(params.chip_type == 'ESP32'):
        try:
            esp = esptool.ESP32ROM(params.port, initial_baud)
        except:
            print "ERROR!! The com port is occupied!!\n"
            esprftool._SignalTX.emit('ERROR!! The com port is occupied!!')
            return
                
    elif(params.chip_type == 'ESP8266'):
        try:
            esp = esptool.ESP8266ROM(params.port, initial_baud)
        except:
            print "ERROR!! The com port is occupied!!\n"
            esprftool._SignalTX.emit('ERROR!! The com port is occupied!!')
            return
    
    esprftool._SignalLoadStatus.emit(1)
    esp_mac = (00, 00, 00, 00, 00, 00)
    cus_mac = "00:00:00:00:00:00"
    print('%s: %s' % ("ESP_MAC", ':'.join(map(lambda x: '%02x' % x, esp_mac))))
    esprftool._SignalLoadStatus.emit(1)
    while True:
        try:
            esp.connect()
            break
        except:
            pass
    try:
        esprftool._SignalTX.emit('sync success')
        esp_mac = esp.read_mac()
        print 'esp_mac:%02x-%02x-%02x-%02x-%02x-%02x' %(esp_mac)
        esprftool._SignalTX.emit('esp_mac:%02x-%02x-%02x-%02x-%02x-%02x' %(esp_mac))
        esprftool._SignalLoadStatus.emit(2)
    
        if(params.esp_download_mode == 1):        
            #print "load ram ..."
            if load_ram(esp, params, esprftool) == 1:
                esprftool._SignalStart.emit()
            
        elif(params.esp_download_mode == 2):
            if not params.no_stub:
                esp = esp.run_stub()    
            esp.change_baud(921600)        
            #print "load flash ..." 
            write_flash(esp, params, esprftool)
    except:
        esprftool._SignalLoadStatus.emit(4)
        esprftool._SignalTX.emit('load bin fail')
        return 
    
    esprftool._SignalLoadStatus.emit(3)
    

class WFParams(object):
    WFTestMode = {'TX continues':'0', 'TX packet':'1', 'RX packet':'2', 'TX tone':'3'}
    WFChannel = ()
    WFBandWidth = {'20M':'0', '40M':'1'}
    WFDataRate = {'11b 1M':'0x00', '11b 2M':'0x01', '11b 5.5M':'0x02', '11b 11M':'0x03', '11g 6M':'0x0b',
                  '11g 9M':'0x0f', '11g 12M':'0x0a', '11g 18M':'0x0e', '11g 24M':'0x09', '11g 36M':'0x0d',
                  '11g 48M':'0x08', '11g 54M':'0x0c', '11n MCS0':'0x10', '11n MCS1':'0x11','11n MCS2':'0x12',
                  '11n MCS3':'0x13','11n MCS4':'0x14','11n MCS5':'0x15','11n MCS6':'0x16','11n MCS7':'0x17'}
    WFAtten = 0

class BTParams(object):
    BTTestMode = {'classBT TX':'0', 'classBT RX/BR':'1', 'class BT/EDR':'2', 'BLE TX':'3', 
                  'BLE TX Syncw':'4', 'BLE RX':'5', 'BT TX tone':'6'}
    BTpowerLevel = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    BTChannel = ()
    BLEChannel = ()
    BTDataRateType={'1M_DH1_1010':'1 1 0', '1M_DH1_00001111':'1 1 1', '1M_DH1_prbs9':'1 1 2', '1M_DH3_1010':'1 3 0', 
                    '1M_DH3_00001111':'1 3 1', '1M_DH3_prbs9':'1 3 2', '1M_DH5_1010':'1 5 0','1M_DH5_00001111':'1 5 1', 
                    '1M_DH5_prbs9':'1 5 2', '2M_DH1_1010':'2 1 0', '2M_DH1_00001111':'2 1 1', '2M_DH1_prbs9':'2 1 2', 
                    '2M_DH3_1010':'2 3 0', '2M_DH3_00001111':'2 3 1', '2M_DH3_prbs9':'2 3 2', '2M_DH5_1010':'2 5 0', 
                    '2M_DH5_00001111':'2 5 1', '2M_DH5_prbs9':'2 5 2', '3M_DH1_1010':'3 1 0', '3M_DH1_00001111':'3 1 1', 
                    '3M_DH1_prbs9':'3 1 2', '3M_DH3_1010':'3 3 0', '3M_DH3_00001111':'3 3 1', '3M_DH3_prbs9':'3 3 2', 
                    '3M_DH5_1010':'3 5 0', '3M_DH5_00001111':'3 5 1', '3M_DH5_prbs9':'3 5 2'}
    BLEDataRateType={'LE_1010':'0', 'LE_00001111':'1', 'LE_prbs9':'2'}
    BTChanJmp = {'no':'0', 'yes':'1'}
    BLEPayload = 0
    BLESyncw = {'0x0':'0', '0x71764129':'1', 'custom':'2'}

class CmdParams(WFParams, BTParams):
    def __init(self):
        pass

class myComboBox(QtGui.QComboBox):
    clicked = QtCore.pyqtSignal()
    def mousePressEvent(self, event):
        """ QComboBox.mousePressEvent(QMouseEvent) """
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()
    

class Ui_EspRFTool(espRFToolUIEN.Ui_EspRFtestTool, QtGui.QWidget):
    _SignalTX = QtCore.pyqtSignal(str)
    _Signalprb = QtCore.pyqtSignal(int)
    _SignalStart = QtCore.pyqtSignal()
    _SignalLoadStatus = QtCore.pyqtSignal(int)  # 0:idle, 1:syncing..., 2:loading..., 3:success, 4:fail
    _SignalCycleTiming = QtCore.pyqtSignal(str)
    _port_state = 0 # 0:closed, 1:opened
    _checkBok_selected = 0
    rbSend_group = QtGui.QButtonGroup()
    leSend_group = {}
    cmdParams = CmdParams()
    _WFStatus = 0 # use for WiFi tone
    _BTstatus = 0 # use for BT tone
    _ulap = 0x6bc6967e
    _ltaddr = 0x0
    _timeFlag = False
    _showSend = True
    _addCRFlag = False
    _cycleFlag = False
    _cycSendFlg = False
    _TestType = 0 # 0:cmd hander with wifi, 1:use cmd hander with esp

    #cycTimer=threading.Timer(1.0, )
    def __init__(self, EspRFtestTool, configParams, parent=None):
        super(QtGui.QWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.addMyUI(self)
        self.setupSignal(self)
        self.twTestPanel.setEnabled(False)
        self.paramInit(configParams)
    
    def closeEvent(self, event):
        try:
            self._ser.close()
            print 'com port close'
        except:
            print 'com port not open'
        self.saveParams()
        print 'bye bye'
        os._exit(0)
        
    def addMyUI(self, EspRFtestTool):
        self.cbComIndex = myComboBox(EspRFtestTool)
        self.cbComIndex.setGeometry(QtCore.QRect(208, 9, 101, 21))
        self.cbComIndex.setObjectName(_fromUtf8("cbComIndex"))
        self.cbComIndex.addItem(_fromUtf8(""))
        self.cbComIndex.setItemText(0, _translate("EspRFtestTool", "--", None))        
        
    def setupSignal(self, EspRFtestTool):
        QtCore.QObject.connect(self.pbOpenSerial, QtCore.SIGNAL(_fromUtf8("clicked()")), self._startRFTest)
        QtCore.QObject.connect(self.cbComIndex, QtCore.SIGNAL(_fromUtf8("clicked()")), self.cbUpdate)
        QtCore.QObject.connect(self.pbLoadBin, QtCore.SIGNAL(_fromUtf8("clicked()")), self.loadBin)
        QtCore.QObject.connect(self.pbOpenFile, QtCore.SIGNAL(_fromUtf8("clicked()")), self.showFileDialog)
        QtCore.QObject.connect(self.pbSend, QtCore.SIGNAL(_fromUtf8("clicked()")), self.manuCmdSend)
        QtCore.QObject.connect(self.cbBTTestMode, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.btCmdUpdate)
        QtCore.QObject.connect(self.cbWFTestMode, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.wfCmdUpdate)
        QtCore.QObject.connect(self.cbBTSyncw, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.btSyncw)
        QtCore.QObject.connect(self.cbComBaud, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.comBaud)
        QtCore.QObject.connect(self.cbWFDataRate, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.wfCmdUpdate)
        QtCore.QObject.connect(self.cbWFBandWidth, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.wfBWUpdate)
        QtCore.QObject.connect(self.pbBTSend, QtCore.SIGNAL(_fromUtf8("clicked()")), self.btCmdSend)
        QtCore.QObject.connect(self.pbWFSend, QtCore.SIGNAL(_fromUtf8("clicked()")), self.wfCmdSend)
        QtCore.QObject.connect(self.pbBTStop, QtCore.SIGNAL(_fromUtf8("clicked()")), self.cmdStop)
        QtCore.QObject.connect(self.pbWFStop, QtCore.SIGNAL(_fromUtf8("clicked()")), self.cmdStop)
        QtCore.QObject.connect(self.cbChipType, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.chipChg)
        QtCore.QObject.connect(self.pbLogClear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.logClear)
        QtCore.QObject.connect(self.pbLogSave, QtCore.SIGNAL(_fromUtf8("clicked()")), self.saveFileDialog)
        QtCore.QObject.connect(self.ckbTimeFlag, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.showFlag)
        QtCore.QObject.connect(self.ckbShowSend, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.showFlag)
        QtCore.QObject.connect(self.ckbAddCR, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.showFlag)
        QtCore.QObject.connect(self.ckbCycleFlag, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.showFlag)
        self._SignalTX.connect(self.printLog)
        self._Signalprb.connect(self.prbUpdate)
        self._SignalStart.connect(self._startRFTest)
        self._SignalLoadStatus.connect(self.loadStatus)
        self._SignalCycleTiming.connect(self.cycSend)
        QtCore.QMetaObject.connectSlotsByName(EspRFtestTool)
        self.rbSend1.setChecked(True)
        
        for chd in self.gbSend.children():
            if type(chd) == QtGui.QRadioButton:
                #chd.clicked.connect(lambda:self.radiobtnChg(chd))
                self.rbSend_group.addButton(chd, int(chd.objectName()[6:]))
            elif type(chd) == QtGui.QLineEdit:
                try:
                    self.leSend_group[int(chd.objectName()[6:])] = chd
                except:
                    pass
    
    def chipChg(self):
        if str(self.cbChipType.currentText()).find('8266') >= 0:
            self.twTestPanel.setCurrentIndex(1)
            self.twTestPanel.currentWidget().setEnabled(False)
            self.twTestPanel.setCurrentIndex(0)
        elif str(self.cbChipType.currentText()).find('32') >= 0:
            self.twTestPanel.setCurrentIndex(1)
            self.twTestPanel.currentWidget().setEnabled(True)
            self.twTestPanel.setCurrentIndex(0)
        self.wfCmdUpdate()
        self.btCmdUpdate()
    
    def loadStatus(self, status):
        self.leStatus.setAutoFillBackground(True)
        p=self.leStatus.palette()
        if status == 0:
            self.leStatus.setText(' IDLE')
        elif status == 1:
            p.setColor(QtGui.QPalette.Base,QtGui.QColor(0, 0, 255))
            p.setColor(QtGui.QPalette.Text,QtGui.QColor(255, 255, 0))
            self.leStatus.setText('SYNC')
        elif status == 2:
            p.setColor(QtGui.QPalette.Base,QtGui.QColor(0, 255, 0))
            p.setColor(QtGui.QPalette.Text,QtGui.QColor(255, 0, 255))
            self.leStatus.setText('LOAD')
        elif status == 3:
            p.setColor(QtGui.QPalette.Base,QtGui.QColor(255, 255, 0))
            p.setColor(QtGui.QPalette.Text,QtGui.QColor(0, 0, 255))
            self.leStatus.setText('SUCC')
        elif status == 4:
            p.setColor(QtGui.QPalette.Base,QtGui.QColor(255, 0, 0))
            p.setColor(QtGui.QPalette.Text,QtGui.QColor(0, 255, 255))
            self.leStatus.setText(' FAIL')
        self.leStatus.setPalette(p)
    
    def paramInit(self, configParams):
        self._TestType = int(configParams['common_conf']['Test_Type'])
        self.loadSave(configParams)
        self.twTestPanel.setEnabled(False)
        self.twTestPanel.setCurrentIndex(0)
        self.cbWFTestMode.setCurrentIndex(0)
        self.cbBTTestMode.setCurrentIndex(0)
        self.cbWFChannel.clear()
        self.leSyncw.setHidden(True)
        self.leCOM.setHidden(True)
        self.chipChg()
        
        self.twTestPanel.currentWidget
        for i in range(13):
            self.cbWFChannel.addItem(str(i+1)+'/'+str(2412+i*5))
        self.cbWFChannel.addItem('14/2484')
        
        self.wfCmdUpdate()
        self.btCmdUpdate()
        
        self.cbWFBandWidth.setCurrentIndex(0)
        self.cbWFChannel.setCurrentIndex(0)
        self.cbWFDataRate.setCurrentIndex(0)
        self.leWFAtten.setText('0')
        
        self.cbBTChannel.setCurrentIndex(0)
        self.cbBTChanJmp.setCurrentIndex(0)
        self.cbBTDataRate.setCurrentIndex(0)
        self.cbBTPowerLevel.setCurrentIndex(4)
        self.cbBTSyncw.setCurrentIndex(0)
        self.leBTPayload.setText('250')
        self.leBTPayload.setEnabled(False)

    
    def wfCmdUpdate(self):
        if str(self.cbChipType.currentText()).find('8266') >= 0 or str(self.cbWFDataRate.currentText()).find('11n') < 0:
            self.cbWFBandWidth.removeItem(1)
        else:
            if self.cbWFBandWidth.count() < 2:
                self.cbWFBandWidth.addItem('40M')

        if str(self.cbChipType.currentText()).find('RX') >= 0:
            self.leWFAtten.setEnabled(False)
        else:
            self.leWFAtten.setEnabled(True)

        if str(self.cbWFTestMode.currentText()).find('tone') >= 0:
            self.cbWFBandWidth.setEnabled(False)
            self.cbWFDataRate.setEnabled(False)
        else:
            self.cbWFBandWidth.setEnabled(True)
            self.cbWFDataRate.setEnabled(True)

        
    def wfBWUpdate(self):
        self.cbWFChannel.clear()
        if str(self.cbWFBandWidth.currentText()).find('40M') >= 0:
            for i in range(7):
                self.cbWFChannel.addItem(str(i+3)+'/'+str(2412+(i+3)*5))
        else:
            for i in range(13):
                self.cbWFChannel.addItem(str(i+1)+'/'+str(2412+i*5))
            self.cbWFChannel.addItem('14/2484')
    
    def btCmdUpdate(self):
        if str(self.cbBTTestMode.currentText()).find('BT') >= 0:
            self.cbBTChannel.clear()
            for i in range(79):
                self.cbBTChannel.addItem(str(i)+'/'+str(2402+i))
            self.leBTPayload.setEnabled(False)
            self.cbBTSyncw.setEnabled(False)
            self.cbBTPowerLevel.clear()
            for i in range(10):
                self.cbBTPowerLevel.addItem(str(i))

            if str(self.cbBTTestMode.currentText()).find('RX') >= 0:
                if self.cbBTDataRate.count() != 6:
                    self.cbBTDataRate.clear()
                    for it in sorted(self.cmdParams.BTDataRateType.items(), key=lambda item:item[1]):
                        if it[0].find('prbs9') >= 0 and it[0].find('DH5') < 0:
                            self.cbBTDataRate.addItem(it[0])
            elif self.cbBTDataRate.count() != 27:
                self.cbBTDataRate.clear()
                for it in sorted(self.cmdParams.BTDataRateType.items(), key=lambda item:item[1]):
                    self.cbBTDataRate.addItem(it[0])
                
        elif str(self.cbBTTestMode.currentText()).find('BLE') >= 0:
            self.cbBTChannel.clear()
            for i in range(11):
                self.cbBTChannel.addItem(str(i)+'/'+str(2404+i*2))
            for i in range(26):
                self.cbBTChannel.addItem(str(i+11)+'/'+str(2428+i*2))
            self.cbBTChannel.addItem(str(37)+'/2402')
            self.cbBTChannel.addItem(str(38)+'/2426')
            self.cbBTChannel.addItem(str(39)+'/2480')
            self.leBTPayload.setEnabled(False)
            self.cbBTSyncw.setEnabled(True)
            self.cbBTPowerLevel.clear()
            for i in range(9):
                self.cbBTPowerLevel.addItem(str(i))

            if str(self.cbBTTestMode.currentText()).find('RX') >= 0:
                if self.cbBTDataRate.count() != 1:
                    self.cbBTDataRate.clear()
                    self.cbBTDataRate.addItem('LE_prbs9')
            elif self.cbBTDataRate.count() != 3:
                self.cbBTDataRate.clear()
                for it in sorted(self.cmdParams.BLEDataRateType.items(), key=lambda item:item[1]):
                    self.cbBTDataRate.addItem(it[0])

        if str(self.cbBTTestMode.currentText()).find('tone') >= 0:
            self.lbBTPowerLevel.setText('Backoff:')
        else:
            self.lbBTPowerLevel.setText('Power Level:')

            
    def btSyncw(self):
        if str(self.cbBTSyncw.currentText()).find('custom') >= 0:
            self.leSyncw.setHidden(False)
        else:
            self.leSyncw.setHidden(True)
    
    def comBaud(self):
        if str(self.cbComBaud.currentText()).find('custom') >= 0:
            self.leCOM.setHidden(False)
        else:
            self.leCOM.setHidden(True)
    
    def wfCmdSend(self):            
        cmd = ''        
        channel = int(self.cbWFChannel.currentIndex()) + 1
        rate = self.cmdParams.WFDataRate[str(self.cbWFDataRate.currentText())]
        try:
            attenuation = int(str(self.leWFAtten.text()))
        except:
            self.printLog('attenuation is error(type)')
            return
        if attenuation > 255 or attenuation < 0:
            self.printLog('attenuation is error(value)')
            return
        
        if str(self.cbWFBandWidth.currentText()).find('40M') >= 0:
            self.cmdSend('tx_cbw40m_en 1\r')
        else:
            self.cmdSend('tx_cbw40m_en 0\r')
        
        if str(self.cbWFTestMode.currentText()).find('TX continues') >= 0:
            self.cmdSend('tx_contin_en 1\r')
            cmd = 'wifitxout ' + str(channel) + ' ' + rate + ' ' + str(attenuation)
            if self._TestType == 1:
                cmd = 'esp_tx ' + str(channel) + ' ' + rate + ' ' + str(attenuation)
        elif str(self.cbWFTestMode.currentText()).find('TX packet') >= 0:
            cmd = 'wifitxout ' + str(channel) + ' ' + rate + ' ' + str(attenuation)
            if self._TestType == 1:
                cmd = 'esp_tx ' + str(channel) + ' ' + rate + ' ' + str(attenuation)            
        elif str(self.cbWFTestMode.currentText()).find('RX packet') >= 0:
            cmd = 'esp_rx ' + str(channel) + ' ' + rate
        elif str(self.cbWFTestMode.currentText()).find('TX tone') >= 0:
            cmd = 'wifiscwout 1 ' + str(channel) + ' ' + str(attenuation)
        
        if not cmd.endswith('\r'):
            cmd = cmd+'\r'
        self.cmdSend(cmd)
    
    def btCmdSend(self):
        cmd = ''
        powerLevel = str(self.cbBTPowerLevel.currentText())
        chanJump = str(self.cbBTChanJmp.currentIndex())
        channel = self.cbBTChannel.currentIndex()
        dataRateType = ''
        if str(self.cbBTTestMode.currentText()).find('BT') >= 0:
            dataRateType = self.cmdParams.BTDataRateType[str(self.cbBTDataRate.currentText())]
        else:
            dataRateType = self.cmdParams.BLEDataRateType[str(self.cbBTDataRate.currentText())]
        syncw = str(self.cbBTSyncw.currentText())
        if syncw.find('custom') >= 0:
            syncw = str(self.leSyncw.text())
            
        try:
            payloadLength = int(str(self.leBTPayload.text()))
        except:
            self.printLog('payloadLength is error(type)')
            return
        if payloadLength > 255 or payloadLength < 0:
            self.printLog('payloadLength is error(value)')
            return
        
        if str(self.cbBTTestMode.currentText()).find('BT TX') >= 0:
            cmd = 'fcc_bt_tx '+powerLevel+' '+chanJump+' '+str(channel)+' '+dataRateType+'\r'
        elif str(self.cbBTTestMode.currentText()).find('BT RX') >= 0 and self.cbBTDataRate.currentIndex() <= 1:
            if channel % 2 == 0:
                channel = channel / 2
            else:
                channel = (channel-1)/2 + 40
            cmd = 'rw_rx_per 0 '+str(channel)+' '+hex(self._ulap)+' '+str(self._ltaddr)
        elif str(self.cbBTTestMode.currentText()).find('BT RX') >= 0 and self.cbBTDataRate.currentIndex() > 1:
            if channel % 2 == 0:
                channel = channel / 2
            else:
                channel = (channel-1)/2 + 40
            cmd = 'rw_rx_per 1 '+str(channel)+' '+hex(self._ulap)+' '+str(self._ltaddr)
        elif str(self.cbBTTestMode.currentText()).find('BLE TX') >= 0 and syncw=='0x0':
            cmd = 'fcc_le_tx '+powerLevel+' '+str(channel)+' '+str(payloadLength)+' '+dataRateType+'\r'
        elif str(self.cbBTTestMode.currentText()).find('BLE TX') >= 0 and syncw!='0x0':
            cmd = 'fcc_le_tx '+powerLevel+' '+str(channel)+' '+str(payloadLength)+' '+dataRateType+' '+syncw+'\r'
        elif str(self.cbBTTestMode.currentText()).find('BLE RX') >= 0:
            cmd = 'rw_le_rx_per '+str(channel)+' '+syncw
        elif str(self.cbBTTestMode.currentText()).find('BT TX tone') >= 0:
            cmd = 'bt_tx_tone 1 '+str(channel)+' '+powerLevel
            
        if not cmd.endswith('\r'):
            cmd = cmd+'\r'
        self.cmdSend(cmd)
        

    def cmdStop(self):
        if self.twTestPanel.currentIndex() == 0 and str(self.cbWFTestMode.currentText()).find('tone') >= 0:
            channel = int(self.cbWFChannel.currentIndex()) + 1
            try:
                attenuation = int(str(self.leWFAtten.text()))
            except:
                self.printLog('attenuation is error(type)')
                return
            if attenuation > 255 or attenuation < 0:
                self.printLog('attenuation is error(value)')
                return
            cmd = 'wifiscwout 0 ' + str(channel) + ' ' + str(attenuation)+'\r'
            self.cmdSend(cmd)

        elif self.twTestPanel.currentIndex() == 0 and str(self.cbWFTestMode.currentText()).find('continue') >= 0:
            self.cmdSend('tx_contin_en 0\r')
            self.cmdSend('cmdstop\r')
            
        elif self.twTestPanel.currentIndex() == 1 and str(self.cbBTTestMode.currentText()).find('tone') >= 0:
            powerLevel = str(self.cbBTPowerLevel.currentText())
            channel = self.cbBTChannel.currentIndex()
            cmd = 'bt_tx_tone 0 '+str(channel)+' '+powerLevel+'\r'
            self.cmdSend(cmd)
        else:
            self.cmdSend('cmdstop\r')
    
    def loadSave(self, configParams):
        if configParams.has_key('manual_cmd'):
            for le in self.leSend_group:
                try:
                    self.leSend_group[le].setText(configParams['manual_cmd'][str(le)])
                except:
                    pass
            
    def saveParams(self):
        with open('./config/settings.conf', 'w') as fd:
            fd.write('\n[common_conf]\n')
            fd.write('Test_Type = '+str(int(self._TestType)) + ' # 0:cmd hander with wifi, 1:use cmd hander with esp')
            fd.write('\n[manual_cmd]\n')
            for le in self.leSend_group:
                fd.write(str(le) + '=' + self.leSend_group[le].text() + '\n')            
            

    ''' signal event handler '''
    def onClose(self):
        os._exit(0)
        
    def radiobtnChg(self, rbx):
        print(self.rbSend_group.checkedId(), 'has been selected')
    
    def cmdSend(self, sendData):
        if not self._ser.is_open:
            return

        if type(sendData) != type('s'):
            print 'sendData type is not right'
            return
        if (self._addCRFlag==True) and not sendData.endswith('\r'):
            sendData += '\r'
        if self._showSend == True:
            self.printLog(sendData)
        self._ser.write(bytes(sendData))        
    
    def manuCmdSend(self):
        if not self._ser.is_open:
            return 

        if self._cycleFlag == False:
            sendData = str(self.leSend_group[self.rbSend_group.checkedId()].text())
            self.cmdSend(sendData)
        else:
            try:
                cycInterval = int(self.leCycleInter.text())
            except:
                self.printLog('please input a number')
                return
            if cycInterval < 10:
                self.printLog('please input >= 10')
                return
            if self._cycSendFlg == False:
                self._cycSendFlg = True
                self.pbSend.setText('stop')
                self.leCycleInter.setEnabled(False)
                t1 = threading.Thread(target=self.cycTask, args=[1.0*cycInterval/1000, str(self.leSend_group[self.rbSend_group.checkedId()].text())])
                t1.start()
            else:
                self._cycSendFlg = False
                self.pbSend.setText('send')
                self.leCycleInter.setEnabled(True)
    
    def loadBin(self):
        self._ser.close()
        esp_params = esp_param()        
        esp_params.chip_type = str(self.cbChipType.currentText())
        esp_params.filename = str(self.leFilePath.text())
        esp_params.port_baud = int(self.cbComBaud.currentText())
        esp_params.port = str(self.cbComIndex.currentText())        
        if esp_params.filename.endswith('.bin') != True:
            self.printLog('choose file not a bin file')
            return
        esp_params.addr_filename = {(0x0, open(esp_params.filename,'rb'))}
        if str(self.cbLoadType.currentText()).find('RAM') >= 0:
            esp_params.esp_download_mode = 1
        elif str(self.cbLoadType.currentText()).find('Flash') >= 0:
            esp_params.esp_download_mode = 2
            
        print "esp params:", esp_params.chip_type, esp_params.filename
        print esp_params.port
        
        t1 = threading.Thread(target=t_loadBin, args=[self, esp_params])
        t1.start()
        self._ser.close()
        
    def _startRFTest(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("image/button_open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        if self._port_state == 1:
            #self.pbOpenSerial.setText('Open')
            icon.addPixmap(QtGui.QPixmap(_fromUtf8("image/button_close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pbOpenSerial.setIcon(icon)
            self.printLog('COM is close')
            self._ser.close()
            self.twTestPanel.setEnabled(False)
            self._cycSendFlg = False
            self.pbSend.setText('send')
            self.leCycleInter.setEnabled(True)
            self._port_state = 0
            return
        
    
        self.pbOpenSerial.setAutoFillBackground(True)
        p=self.pbOpenSerial.palette()
        p.setColor(QtGui.QPalette.Foreground,QtGui.QColor(0,123,255, 255))
        p.setColor(QtGui.QPalette.ButtonText,QtGui.QColor(255,0,0, 255))
        p.setBrush
        self.pbOpenSerial.setPalette(p)        

        com_port = str(self.cbComIndex.currentText())
        try:
            if str(self.cbComBaud.currentText()).find('custom') >= 0:
                baud_rate = int(self.leCOM.text())
            else:
                baud_rate = int(self.cbComBaud.currentText())

            self._ser = serial.Serial(port=com_port,
                                baudrate=baud_rate,
                                parity=serial.PARITY_NONE,stopbits=1,bytesize=8)
        except:
            self.printLog('open serial fail...')
            return
        self._port_state = 1
        #self.pbOpenSerial.setText('Close')
        self.pbOpenSerial.setIcon(icon)
        self.printLog('start rf test')
        self.twTestPanel.setEnabled(True)
        t2 = threading.Thread(target=startRFTest, args=[self, self._ser])
        t2.start()
    
    def showFileDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(None, 'Open file', './')
        self.leFilePath.setText(filename)
        
    def saveFileDialog(self):
        filename = QtGui.QFileDialog.getSaveFileName(None, 'Save file', './')
        with open(filename, 'w') as fd:
            fd.write(str(self.tbSerial.toPlainText()))
    
    def prbUpdate(self, persent):
        self.prbLoad.setValue(persent)
        if persent == 100:
            self._startRFTest()
        
    def cbUpdate(self):
        port_list = list(serial.tools.list_ports.comports())
        self.cbComIndex.clear()
        for port in port_list:
            print port[0]
            self.cbComIndex.addItem(_fromUtf8(port[0]))
        self.cbComIndex.showPopup()
                
    def printLog(self, log):
        log=str(log)
        if log.lower().find('esp_mac:') >= 0:
            mac = int(log[log.find('esp_mac:')+8:].replace('-', ''), 16)
            bt_mac = mac + 2
            self.teChipInfo.setText("STA Mac:\n"+hex(mac).strip('L').strip('0x').upper())
            if str(self.cbChipType.currentText()).find('32') >= 0:
                self.teChipInfo.append("BT Mac:\n"+hex(mac+2).strip('L').strip('0x').upper())
                
        if self._timeFlag == True:
            log = time.strftime('%y-%m-%d %H:%M:%S',time.localtime(time.time())) + '.' + str(int((time.time()*100)%100)) + ':' + log
        self.tbSerial.append(log)
        
            
    def showFlag(self):
        if self.ckbTimeFlag.isChecked()==True:
            self._timeFlag=True  
        else:
            self._timeFlag=False
            
        if self.ckbShowSend.isChecked() == True:
            self._showSend=True
        else:
            self._showSend=False

        if self.ckbAddCR.isChecked()==True:
            self._addCRFlag = True
        else:
            self._addCRFlag = False

        if self.ckbCycleFlag.isChecked()==True:
            self._cycleFlag = True
            self.leCycleInter.setEnabled(True)
        else:
            self._cycleFlag = False
            self.leCycleInter.setEnabled(False)
    
    def logClear(self):
        self.tbSerial.clear()

    def cycSend(self, cmd):
        self.cmdSend(str(cmd))

    def cycTask(self, cycInterval, cmd):
        print 'cycle:', cycInterval, '\ncmd:', cmd
        while True:
            time.sleep(cycInterval)
            if self._cycSendFlg == False:
                break
            self._SignalCycleTiming.emit(cmd)
        
        
def settingLoad(path):
    with open(path, "r") as fd:
        params = {}
        line = fd.readline()
        while line != '':
            if line.find('#'): line=line[:line.find('#')]
            if line.startswith('[') and line.find(']')>0:
                cmd_type = line[line.find('[')+1:line.find(']')]
                params[cmd_type] = {}
                line = fd.readline()
                while line != '':
                    if line.startswith('['): break
                    if line.find('#'): line=line[:line.find('#')]
                    line = line.strip('\n').strip(' ')
                    if len(line) > 0:
                        params[cmd_type][line.split('=')[0].strip(' ')] = line.split('=')[1].strip(' ')
                    line = fd.readline()
            else:
                line = fd.readline()
                
            
    return params


def main():
    params = {"common_conf":{"Test_Type":'0'}}
    try:
        params = settingLoad('./config/settings.conf')
    except:
        print 'not find config file use default settings'
        
    app = QtGui.QApplication(sys.argv)
    EspRFTool = QtGui.QWidget()
    ui = Ui_EspRFTool(EspRFTool, params)
    ui.show()
    sys.exit(app.exec_())    
    pass

if __name__ == "__main__":
    main()
    