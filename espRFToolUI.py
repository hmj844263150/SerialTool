# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'espRFToolUI.ui'
#
# Created: Wed Nov 22 14:39:40 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_EspRFtestTool(object):
    def setupUi(self, EspRFtestTool):
        EspRFtestTool.setObjectName(_fromUtf8("EspRFtestTool"))
        EspRFtestTool.resize(550, 570)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EspRFtestTool.sizePolicy().hasHeightForWidth())
        EspRFtestTool.setSizePolicy(sizePolicy)
        EspRFtestTool.setMinimumSize(QtCore.QSize(550, 560))
        EspRFtestTool.setMaximumSize(QtCore.QSize(550, 570))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("image/esplogo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        EspRFtestTool.setWindowIcon(icon)
        self.tbSerial = QtGui.QTextBrowser(EspRFtestTool)
        self.tbSerial.setGeometry(QtCore.QRect(10, 320, 451, 241))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(200)
        sizePolicy.setHeightForWidth(self.tbSerial.sizePolicy().hasHeightForWidth())
        self.tbSerial.setSizePolicy(sizePolicy)
        self.tbSerial.setObjectName(_fromUtf8("tbSerial"))
        self.line = QtGui.QFrame(EspRFtestTool)
        self.line.setGeometry(QtCore.QRect(-3, 30, 611, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.line_2 = QtGui.QFrame(EspRFtestTool)
        self.line_2.setGeometry(QtCore.QRect(0, 100, 911, 20))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayoutWidget = QtGui.QWidget(EspRFtestTool)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 40, 551, 71))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout_11 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setContentsMargins(5, -1, 5, -1)
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setContentsMargins(0, -1, -1, -1)
        self.gridLayout_4.setVerticalSpacing(6)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.pbOpenFile = QtGui.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbOpenFile.sizePolicy().hasHeightForWidth())
        self.pbOpenFile.setSizePolicy(sizePolicy)
        self.pbOpenFile.setObjectName(_fromUtf8("pbOpenFile"))
        self.gridLayout_4.addWidget(self.pbOpenFile, 0, 11, 1, 1)
        self.leStatus = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.leStatus.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leStatus.sizePolicy().hasHeightForWidth())
        self.leStatus.setSizePolicy(sizePolicy)
        self.leStatus.setMinimumSize(QtCore.QSize(60, 50))
        self.leStatus.setMaximumSize(QtCore.QSize(60, 50))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Bauhaus 93"))
        font.setPointSize(16)
        self.leStatus.setFont(font)
        self.leStatus.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.leStatus.setAutoFillBackground(True)
        self.leStatus.setText(_fromUtf8(" IDLE"))
        self.leStatus.setObjectName(_fromUtf8("leStatus"))
        self.gridLayout_4.addWidget(self.leStatus, 0, 1, 2, 1)
        self.pbLoadBin = QtGui.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbLoadBin.sizePolicy().hasHeightForWidth())
        self.pbLoadBin.setSizePolicy(sizePolicy)
        self.pbLoadBin.setObjectName(_fromUtf8("pbLoadBin"))
        self.gridLayout_4.addWidget(self.pbLoadBin, 1, 11, 1, 1)
        self.label_10 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_10.setText(_fromUtf8(""))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_4.addWidget(self.label_10, 0, 2, 1, 1)
        self.label_23 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_23.setText(_fromUtf8(""))
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.gridLayout_4.addWidget(self.label_23, 1, 10, 1, 1)
        self.leFilePath = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.leFilePath.setEnabled(False)
        self.leFilePath.setObjectName(_fromUtf8("leFilePath"))
        self.gridLayout_4.addWidget(self.leFilePath, 0, 6, 1, 1)
        self.teChipInfo = QtGui.QTextEdit(self.verticalLayoutWidget)
        self.teChipInfo.setMaximumSize(QtCore.QSize(120, 50))
        self.teChipInfo.setObjectName(_fromUtf8("teChipInfo"))
        self.gridLayout_4.addWidget(self.teChipInfo, 0, 4, 2, 1)
        self.label_20 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_20.setText(_fromUtf8(""))
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.gridLayout_4.addWidget(self.label_20, 0, 5, 1, 1)
        self.cbLoadType = QtGui.QComboBox(self.verticalLayoutWidget)
        self.cbLoadType.setMinimumSize(QtCore.QSize(20, 0))
        self.cbLoadType.setMaximumSize(QtCore.QSize(50, 16777215))
        self.cbLoadType.setObjectName(_fromUtf8("cbLoadType"))
        self.cbLoadType.addItem(_fromUtf8(""))
        self.cbLoadType.addItem(_fromUtf8(""))
        self.gridLayout_4.addWidget(self.cbLoadType, 0, 8, 1, 2)
        self.label_24 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_24.setText(_fromUtf8(""))
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.gridLayout_4.addWidget(self.label_24, 1, 9, 1, 1)
        self.prbLoad = QtGui.QProgressBar(self.verticalLayoutWidget)
        self.prbLoad.setProperty("value", 0)
        self.prbLoad.setObjectName(_fromUtf8("prbLoad"))
        self.gridLayout_4.addWidget(self.prbLoad, 1, 6, 1, 3)
        self.label_25 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_25.setText(_fromUtf8(""))
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.gridLayout_4.addWidget(self.label_25, 0, 7, 1, 1)
        self.verticalLayout_11.addLayout(self.gridLayout_4)
        self.twTestPanel = QtGui.QTabWidget(EspRFtestTool)
        self.twTestPanel.setEnabled(True)
        self.twTestPanel.setGeometry(QtCore.QRect(10, 120, 533, 191))
        self.twTestPanel.setObjectName(_fromUtf8("twTestPanel"))
        self.tabWF = QtGui.QWidget()
        self.tabWF.setObjectName(_fromUtf8("tabWF"))
        self.cbWFTestMode = QtGui.QComboBox(self.tabWF)
        self.cbWFTestMode.setGeometry(QtCore.QRect(20, 30, 101, 22))
        self.cbWFTestMode.setObjectName(_fromUtf8("cbWFTestMode"))
        self.cbWFTestMode.addItem(_fromUtf8(""))
        self.cbWFTestMode.addItem(_fromUtf8(""))
        self.cbWFTestMode.addItem(_fromUtf8(""))
        self.cbWFTestMode.addItem(_fromUtf8(""))
        self.label_4 = QtGui.QLabel(self.tabWF)
        self.label_4.setGeometry(QtCore.QRect(20, 10, 101, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.tabWF)
        self.label_5.setGeometry(QtCore.QRect(20, 60, 101, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.leWFAtten = QtGui.QLineEdit(self.tabWF)
        self.leWFAtten.setGeometry(QtCore.QRect(20, 80, 101, 20))
        self.leWFAtten.setObjectName(_fromUtf8("leWFAtten"))
        self.cbWFDataRate = QtGui.QComboBox(self.tabWF)
        self.cbWFDataRate.setGeometry(QtCore.QRect(410, 30, 101, 22))
        self.cbWFDataRate.setObjectName(_fromUtf8("cbWFDataRate"))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.cbWFDataRate.addItem(_fromUtf8(""))
        self.label_6 = QtGui.QLabel(self.tabWF)
        self.label_6.setGeometry(QtCore.QRect(410, 10, 101, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.cbWFChannel = QtGui.QComboBox(self.tabWF)
        self.cbWFChannel.setGeometry(QtCore.QRect(150, 30, 101, 22))
        self.cbWFChannel.setObjectName(_fromUtf8("cbWFChannel"))
        self.cbWFChannel.addItem(_fromUtf8(""))
        self.cbWFChannel.addItem(_fromUtf8(""))
        self.cbWFChannel.addItem(_fromUtf8(""))
        self.cbWFChannel.addItem(_fromUtf8(""))
        self.cbWFChannel.addItem(_fromUtf8(""))
        self.cbWFChannel.addItem(_fromUtf8(""))
        self.cbWFChannel.addItem(_fromUtf8(""))
        self.cbWFChannel.addItem(_fromUtf8(""))
        self.cbWFChannel.addItem(_fromUtf8(""))
        self.cbWFChannel.addItem(_fromUtf8(""))
        self.cbWFChannel.addItem(_fromUtf8(""))
        self.cbWFChannel.addItem(_fromUtf8(""))
        self.cbWFChannel.addItem(_fromUtf8(""))
        self.cbWFChannel.addItem(_fromUtf8(""))
        self.label_7 = QtGui.QLabel(self.tabWF)
        self.label_7.setGeometry(QtCore.QRect(150, 10, 101, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(self.tabWF)
        self.label_8.setGeometry(QtCore.QRect(280, 10, 101, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.cbWFBandWidth = QtGui.QComboBox(self.tabWF)
        self.cbWFBandWidth.setGeometry(QtCore.QRect(280, 30, 101, 22))
        self.cbWFBandWidth.setObjectName(_fromUtf8("cbWFBandWidth"))
        self.cbWFBandWidth.addItem(_fromUtf8(""))
        self.cbWFBandWidth.addItem(_fromUtf8(""))
        self.pbWFStop = QtGui.QPushButton(self.tabWF)
        self.pbWFStop.setGeometry(QtCore.QRect(440, 130, 71, 23))
        self.pbWFStop.setObjectName(_fromUtf8("pbWFStop"))
        self.pbWFSend = QtGui.QPushButton(self.tabWF)
        self.pbWFSend.setGeometry(QtCore.QRect(360, 130, 71, 23))
        self.pbWFSend.setObjectName(_fromUtf8("pbWFSend"))
        self.twTestPanel.addTab(self.tabWF, _fromUtf8(""))
        self.tabBT = QtGui.QWidget()
        self.tabBT.setObjectName(_fromUtf8("tabBT"))
        self.cbBTTestMode = QtGui.QComboBox(self.tabBT)
        self.cbBTTestMode.setGeometry(QtCore.QRect(20, 30, 101, 22))
        self.cbBTTestMode.setObjectName(_fromUtf8("cbBTTestMode"))
        self.cbBTTestMode.addItem(_fromUtf8(""))
        self.cbBTTestMode.addItem(_fromUtf8(""))
        self.cbBTTestMode.addItem(_fromUtf8(""))
        self.cbBTTestMode.addItem(_fromUtf8(""))
        self.cbBTTestMode.addItem(_fromUtf8(""))
        self.cbBTTestMode.addItem(_fromUtf8(""))
        self.cbBTTestMode.addItem(_fromUtf8(""))
        self.pbBTStop = QtGui.QPushButton(self.tabBT)
        self.pbBTStop.setGeometry(QtCore.QRect(440, 130, 71, 23))
        self.pbBTStop.setObjectName(_fromUtf8("pbBTStop"))
        self.cbBTChannel = QtGui.QComboBox(self.tabBT)
        self.cbBTChannel.setGeometry(QtCore.QRect(280, 30, 101, 22))
        self.cbBTChannel.setObjectName(_fromUtf8("cbBTChannel"))
        self.label_9 = QtGui.QLabel(self.tabBT)
        self.label_9.setGeometry(QtCore.QRect(280, 10, 101, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.lbBTPowerLevel = QtGui.QLabel(self.tabBT)
        self.lbBTPowerLevel.setGeometry(QtCore.QRect(150, 10, 101, 16))
        self.lbBTPowerLevel.setObjectName(_fromUtf8("lbBTPowerLevel"))
        self.label_11 = QtGui.QLabel(self.tabBT)
        self.label_11.setGeometry(QtCore.QRect(20, 10, 101, 16))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_12 = QtGui.QLabel(self.tabBT)
        self.label_12.setGeometry(QtCore.QRect(20, 110, 101, 16))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.cbBTChanJmp = QtGui.QComboBox(self.tabBT)
        self.cbBTChanJmp.setGeometry(QtCore.QRect(20, 130, 101, 22))
        self.cbBTChanJmp.setObjectName(_fromUtf8("cbBTChanJmp"))
        self.cbBTChanJmp.addItem(_fromUtf8(""))
        self.cbBTChanJmp.addItem(_fromUtf8(""))
        self.cbBTDataRate = QtGui.QComboBox(self.tabBT)
        self.cbBTDataRate.setGeometry(QtCore.QRect(150, 80, 101, 22))
        self.cbBTDataRate.setObjectName(_fromUtf8("cbBTDataRate"))
        self.cbBTDataRate.addItem(_fromUtf8(""))
        self.cbBTDataRate.addItem(_fromUtf8(""))
        self.cbBTDataRate.addItem(_fromUtf8(""))
        self.label_13 = QtGui.QLabel(self.tabBT)
        self.label_13.setGeometry(QtCore.QRect(150, 60, 101, 16))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.cbBTPowerLevel = QtGui.QComboBox(self.tabBT)
        self.cbBTPowerLevel.setGeometry(QtCore.QRect(150, 30, 101, 22))
        self.cbBTPowerLevel.setObjectName(_fromUtf8("cbBTPowerLevel"))
        self.cbBTPowerLevel.addItem(_fromUtf8(""))
        self.cbBTPowerLevel.addItem(_fromUtf8(""))
        self.cbBTPowerLevel.addItem(_fromUtf8(""))
        self.cbBTPowerLevel.addItem(_fromUtf8(""))
        self.cbBTPowerLevel.addItem(_fromUtf8(""))
        self.cbBTPowerLevel.addItem(_fromUtf8(""))
        self.cbBTPowerLevel.addItem(_fromUtf8(""))
        self.cbBTPowerLevel.addItem(_fromUtf8(""))
        self.cbBTPowerLevel.addItem(_fromUtf8(""))
        self.cbBTDataType = QtGui.QComboBox(self.tabBT)
        self.cbBTDataType.setGeometry(QtCore.QRect(20, 80, 101, 22))
        self.cbBTDataType.setObjectName(_fromUtf8("cbBTDataType"))
        self.cbBTDataType.addItem(_fromUtf8(""))
        self.cbBTDataType.addItem(_fromUtf8(""))
        self.cbBTDataType.addItem(_fromUtf8(""))
        self.label_14 = QtGui.QLabel(self.tabBT)
        self.label_14.setGeometry(QtCore.QRect(20, 60, 101, 16))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.label_15 = QtGui.QLabel(self.tabBT)
        self.label_15.setGeometry(QtCore.QRect(280, 60, 101, 16))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.cbBTDHType = QtGui.QComboBox(self.tabBT)
        self.cbBTDHType.setGeometry(QtCore.QRect(280, 80, 101, 22))
        self.cbBTDHType.setObjectName(_fromUtf8("cbBTDHType"))
        self.cbBTDHType.addItem(_fromUtf8(""))
        self.cbBTDHType.addItem(_fromUtf8(""))
        self.cbBTDHType.addItem(_fromUtf8(""))
        self.label_16 = QtGui.QLabel(self.tabBT)
        self.label_16.setGeometry(QtCore.QRect(410, 10, 101, 16))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.leBTPayload = QtGui.QLineEdit(self.tabBT)
        self.leBTPayload.setGeometry(QtCore.QRect(410, 30, 101, 20))
        self.leBTPayload.setObjectName(_fromUtf8("leBTPayload"))
        self.label_17 = QtGui.QLabel(self.tabBT)
        self.label_17.setGeometry(QtCore.QRect(410, 60, 101, 16))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.cbBTSyncw = QtGui.QComboBox(self.tabBT)
        self.cbBTSyncw.setGeometry(QtCore.QRect(410, 80, 101, 22))
        self.cbBTSyncw.setObjectName(_fromUtf8("cbBTSyncw"))
        self.cbBTSyncw.addItem(_fromUtf8(""))
        self.cbBTSyncw.addItem(_fromUtf8(""))
        self.leSyncw = QtGui.QLineEdit(self.tabBT)
        self.leSyncw.setGeometry(QtCore.QRect(410, 80, 82, 22))
        self.leSyncw.setObjectName(_fromUtf8("leSyncw"))
        self.pbBTSend = QtGui.QPushButton(self.tabBT)
        self.pbBTSend.setGeometry(QtCore.QRect(360, 130, 71, 23))
        self.pbBTSend.setObjectName(_fromUtf8("pbBTSend"))
        self.twTestPanel.addTab(self.tabBT, _fromUtf8(""))
        self.tabManul = QtGui.QWidget()
        self.tabManul.setObjectName(_fromUtf8("tabManul"))
        self.gbSend = QtGui.QGroupBox(self.tabManul)
        self.gbSend.setEnabled(True)
        self.gbSend.setGeometry(QtCore.QRect(0, 0, 531, 181))
        self.gbSend.setTitle(_fromUtf8(""))
        self.gbSend.setObjectName(_fromUtf8("gbSend"))
        self.rbSend1 = QtGui.QRadioButton(self.gbSend)
        self.rbSend1.setGeometry(QtCore.QRect(10, 10, 16, 16))
        self.rbSend1.setText(_fromUtf8(""))
        self.rbSend1.setObjectName(_fromUtf8("rbSend1"))
        self.rbSend2 = QtGui.QRadioButton(self.gbSend)
        self.rbSend2.setGeometry(QtCore.QRect(10, 40, 16, 16))
        self.rbSend2.setText(_fromUtf8(""))
        self.rbSend2.setObjectName(_fromUtf8("rbSend2"))
        self.rbSend3 = QtGui.QRadioButton(self.gbSend)
        self.rbSend3.setGeometry(QtCore.QRect(10, 70, 16, 16))
        self.rbSend3.setText(_fromUtf8(""))
        self.rbSend3.setObjectName(_fromUtf8("rbSend3"))
        self.rbSend4 = QtGui.QRadioButton(self.gbSend)
        self.rbSend4.setGeometry(QtCore.QRect(10, 100, 16, 16))
        self.rbSend4.setText(_fromUtf8(""))
        self.rbSend4.setObjectName(_fromUtf8("rbSend4"))
        self.rbSend5 = QtGui.QRadioButton(self.gbSend)
        self.rbSend5.setGeometry(QtCore.QRect(10, 130, 16, 16))
        self.rbSend5.setText(_fromUtf8(""))
        self.rbSend5.setObjectName(_fromUtf8("rbSend5"))
        self.rbSend6 = QtGui.QRadioButton(self.gbSend)
        self.rbSend6.setGeometry(QtCore.QRect(240, 10, 16, 16))
        self.rbSend6.setText(_fromUtf8(""))
        self.rbSend6.setObjectName(_fromUtf8("rbSend6"))
        self.rbSend7 = QtGui.QRadioButton(self.gbSend)
        self.rbSend7.setGeometry(QtCore.QRect(240, 40, 16, 16))
        self.rbSend7.setText(_fromUtf8(""))
        self.rbSend7.setObjectName(_fromUtf8("rbSend7"))
        self.rbSend8 = QtGui.QRadioButton(self.gbSend)
        self.rbSend8.setGeometry(QtCore.QRect(240, 70, 16, 16))
        self.rbSend8.setText(_fromUtf8(""))
        self.rbSend8.setObjectName(_fromUtf8("rbSend8"))
        self.leSend1 = QtGui.QLineEdit(self.gbSend)
        self.leSend1.setGeometry(QtCore.QRect(30, 10, 191, 20))
        self.leSend1.setObjectName(_fromUtf8("leSend1"))
        self.leSend2 = QtGui.QLineEdit(self.gbSend)
        self.leSend2.setGeometry(QtCore.QRect(30, 40, 191, 20))
        self.leSend2.setObjectName(_fromUtf8("leSend2"))
        self.leSend3 = QtGui.QLineEdit(self.gbSend)
        self.leSend3.setGeometry(QtCore.QRect(30, 70, 191, 20))
        self.leSend3.setObjectName(_fromUtf8("leSend3"))
        self.leSend4 = QtGui.QLineEdit(self.gbSend)
        self.leSend4.setGeometry(QtCore.QRect(30, 100, 191, 20))
        self.leSend4.setObjectName(_fromUtf8("leSend4"))
        self.leSend7 = QtGui.QLineEdit(self.gbSend)
        self.leSend7.setGeometry(QtCore.QRect(260, 40, 191, 20))
        self.leSend7.setObjectName(_fromUtf8("leSend7"))
        self.leSend8 = QtGui.QLineEdit(self.gbSend)
        self.leSend8.setGeometry(QtCore.QRect(260, 70, 191, 20))
        self.leSend8.setObjectName(_fromUtf8("leSend8"))
        self.leSend6 = QtGui.QLineEdit(self.gbSend)
        self.leSend6.setGeometry(QtCore.QRect(260, 10, 191, 20))
        self.leSend6.setObjectName(_fromUtf8("leSend6"))
        self.leSend5 = QtGui.QLineEdit(self.gbSend)
        self.leSend5.setGeometry(QtCore.QRect(30, 130, 191, 20))
        self.leSend5.setObjectName(_fromUtf8("leSend5"))
        self.rbSend9 = QtGui.QRadioButton(self.gbSend)
        self.rbSend9.setGeometry(QtCore.QRect(240, 100, 16, 16))
        self.rbSend9.setText(_fromUtf8(""))
        self.rbSend9.setObjectName(_fromUtf8("rbSend9"))
        self.leSend9 = QtGui.QLineEdit(self.gbSend)
        self.leSend9.setGeometry(QtCore.QRect(260, 100, 191, 20))
        self.leSend9.setObjectName(_fromUtf8("leSend9"))
        self.leSend10 = QtGui.QLineEdit(self.gbSend)
        self.leSend10.setGeometry(QtCore.QRect(260, 130, 191, 20))
        self.leSend10.setObjectName(_fromUtf8("leSend10"))
        self.rbSend10 = QtGui.QRadioButton(self.gbSend)
        self.rbSend10.setGeometry(QtCore.QRect(240, 130, 16, 16))
        self.rbSend10.setText(_fromUtf8(""))
        self.rbSend10.setObjectName(_fromUtf8("rbSend10"))
        self.pbSend = QtGui.QPushButton(self.gbSend)
        self.pbSend.setGeometry(QtCore.QRect(460, 130, 61, 23))
        self.pbSend.setObjectName(_fromUtf8("pbSend"))
        self.twTestPanel.addTab(self.tabManul, _fromUtf8(""))
        self.ckbTimeFlag = QtGui.QCheckBox(EspRFtestTool)
        self.ckbTimeFlag.setGeometry(QtCore.QRect(470, 480, 71, 16))
        self.ckbTimeFlag.setObjectName(_fromUtf8("ckbTimeFlag"))
        self.pbLogSave = QtGui.QPushButton(EspRFtestTool)
        self.pbLogSave.setGeometry(QtCore.QRect(470, 540, 75, 23))
        self.pbLogSave.setObjectName(_fromUtf8("pbLogSave"))
        self.pbLogClear = QtGui.QPushButton(EspRFtestTool)
        self.pbLogClear.setGeometry(QtCore.QRect(470, 510, 75, 23))
        self.pbLogClear.setObjectName(_fromUtf8("pbLogClear"))
        self.ckbShowSend = QtGui.QCheckBox(EspRFtestTool)
        self.ckbShowSend.setGeometry(QtCore.QRect(470, 460, 71, 16))
        self.ckbShowSend.setObjectName(_fromUtf8("ckbShowSend"))
        self.label_2 = QtGui.QLabel(EspRFtestTool)
        self.label_2.setGeometry(QtCore.QRect(4, 0, 48, 39))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.cbChipType = QtGui.QComboBox(EspRFtestTool)
        self.cbChipType.setGeometry(QtCore.QRect(58, 9, 95, 20))
        self.cbChipType.setObjectName(_fromUtf8("cbChipType"))
        self.cbChipType.addItem(_fromUtf8(""))
        self.cbChipType.addItem(_fromUtf8(""))
        self.label = QtGui.QLabel(EspRFtestTool)
        self.label.setGeometry(QtCore.QRect(315, 0, 48, 39))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.cbComIndex = QtGui.QComboBox(EspRFtestTool)
        self.cbComIndex.setGeometry(QtCore.QRect(213, 9, 96, 20))
        self.cbComIndex.setObjectName(_fromUtf8("cbComIndex"))
        self.cbComIndex.addItem(_fromUtf8(""))
        self.pbOpenSerial = QtGui.QPushButton(EspRFtestTool)
        self.pbOpenSerial.setEnabled(True)
        self.pbOpenSerial.setGeometry(QtCore.QRect(470, 8, 75, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbOpenSerial.sizePolicy().hasHeightForWidth())
        self.pbOpenSerial.setSizePolicy(sizePolicy)
        self.pbOpenSerial.setMinimumSize(QtCore.QSize(75, 23))
        self.pbOpenSerial.setMaximumSize(QtCore.QSize(75, 23))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Agency FB"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pbOpenSerial.setFont(font)
        self.pbOpenSerial.setAutoFillBackground(False)
        self.pbOpenSerial.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("image/button_close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbOpenSerial.setIcon(icon1)
        self.pbOpenSerial.setIconSize(QtCore.QSize(75, 25))
        self.pbOpenSerial.setObjectName(_fromUtf8("pbOpenSerial"))
        self.label_3 = QtGui.QLabel(EspRFtestTool)
        self.label_3.setGeometry(QtCore.QRect(159, 0, 48, 39))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.cbComBaud = QtGui.QComboBox(EspRFtestTool)
        self.cbComBaud.setGeometry(QtCore.QRect(369, 9, 95, 20))
        self.cbComBaud.setObjectName(_fromUtf8("cbComBaud"))
        self.cbComBaud.addItem(_fromUtf8(""))
        self.cbComBaud.addItem(_fromUtf8(""))
        self.cbComBaud.addItem(_fromUtf8(""))
        self.cbComBaud.addItem(_fromUtf8(""))
        self.cbComBaud.addItem(_fromUtf8(""))
        self.leCOM = QtGui.QLineEdit(EspRFtestTool)
        self.leCOM.setGeometry(QtCore.QRect(369, 9, 76, 20))
        self.leCOM.setObjectName(_fromUtf8("leCOM"))

        self.retranslateUi(EspRFtestTool)
        self.twTestPanel.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(EspRFtestTool)

    def retranslateUi(self, EspRFtestTool):
        EspRFtestTool.setWindowTitle(_translate("EspRFtestTool", "EspRFtestTool", None))
        self.pbOpenFile.setText(_translate("EspRFtestTool", "选择测试bin", None))
        self.pbLoadBin.setText(_translate("EspRFtestTool", "加载测试bin", None))
        self.cbLoadType.setItemText(0, _translate("EspRFtestTool", "RAM", None))
        self.cbLoadType.setItemText(1, _translate("EspRFtestTool", "Flash", None))
        self.cbWFTestMode.setItemText(0, _translate("EspRFtestTool", "TX continues", None))
        self.cbWFTestMode.setItemText(1, _translate("EspRFtestTool", "TX packet", None))
        self.cbWFTestMode.setItemText(2, _translate("EspRFtestTool", "RX packet", None))
        self.cbWFTestMode.setItemText(3, _translate("EspRFtestTool", "TX tone", None))
        self.label_4.setText(_translate("EspRFtestTool", "测试模式：", None))
        self.label_5.setText(_translate("EspRFtestTool", "信号衰减(0.25dB)：", None))
        self.leWFAtten.setText(_translate("EspRFtestTool", "0", None))
        self.cbWFDataRate.setItemText(0, _translate("EspRFtestTool", "11b 1M", None))
        self.cbWFDataRate.setItemText(1, _translate("EspRFtestTool", "11b 2M", None))
        self.cbWFDataRate.setItemText(2, _translate("EspRFtestTool", "11b 5.5M", None))
        self.cbWFDataRate.setItemText(3, _translate("EspRFtestTool", "11b 11M", None))
        self.cbWFDataRate.setItemText(4, _translate("EspRFtestTool", "11g 6M", None))
        self.cbWFDataRate.setItemText(5, _translate("EspRFtestTool", "11g 9M", None))
        self.cbWFDataRate.setItemText(6, _translate("EspRFtestTool", "11g 12M", None))
        self.cbWFDataRate.setItemText(7, _translate("EspRFtestTool", "11g 18M", None))
        self.cbWFDataRate.setItemText(8, _translate("EspRFtestTool", "11g 24M", None))
        self.cbWFDataRate.setItemText(9, _translate("EspRFtestTool", "11g 36M", None))
        self.cbWFDataRate.setItemText(10, _translate("EspRFtestTool", "11g 48M", None))
        self.cbWFDataRate.setItemText(11, _translate("EspRFtestTool", "11g 54M", None))
        self.cbWFDataRate.setItemText(12, _translate("EspRFtestTool", "11n MCS0", None))
        self.cbWFDataRate.setItemText(13, _translate("EspRFtestTool", "11n MCS1", None))
        self.cbWFDataRate.setItemText(14, _translate("EspRFtestTool", "11n MCS2", None))
        self.cbWFDataRate.setItemText(15, _translate("EspRFtestTool", "11n MCS3", None))
        self.cbWFDataRate.setItemText(16, _translate("EspRFtestTool", "11n MCS4", None))
        self.cbWFDataRate.setItemText(17, _translate("EspRFtestTool", "11n MCS5", None))
        self.cbWFDataRate.setItemText(18, _translate("EspRFtestTool", "11n MCS6", None))
        self.cbWFDataRate.setItemText(19, _translate("EspRFtestTool", "11n MCS7", None))
        self.label_6.setText(_translate("EspRFtestTool", "WiFi速率：", None))
        self.cbWFChannel.setItemText(0, _translate("EspRFtestTool", "1/2412", None))
        self.cbWFChannel.setItemText(1, _translate("EspRFtestTool", "2/2417", None))
        self.cbWFChannel.setItemText(2, _translate("EspRFtestTool", "3/2422", None))
        self.cbWFChannel.setItemText(3, _translate("EspRFtestTool", "4/2427", None))
        self.cbWFChannel.setItemText(4, _translate("EspRFtestTool", "5/2432", None))
        self.cbWFChannel.setItemText(5, _translate("EspRFtestTool", "6/2437", None))
        self.cbWFChannel.setItemText(6, _translate("EspRFtestTool", "7/2442", None))
        self.cbWFChannel.setItemText(7, _translate("EspRFtestTool", "8/2447", None))
        self.cbWFChannel.setItemText(8, _translate("EspRFtestTool", "9/2452", None))
        self.cbWFChannel.setItemText(9, _translate("EspRFtestTool", "10/2457", None))
        self.cbWFChannel.setItemText(10, _translate("EspRFtestTool", "11/2462", None))
        self.cbWFChannel.setItemText(11, _translate("EspRFtestTool", "12/2467", None))
        self.cbWFChannel.setItemText(12, _translate("EspRFtestTool", "13/2472", None))
        self.cbWFChannel.setItemText(13, _translate("EspRFtestTool", "14/2484", None))
        self.label_7.setText(_translate("EspRFtestTool", "信道选择：", None))
        self.label_8.setText(_translate("EspRFtestTool", "信道带宽：", None))
        self.cbWFBandWidth.setItemText(0, _translate("EspRFtestTool", "20M", None))
        self.cbWFBandWidth.setItemText(1, _translate("EspRFtestTool", "40M", None))
        self.pbWFStop.setText(_translate("EspRFtestTool", "stop", None))
        self.pbWFSend.setText(_translate("EspRFtestTool", "start", None))
        self.twTestPanel.setTabText(self.twTestPanel.indexOf(self.tabWF), _translate("EspRFtestTool", "wifi测试", None))
        self.cbBTTestMode.setItemText(0, _translate("EspRFtestTool", "classBT TX", None))
        self.cbBTTestMode.setItemText(1, _translate("EspRFtestTool", "classBT RX/BR", None))
        self.cbBTTestMode.setItemText(2, _translate("EspRFtestTool", "classBT RX/EDR", None))
        self.cbBTTestMode.setItemText(3, _translate("EspRFtestTool", "BLE TX", None))
        self.cbBTTestMode.setItemText(4, _translate("EspRFtestTool", "BLE TX Syncw", None))
        self.cbBTTestMode.setItemText(5, _translate("EspRFtestTool", "BLE RX", None))
        self.cbBTTestMode.setItemText(6, _translate("EspRFtestTool", "BT TX tone", None))
        self.pbBTStop.setText(_translate("EspRFtestTool", "stop", None))
        self.label_9.setText(_translate("EspRFtestTool", "信道选择：", None))
        self.lbBTPowerLevel.setText(_translate("EspRFtestTool", "功耗等级(dB)：", None))
        self.label_11.setText(_translate("EspRFtestTool", "蓝牙测试模式：", None))
        self.label_12.setText(_translate("EspRFtestTool", "是否跳频：", None))
        self.cbBTChanJmp.setItemText(0, _translate("EspRFtestTool", "No", None))
        self.cbBTChanJmp.setItemText(1, _translate("EspRFtestTool", "Yes", None))
        self.cbBTDataRate.setItemText(0, _translate("EspRFtestTool", "1M", None))
        self.cbBTDataRate.setItemText(1, _translate("EspRFtestTool", "2M", None))
        self.cbBTDataRate.setItemText(2, _translate("EspRFtestTool", "3M", None))
        self.label_13.setText(_translate("EspRFtestTool", "调制方式：", None))
        self.cbBTPowerLevel.setItemText(0, _translate("EspRFtestTool", "0", None))
        self.cbBTPowerLevel.setItemText(1, _translate("EspRFtestTool", "1", None))
        self.cbBTPowerLevel.setItemText(2, _translate("EspRFtestTool", "2", None))
        self.cbBTPowerLevel.setItemText(3, _translate("EspRFtestTool", "3", None))
        self.cbBTPowerLevel.setItemText(4, _translate("EspRFtestTool", "4", None))
        self.cbBTPowerLevel.setItemText(5, _translate("EspRFtestTool", "5", None))
        self.cbBTPowerLevel.setItemText(6, _translate("EspRFtestTool", "6", None))
        self.cbBTPowerLevel.setItemText(7, _translate("EspRFtestTool", "7", None))
        self.cbBTPowerLevel.setItemText(8, _translate("EspRFtestTool", "8", None))
        self.cbBTDataType.setItemText(0, _translate("EspRFtestTool", "1010", None))
        self.cbBTDataType.setItemText(1, _translate("EspRFtestTool", "00001111", None))
        self.cbBTDataType.setItemText(2, _translate("EspRFtestTool", "prbs9", None))
        self.label_14.setText(_translate("EspRFtestTool", "Data类型：", None))
        self.label_15.setText(_translate("EspRFtestTool", "DH类型：", None))
        self.cbBTDHType.setItemText(0, _translate("EspRFtestTool", "DH1", None))
        self.cbBTDHType.setItemText(1, _translate("EspRFtestTool", "DH3", None))
        self.cbBTDHType.setItemText(2, _translate("EspRFtestTool", "DH5", None))
        self.label_16.setText(_translate("EspRFtestTool", "负载长度(0~255)：", None))
        self.leBTPayload.setText(_translate("EspRFtestTool", "0", None))
        self.label_17.setText(_translate("EspRFtestTool", "包的身份识别：", None))
        self.cbBTSyncw.setItemText(0, _translate("EspRFtestTool", "0x71764129", None))
        self.cbBTSyncw.setItemText(1, _translate("EspRFtestTool", "custom", None))
        self.pbBTSend.setText(_translate("EspRFtestTool", "start", None))
        self.twTestPanel.setTabText(self.twTestPanel.indexOf(self.tabBT), _translate("EspRFtestTool", "BT测试 ", None))
        self.pbSend.setText(_translate("EspRFtestTool", "send", None))
        self.twTestPanel.setTabText(self.twTestPanel.indexOf(self.tabManul), _translate("EspRFtestTool", "手动测试", None))
        self.ckbTimeFlag.setText(_translate("EspRFtestTool", "显示时间", None))
        self.pbLogSave.setText(_translate("EspRFtestTool", "保存log", None))
        self.pbLogClear.setText(_translate("EspRFtestTool", "清除log", None))
        self.ckbShowSend.setText(_translate("EspRFtestTool", "显示发送", None))
        self.label_2.setText(_translate("EspRFtestTool", "芯片平台", None))
        self.cbChipType.setItemText(0, _translate("EspRFtestTool", "ESP8266", None))
        self.cbChipType.setItemText(1, _translate("EspRFtestTool", "ESP32", None))
        self.label.setText(_translate("EspRFtestTool", " 波特率 ", None))
        self.cbComIndex.setItemText(0, _translate("EspRFtestTool", "--", None))
        self.label_3.setText(_translate("EspRFtestTool", "串口选择", None))
        self.cbComBaud.setItemText(0, _translate("EspRFtestTool", "9600", None))
        self.cbComBaud.setItemText(1, _translate("EspRFtestTool", "74880", None))
        self.cbComBaud.setItemText(2, _translate("EspRFtestTool", "115200", None))
        self.cbComBaud.setItemText(3, _translate("EspRFtestTool", "921600", None))
        self.cbComBaud.setItemText(4, _translate("EspRFtestTool", "custom", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    EspRFtestTool = QtGui.QWidget()
    ui = Ui_EspRFtestTool()
    ui.setupUi(EspRFtestTool)
    EspRFtestTool.show()
    sys.exit(app.exec_())

