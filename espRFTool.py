import espRFToolUI
from PyQt4 import QtCore, QtGui
import threading
import sys
import serial  
import serial.tools.list_ports 
import esptool

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
    flash_path = ''     #para_dict['FLASH_PATH']
    addr_filename = ''  #{(0x0, self.flash_path)}
    rampath = ''
    
    
class esp_dev_param(object):
    chip_type = 'ESP32' #para_dict['CHIP_TYPE']
    port = ''
    port_baud = 115200
    compress = False
    no_compress = True
    no_stub = False
    verify = False
    esp_download_mode = 2
    
    
class esp_param(write_flash_param, esp_dev_param):
    def __init__(self):
        pass
    

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
    if not params.no_stub:
        esp = esp.run_stub()
        
    esp_mac = esp.read_mac()
    esp.change_baud(921600)
    print 'esp_mac:%02x-%02x-%02x-%02x-%02x-%02x' %(esp_mac)
    esprftool._SignalTX.emit('esp_mac:%02x-%02x-%02x-%02x-%02x-%02x' %(esp_mac))
    
    if(params.esp_download_mode == 1):        
        #print "load ram ..."
        load_ram(esp, params.rampath)
        
    elif(params.esp_download_mode == 2):
        #print "load flash ..." 
        write_flash(esp, params, esprftool)


class Ui_EspRFTool(espRFToolUI.Ui_EspRFtestTool, QtCore.QObject):
    _SignalTX = QtCore.pyqtSignal(str)
    _Signalprb = QtCore.pyqtSignal(int)
    def __init__(self,EspRFtestTool):
        #self._Singnal.connect(self.printLog)
        super(Ui_EspRFTool, self).__init__()  
        self.setupUi(EspRFtestTool)
        self.setupSignal(EspRFtestTool)
    
    def init(self):
        pass
        
    def setupSignal(self, EspRFtestTool):
        #QtCore.QObject.connect(self.pbOpenSerial, QtCore.SIGNAL(_fromUtf8("clicked()")), EspRFtestTool.exec)
        QtCore.QObject.connect(self.pbComIndex, QtCore.SIGNAL(_fromUtf8("clicked()")), self.cbUpdate)
        QtCore.QObject.connect(self.pbComIndex_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.cbUpdate)
        QtCore.QObject.connect(self.pbLoadBin, QtCore.SIGNAL(_fromUtf8("clicked()")), self.loadBin)
        QtCore.QObject.connect(self.cbComIndex, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.cbUpdate2)
        QtCore.QObject.connect(self.pbOpenFile, QtCore.SIGNAL(_fromUtf8("clicked()")), self.showFileDialog)
        self._SignalTX.connect(self.printLog)
        self._Signalprb.connect(self.prbUpdate)
        QtCore.QMetaObject.connectSlotsByName(EspRFtestTool)

    ''' signal event handler '''
    def loadBin(self):
        esp_params = esp_param()        
        esp_params.chip_type = str(self.cbChipType.currentText())
        esp_params.flash_path = str(self.leFilePath.text())
        esp_params.port_baud = int(self.cbComBaud.currentText())
        esp_params.port = str(self.cbComIndex.currentText())        
        if esp_params.flash_path.endswith('.bin') != True:
            self.printLog('choose file not a bin file')
            return
        esp_params.addr_filename = {(0x0, open(esp_params.flash_path,'rb'))}
            
        print "esp params:", esp_params.chip_type, esp_params.flash_path
        print esp_params.port
        
        t1 = threading.Thread(target=t_loadBin, args=[self, esp_params])
        t1.start()
    
    def showFileDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(None, 'Open file', './')
        self.leFilePath.setText(filename)
    
    def prbUpdate(self, pesent):
        self.prbLoad.setValue(pesent)
        
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
    EspRFTool = QtGui.QDialog()
    ui = Ui_EspRFTool(EspRFTool)

    EspRFTool.show()
    sys.exit(app.exec_())