import espRFToolUI
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
    if(params.chip_type == 'ESP32'):
        try:
            esp = esptool.ESP32ROM(params.port, initial_baud)
        except:
            print "ERROR!! The com port is occupied!!\n"
            esprftool._SignalTX.emit('ERROR!! The com port is occupied!!')
                
    elif(params.chip_type == 'ESP8266'):
        try:
            esp = esptool.ESP8266ROM(params.port, initial_baud)
        except:
            print "ERROR!! The com port is occupied!!\n"
            esprftool._SignalTX.emit('ERROR!! The com port is occupied!!')

    esp_mac = (00, 00, 00, 00, 00, 00)
    cus_mac = "00:00:00:00:00:00"
    print('%s: %s' % ("ESP_MAC", ':'.join(map(lambda x: '%02x' % x, esp_mac))))
    
    while True:
        try:
            esp.connect()
            break
        except:
            pass
        
    esprftool._SignalTX.emit('sync success')
    esp_mac = esp.read_mac()
    print 'esp_mac:%02x-%02x-%02x-%02x-%02x-%02x' %(esp_mac)
    esprftool._SignalTX.emit('esp_mac:%02x-%02x-%02x-%02x-%02x-%02x' %(esp_mac))
    
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
    BTDataType = {'1010':'0', '00001111':'1', 'prbs9':'2'}
    BTDataRate = {'1M':'1', '2M':'2', '3M':'3'}
    BLEDataRate = ('LE')
    BTDHType = {'DH1':'1', 'DH3':'3', 'DH5':'5'}
    BTChanJmp = {'no':'0', 'yes':'1'}
    BLEPayload = 0
    BLESyncw = {'0x71764129':'0', 'custom':'1'}

class CmdParams(WFParams, BTParams):
    def __init(self):
        pass

class myComboBox(QtGui.QComboBox):
    clicked = QtCore.pyqtSignal()
    def mousePressEvent(self, event):
        """ QComboBox.mousePressEvent(QMouseEvent) """
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()
    

