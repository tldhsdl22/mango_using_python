import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.uic.properties import QtWidgets

alertHtml = "<font color=\"DeepPink\">";
notifyHtml = "<font color=\"Lime\">";
infoHtml = "<font color=\"Aqua\">";
endHtml = "</font><br>";


class MainActivity(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vbMain = QVBoxLayout()

        # Log
        vbLog = QVBoxLayout()
        labelLog = QLabel("Log")
        self.textLog = QPlainTextEdit()
        self.textLog.setReadOnly(True)
        self.textLog.appendPlainText('Simple Test')
        vbLog.addWidget(labelLog)
        vbLog.addWidget(self.textLog)

        # Device Info
        vbDeviceInfo = QVBoxLayout()
        labelDeviceInfo = QLabel("작업상태")
        self.table = QTableWidget()
        self.table.setRowCount(10)
        columns = ["시작시간", "현재 상태", "아이디", "유저데이터"]
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)

        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        vbDeviceInfo.addWidget(labelDeviceInfo)
        vbDeviceInfo.addWidget(self.table)

        # 설정 값
        hbPreference = QHBoxLayout()

        # 메인 버튼
        vhStartBtn = QHBoxLayout()
        btnStart = QPushButton('시작')
        btnStart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btnPause = QPushButton('일시정지')
        btnPause.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        vhStartBtn.addWidget(btnStart)
        vhStartBtn.addWidget(btnPause)

        # IP Type
        groupbox = QGroupBox('아이피 변경 방식')
        self.rbFixed = QRadioButton('고정')
        self.rbTethering = QRadioButton('테더링')
        self.rbVPN = QRadioButton('VPN')
        self.rbFixed.setChecked(True)

        vbIPType = QVBoxLayout()
        vbIPType.addWidget(self.rbFixed)
        vbIPType.addWidget(self.rbTethering)
        vbIPType.addWidget(self.rbVPN)
        groupbox.setLayout(vbIPType)

        # 작업 설정
        gbDetails = QGroupBox('작업 설정')
        gridWorkType = QGridLayout()

        # 작업 설정
        gridWorkType.addWidget(QLabel('DeviceID'), 0, 0)
        self.editDeviceID = QLineEdit()
        gridWorkType.addWidget(self.editDeviceID, 0, 1)

        gridWorkType.addWidget(QLabel('IP ID'), 1, 0)
        self.editIpId = QLineEdit()
        gridWorkType.addWidget(self.editIpId, 1, 1)

        gridWorkType.addWidget(QLabel('동시 개수'), 2, 0)
        self.editBrowserCnt = QLineEdit()
        gridWorkType.addWidget(self.editBrowserCnt, 2, 1)
        gbDetails.setLayout(gridWorkType)

        # 설정 값 레이아웃
        hbPreference.addLayout(vhStartBtn)
        hbPreference.addWidget(groupbox)
        hbPreference.addWidget(gbDetails)

        # 레이아웃 순서
        vbMain.addLayout(vbLog)
        vbMain.addLayout(vbDeviceInfo)
        vbMain.addLayout(hbPreference)

        self.setLayout(vbMain)
        self.setWindowTitle('Mango')
        self.setWindowIcon(QIcon('res/ico.png'))
        self.setGeometry(300, 300, 850, 500)
        self.show()

    def testLog(self):
        self.printLog("test")

    def printLog(self, str):
        self.textLog.appendHtml(str)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainActivity()
    sys.exit(app.exec_())
