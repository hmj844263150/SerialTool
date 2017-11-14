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


class Ui_EspRFTool(espRFToolUI.Ui_EspRFtestTool, QtGui.QWidget):
    _SignalTX = QtCore.pyqtSignal(str)
    _Signalprb = QtCore.pyqtSignal(int)
    _SignalStart = QtCore.pyqtSignal()
    _port_status = 0
    _checkBok_selected = 0
    rbSend_group = QtGui.QButtonGroup()
    leSend_group = {}    
    def __init__(self, EspRFtestTool, parent=None):
        super(QtGui.QWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.setupSignal(self)
        self.twTestPanel.setEnabled(False)
        self.loadParams()
    
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
        QtCore.QObject.connect(self.pbComIndex, QtCore.SIGNAL(_fromUtf8("clicked()")), self.cbUpdate)
        QtCore.QObject.connect(self.pbComIndex_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.cbUpdate)
        QtCore.QObject.connect(self.pbLoadBin, QtCore.SIGNAL(_fromUtf8("clicked()")), self.loadBin)
        QtCore.QObject.connect(self.cbComIndex, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.cbUpdate2)
        QtCore.QObject.connect(self.pbOpenFile, QtCore.SIGNAL(_fromUtf8("clicked()")), self.showFileDialog)
        QtCore.QObject.connect(self.pbSend, QtCore.SIGNAL(_fromUtf8("clicked()")), self.cmdSend)
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
    
    def loadParams(self):
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
    
    def cmdSend(self):
        send_data = self.leSend_group[self.rbSend_group.checkedId()].text()
        send_data += '\r'
        self.printLog(send_data)
        self._ser.write(bytes(send_data))
    
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
        baud_rate = int(self.cbComBaud.currentText())
        try:
            self._ser = serial.Serial(port=com_port,
                                baudrate=baud_rate,
                                parity=serial.PARITY_NONE,stopbits=1,bytesize=8)
        except:
            self.printLog('serial has been occupied')
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
        
    def cbUpdate2(self):
        self.pbComIndex.setText(self.cbComIndex.currentText())
        
    def printLog(self, log):
        self.tbSerial.append(log)
               

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    EspRFTool = QtGui.QWidget()
    ui = Ui_EspRFTool(EspRFTool)
    ui.show()
    sys.exit(app.exec_())