class Ui_EspRFTool(espRFToolUI.Ui_EspRFtestTool, QtGui.QWidget):
    _SignalTX = QtCore.pyqtSignal(str)
    _Signalprb = QtCore.pyqtSignal(int)
    _SignalStart = QtCore.pyqtSignal()
    _port_status = 0
    _checkBok_selected = 0
    rbSend_group = QtGui.QButtonGroup()
    leSend_group = {}
    cmdParams = CmdParams()
    _WFStatus = 0 # use for WiFi tone
    _BTstatus = 0 # use for BT tone
    _ulap = 0x6bc6967e
    _ltaddr = 0x0
    def __init__(self, EspRFtestTool, parent=None):
        super(QtGui.QWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.setupSignal(self)
        self.twTestPanel.setEnabled(False)
        self.paramInit(self.cmdParams)
    
    def closeEvent(self, event):
        try:
            self._ser.close()
            print 'com port close'
        except:
            print 'com port not open'
        self.saveParams()
        print 'bye bye'
        sys.exit(0)
        
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
        QtCore.QObject.connect(self.pbBTSend, QtCore.SIGNAL(_fromUtf8("clicked()")), self.btCmdSend)
        QtCore.QObject.connect(self.pbWFSend, QtCore.SIGNAL(_fromUtf8("clicked()")), self.wfCmdSend)
        QtCore.QObject.connect(self.pbBTStop, QtCore.SIGNAL(_fromUtf8("clicked()")), self.cmdStop)
        QtCore.QObject.connect(self.pbWFStop, QtCore.SIGNAL(_fromUtf8("clicked()")), self.cmdStop)        
        self._SignalTX.connect(self.printLog)
        self._Signalprb.connect(self.prbUpdate)
        self._SignalStart.connect(self._startRFTest)
        QtCore.QMetaObject.connectSlotsByName(EspRFtestTool)
        self.rbSend1.setChecked(True)
        
        for chd in self.gbSend.children():
            if type(chd) == QtGui.QRadioButton:
                #chd.clicked.connect(lambda:self.radiobtnChg(chd))
                self.rbSend_group.addButton(chd, int(chd.objectName()[6:]))
            elif type(chd) == QtGui.QLineEdit:
                self.leSend_group[int(chd.objectName()[6:])] = chd
    
    def paramInit(self, cmdParams):
        self.loadSave()
        self.twTestPanel.setEnabled(False)
        self.twTestPanel.setCurrentIndex(0)
        self.cbWFTestMode.setCurrentIndex(0)
        self.cbBTTestMode.setCurrentIndex(0)
        self.cbWFChannel.clear()
        self.leSyncw.setHidden(True)
        self.leCOM.setHidden(True)
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
        self.cbBTDataType.setCurrentIndex(0)
        self.cbBTDHType.setCurrentIndex(0)
        self.cbBTPowerLevel.setCurrentIndex(4)
        self.cbBTSyncw.setCurrentIndex(0)
        self.leBTPayload.setText('0')
        pass
    
    def wfCmdUpdate(self):
        pass
    
    def btCmdUpdate(self):
        if str(self.cbBTTestMode.currentText()).find('BT') >= 0:
            self.cbBTChannel.clear()
            for i in range(79):
                self.cbBTChannel.addItem(str(i))
            self.leBTPayload.setEnabled(False)
            self.cbBTSyncw.setEnabled(False)
            self.cbBTPowerLevel.addItem('9')
            self.cbBTDataRate.setEnabled(True)
            self.cbBTDHType.setEnabled(True)
            self.cbBTDataRate.clear()
            for dr in self.cmdParams.BTDataRate:
                self.cbBTDataRate.addItem(dr)
                
        elif str(self.cbBTTestMode.currentText()).find('BLE') >= 0:
            self.cbBTChannel.clear()
            for i in range(40):
                self.cbBTChannel.addItem(str(i))
            self.leBTPayload.setEnabled(True)
            self.cbBTSyncw.setEnabled(True)
            self.cbBTPowerLevel.removeItem(9)
            self.cbBTDataRate.setEnabled(False)
            self.cbBTDHType.setEnabled(False)
            self.cbBTDataRate.clear()
            for dr in self.cmdParams.BLEDataRate:
                self.cbBTDataRate.addItem(dr)            
            
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
            self.cmdSend(cmd)
        elif str(self.cbWFTestMode.currentText()).find('TX packet') >= 0:
            self.cmdSend('tx_contin_en 0\r')
            cmd = 'wifitxout ' + str(channel) + ' ' + rate + ' ' + str(attenuation)
            self.cmdSend(cmd)
        elif str(self.cbWFTestMode.currentText()).find('RX packet') >= 0:
            cmd = 'esp_rx ' + str(channel) + ' ' + rate
            self.cmdSend(cmd)
        elif str(self.cbWFTestMode.currentText()).find('TX tone') >= 0:
            cmd = 'wifiscwout 1 ' + str(channel) + ' ' + str(attenuation)
            self.cmdSend(cmd)
    
    def btCmdSend(self):
        cmd = ''
        powerLevel = str(self.cbBTPowerLevel.currentText())
        chanJump = str(self.cbBTChanJmp.currentIndex())
        channel = self.cbBTChannel.currentIndex()
        dataRate = self.cmdParams.BTDataRate[str(self.cbBTDataRate.currentText())]
        dhType = self.cmdParams.BTDHType[str(self.cbBTDHType.currentText())]
        dataType = str(self.cbBTDataType.currentText())
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
        
        if str(self.cbBTTestMode.currentText()).find('classBT TX') >= 0:
            cmd = 'fcc_bt_tx '+powerLevel+' '+chanJump+' '+str(channel)+' '+dataRate+' '+dhType+' '+dataType+'\r'
            self.cmdSend(cmd)
        elif str(self.cbBTTestMode.currentText()).find('classBT RX/BR') >= 0:
            if channel % 2 == 0:
                channel = channel / 2
            else:
                channel = (channel-1)/2 + 40
            cmd = 'rw_rx_per 0 '+str(channel)+' '+str(self._ulap)+' '+str(self._ltaddr)
            self.cmdSend(cmd)
        elif str(self.cbBTTestMode.currentText()).find('classBT RX/EDR') >= 0:
            if channel % 2 == 0:
                channel = channel / 2
            else:
                channel = (channel-1)/2 + 40
            cmd = 'rw_rx_per 1 '+str(channel)+' '+str(self._ulap)+' '+str(self._ltaddr)
            self.cmdSend(cmd)
        elif str(self.cbBTTestMode.currentText()).find('BLE TX') >= 0:
            cmd = 'fcc_le_tx '+powerLevel+' '+str(channel)+' '+str(payloadLength)+' '+dataType+'\r'
            self.cmdSend(cmd)
        elif str(self.cbBTTestMode.currentText()).find('BLE TX Syncw') >= 0:
            cmd = 'fcc_le_tx '+powerLevel+' '+str(channel)+' '+str(payloadLength)+' '+dataType+' '+syncw+'\r'
            self.cmdSend(cmd)
        elif str(self.cbBTTestMode.currentText()).find('BLE RX') >= 0:
            cmd = 'rw_le_rx_per '+str(channel)+' '+syncw
            self.cmdSend(cmd)
        elif str(self.cbBTTestMode.currentText()).find('BT TX tone') >= 0:
            cmd = 'bt_tx_tone 1'+str(channel)+' '+syncw+' '+powerLevel
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
            cmd = 'wifiscwout 0 ' + str(channel) + ' ' + str(attenuation)
            self.cmdSend(cmd)
            
        elif self.twTestPanel.currentIndex() == 1 and str(self.cbBTTestMode.currentText()).find('tone') >= 0:
            powerLevel = str(self.cbBTPowerLevel.currentText())
            channel = self.cbBTChannel.currentIndex()
            cmd = 'bt_tx_tone 0 '+str(channel)+' '+powerLevel
            self.cmdSend(cmd)
        else:
            self.cmdSend('cmdstop\r')
    
    def loadSave(self):
        try:
            with open('default.conf', 'r') as fd:
                for le in self.leSend_group:
                    rl = fd.readline().strip('\n')
                    rl = rl[rl.find(':')+1:]
                    self.leSend_group[le].setText(rl)
        except:
            print 'not find config file'
            
    def saveParams(self):
        with open('default.conf', 'w') as fd:
            for le in self.leSend_group:
                fd.write(str(le) + ':' + self.leSend_group[le].text() + '\n')

    ''' signal event handler '''
    def onClose(self):
        exit()
        
    def radiobtnChg(self, rbx):
        print(self.rbSend_group.checkedId(), 'has been selected')
    
    def cmdSend(self, sendData):
        if not sendData.endswith('\r'):
            sendData += '\r'
        self.printLog(sendData)
        self._ser.write(bytes(sendData))        
    
    def manuCmdSend(self):
        sendData = self.leSend_group[self.rbSend_group.checkedId()].text()
        self.cmdSend(sendData)
    
    def loadBin(self):
        esp_params = esp_param()        
        esp_params.chip_type = str(self.cbChipType.currentText())
        esp_params.filename = str(self.leFilePath.text())
        esp_params.port_baud = int(self.cbComBaud.currentText())
        esp_params.port = str(self.cbComIndex.currentText())        
        if esp_params.filename.endswith('.bin') != True:
            self.printLog('choose file not a bin file')
            return
        esp_params.addr_filename = {(0x0, open(esp_params.filename,'rb'))}
            
        print "esp params:", esp_params.chip_type, esp_params.filename
        print esp_params.port
        
        t1 = threading.Thread(target=t_loadBin, args=[self, esp_params])
        t1.start()
        
    def _startRFTest(self):
        if(self._port_status == 1):
            self.pbOpenSerial.setText('Open COM')
            self.printLog('COM is close')
            self._port_status = 0
            self._ser.close()
            self.twTestPanel.setEnabled(False)
            return

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
        
        self._port_status = 1
        self.pbOpenSerial.setText('Close COM')
        
        self.printLog('start rf test')
        self.twTestPanel.setEnabled(True)
        t2 = threading.Thread(target=startRFTest, args=[self, self._ser])
        t2.start()
    
    def showFileDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(None, 'Open file', './')
        self.leFilePath.setText(filename)
    
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
        self.tbSerial.append(log)
               

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    EspRFTool = QtGui.QWidget()
    ui = Ui_EspRFTool(EspRFTool)
    ui.show()
    sys.exit(app.exec_())