# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uitest.ui'
#
# Created: Fri Nov 10 11:49:38 2017
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
        EspRFtestTool.setEnabled(True)
        EspRFtestTool.resize(550, 550)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EspRFtestTool.sizePolicy().hasHeightForWidth())
        EspRFtestTool.setSizePolicy(sizePolicy)
        EspRFtestTool.setMinimumSize(QtCore.QSize(550, 550))
        EspRFtestTool.setMaximumSize(QtCore.QSize(550, 550))
        EspRFtestTool.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.horizontalLayoutWidget = QtGui.QWidget(EspRFtestTool)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 551, 51))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout_1 = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_1.setContentsMargins(5, -1, 5, -1)
        self.horizontalLayout_1.setObjectName(_fromUtf8("horizontalLayout_1"))
        self.label_2 = QtGui.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_1.addWidget(self.label_2)
        self.cbChipType = QtGui.QComboBox(self.horizontalLayoutWidget)
        self.cbChipType.setObjectName(_fromUtf8("cbChipType"))
        self.cbChipType.addItem(_fromUtf8(""))
        self.cbChipType.addItem(_fromUtf8(""))
        self.horizontalLayout_1.addWidget(self.cbChipType)
        self.label_3 = QtGui.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_1.addWidget(self.label_3)
        self.cbComIndex = QtGui.QComboBox(self.horizontalLayoutWidget)
        self.cbComIndex.setObjectName(_fromUtf8("cbComIndex"))
        self.cbComIndex.addItem(_fromUtf8(""))
        self.horizontalLayout_1.addWidget(self.cbComIndex)
        self.label = QtGui.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_1.addWidget(self.label)
        self.cbComBaud = QtGui.QComboBox(self.horizontalLayoutWidget)
        self.cbComBaud.setObjectName(_fromUtf8("cbComBaud"))
        self.cbComBaud.addItem(_fromUtf8(""))
        self.cbComBaud.addItem(_fromUtf8(""))
        self.cbComBaud.addItem(_fromUtf8(""))
        self.cbComBaud.addItem(_fromUtf8(""))
        self.horizontalLayout_1.addWidget(self.cbComBaud)
        self.pbOpenSerial = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pbOpenSerial.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbOpenSerial.sizePolicy().hasHeightForWidth())
        self.pbOpenSerial.setSizePolicy(sizePolicy)
        self.pbOpenSerial.setObjectName(_fromUtf8("pbOpenSerial"))
        self.horizontalLayout_1.addWidget(self.pbOpenSerial)
        self.line = QtGui.QFrame(EspRFtestTool)
        self.line.setGeometry(QtCore.QRect(-3, 40, 611, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayoutWidget = QtGui.QWidget(EspRFtestTool)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 50, 551, 71))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout_11 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setContentsMargins(5, -1, 5, -1)
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setMargin(0)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.pbLoadBin = QtGui.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbLoadBin.sizePolicy().hasHeightForWidth())
        self.pbLoadBin.setSizePolicy(sizePolicy)
        self.pbLoadBin.setObjectName(_fromUtf8("pbLoadBin"))
        self.horizontalLayout_5.addWidget(self.pbLoadBin)
        self.line_3 = QtGui.QFrame(self.verticalLayoutWidget)
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.horizontalLayout_5.addWidget(self.line_3)
        self.label_4 = QtGui.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_5.addWidget(self.label_4)
        self.line_4 = QtGui.QFrame(self.verticalLayoutWidget)
        self.line_4.setFrameShape(QtGui.QFrame.VLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.horizontalLayout_5.addWidget(self.line_4)
        self.pbOpenFile = QtGui.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbOpenFile.sizePolicy().hasHeightForWidth())
        self.pbOpenFile.setSizePolicy(sizePolicy)
        self.pbOpenFile.setObjectName(_fromUtf8("pbOpenFile"))
        self.horizontalLayout_5.addWidget(self.pbOpenFile)
        self.leFilePath = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.leFilePath.setEnabled(False)
        self.leFilePath.setObjectName(_fromUtf8("leFilePath"))
        self.horizontalLayout_5.addWidget(self.leFilePath)
        self.verticalLayout_11.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.prbLoad = QtGui.QProgressBar(self.verticalLayoutWidget)
        self.prbLoad.setProperty("value", 0)
        self.prbLoad.setObjectName(_fromUtf8("prbLoad"))
        self.horizontalLayout_7.addWidget(self.prbLoad)
        self.verticalLayout_11.addLayout(self.horizontalLayout_7)
        self.line_2 = QtGui.QFrame(EspRFtestTool)
        self.line_2.setGeometry(QtCore.QRect(0, 120, 911, 20))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.tabWidget = QtGui.QTabWidget(EspRFtestTool)
        self.tabWidget.setGeometry(QtCore.QRect(10, 140, 533, 151))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tbSerial = QtGui.QTextBrowser(EspRFtestTool)
        self.tbSerial.setGeometry(QtCore.QRect(10, 300, 531, 241))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(200)
        sizePolicy.setHeightForWidth(self.tbSerial.sizePolicy().hasHeightForWidth())
        self.tbSerial.setSizePolicy(sizePolicy)
        self.tbSerial.setObjectName(_fromUtf8("tbSerial"))
        self.pbComIndex = QtGui.QPushButton(EspRFtestTool)
        self.pbComIndex.setGeometry(QtCore.QRect(213, 14, 80, 22))
        self.pbComIndex.setText(_fromUtf8(""))
        self.pbComIndex.setObjectName(_fromUtf8("pbComIndex"))
        self.pbComIndex_2 = QtGui.QPushButton(EspRFtestTool)
        self.pbComIndex_2.setGeometry(QtCore.QRect(293, 13, 18, 22))
        self.pbComIndex_2.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("image/combobox2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbComIndex_2.setIcon(icon)
        self.pbComIndex_2.setIconSize(QtCore.QSize(18, 22))
        self.pbComIndex_2.setObjectName(_fromUtf8("pbComIndex_2"))

        self.retranslateUi(EspRFtestTool)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(EspRFtestTool)

    def retranslateUi(self, EspRFtestTool):
        EspRFtestTool.setWindowTitle(_translate("EspRFtestTool", "EspRFtestTool", None))
        self.label_2.setText(_translate("EspRFtestTool", "芯片平台", None))
        self.cbChipType.setItemText(0, _translate("EspRFtestTool", "ESP32", None))
        self.cbChipType.setItemText(1, _translate("EspRFtestTool", "ESP8266", None))
        self.label_3.setText(_translate("EspRFtestTool", "串口选择", None))
        self.cbComIndex.setItemText(0, _translate("EspRFtestTool", " ", None))
        self.label.setText(_translate("EspRFtestTool", " 波特率 ", None))
        self.cbComBaud.setItemText(0, _translate("EspRFtestTool", "9600", None))
        self.cbComBaud.setItemText(1, _translate("EspRFtestTool", "74880", None))
        self.cbComBaud.setItemText(2, _translate("EspRFtestTool", "115200", None))
        self.cbComBaud.setItemText(3, _translate("EspRFtestTool", "921600", None))
        self.pbOpenSerial.setText(_translate("EspRFtestTool", "打开串口", None))
        self.pbLoadBin.setText(_translate("EspRFtestTool", "加载测试bin", None))
        self.label_4.setText(_translate("EspRFtestTool", "  ", None))
        self.pbOpenFile.setText(_translate("EspRFtestTool", "选择测试bin", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("EspRFtestTool", "wifi测试", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("EspRFtestTool", "BT测试 ", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("EspRFtestTool", "手动测试", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    EspRFtestTool = QtGui.QDialog()
    ui = Ui_EspRFtestTool()
    ui.setupUi(EspRFtestTool)
    EspRFtestTool.show()
    sys.exit(app.exec_())

