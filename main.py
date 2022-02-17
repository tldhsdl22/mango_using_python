import configparser
import sys
import time
from datetime import datetime
from threading import Thread

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from src.browser_controller.ChromeController import ChromeController


class MainActivity(QWidget):
    def __init__(self):
        super().__init__()
        # UI 객체 생성
        self.table = QTableWidget()
        self.text_log = QPlainTextEdit()
        self.edit_worker_cnt = QLineEdit()
        self.edit_ip_id = QLineEdit()
        self.edit_device_id = QLineEdit()

        self.rb_ip_type1 = QRadioButton('고정')
        self.rb_ip_type2 = QRadioButton('테더링')
        self.rb_ip_type3 = QRadioButton('VPN')

        # 변수 설정
        self.threads = {}
        self.ip_type = ""
        self.start_time_list = {}
        self.properties = configparser.ConfigParser()
        self.properties.read("config.ini")

        # 메소드 호출
        self.init_ui()
        self.load_settings()

    def __del__(self):
        {}

    # 셋팅값 - 전체 데이터 불러오기
    def load_settings(self):
        self.edit_device_id.setText(self.load_ini("edit_device_id"))
        self.edit_ip_id.setText(self.load_ini("edit_ip_id"))
        self.edit_worker_cnt.setText(self.load_ini("edit_worker_cnt"))

        if self.load_ini("ip_type") == "rb_ip_type1":
            self.rb_ip_type1.setChecked(True)
        elif self.load_ini("ip_type") == "rb_ip_type2":
            self.rb_ip_type2.setChecked(True)
        elif self.load_ini("ip_type") == "rb_ip_type3":
            self.rb_ip_type3.setChecked(True)
        else:
            self.rb_ip_type1.setChecked(True)

    # 셋팅값 - 불러오기
    def load_ini(self, key) -> str:
        settings = self.properties["APP SETTINGS"]
        if key in settings:
            return settings[key]
        else:
            return ""

    # 셋팅값 - 저장하기
    def save_ini(self, key, val):
        if not self.properties.has_section("APP SETTINGS"):
            self.properties.add_section("APP SETTINGS")
        self.properties.set("APP SETTINGS", key, val)
        with open("./config.ini", "w") as f:
            self.properties.write(f)

    # UI - 생성하기
    def init_ui(self):
        vb_main = QVBoxLayout()

        # Log
        vb_log = QVBoxLayout()
        label_log = QLabel("Log")
        self.text_log.setReadOnly(True)
        vb_log.addWidget(label_log)
        vb_log.addWidget(self.text_log)

        # Device Info
        vb_device_info = QVBoxLayout()
        label_device_info = QLabel("작업상태")
        self.table.setRowCount(10)
        columns = ["시작시간", "현재 상태", "아이디", "유저데이터"]
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)

        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        vb_device_info.addWidget(label_device_info)
        vb_device_info.addWidget(self.table)

        # 설정 값
        hb_preference = QHBoxLayout()

        # 메인 버튼
        vh_start = QHBoxLayout()
        btn_start = QPushButton('시작')
        btn_start.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_start.clicked.connect(self.start_work)
        btn_pause = QPushButton('일시정지')
        btn_pause.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        vh_start.addWidget(btn_start)
        vh_start.addWidget(btn_pause)

        # IP Type
        groupbox = QGroupBox('아이피 변경 방식')
        self.rb_ip_type1.res_id = "rb_ip_type1"
        self.rb_ip_type1.toggled.connect(self.save_ip_type)
        self.rb_ip_type2.res_id = "rb_ip_type2"
        self.rb_ip_type2.toggled.connect(self.save_ip_type)
        self.rb_ip_type3.res_id = "rb_ip_type3"
        self.rb_ip_type3.toggled.connect(self.save_ip_type)

        vb_ip_type = QVBoxLayout()
        vb_ip_type.addWidget(self.rb_ip_type1)
        vb_ip_type.addWidget(self.rb_ip_type2)
        vb_ip_type.addWidget(self.rb_ip_type3)
        groupbox.setLayout(vb_ip_type)

        # 작업 설정
        gb_details = QGroupBox('작업 설정')
        grid_work_type = QGridLayout()

        # 작업 설정
        grid_work_type.addWidget(QLabel('DeviceID'), 0, 0)
        self.edit_device_id.res_id = "edit_device_id"
        self.edit_device_id.textChanged.connect(self.save_edit_text)
        grid_work_type.addWidget(self.edit_device_id, 0, 1)

        grid_work_type.addWidget(QLabel('IP ID'), 1, 0)
        self.edit_ip_id.res_id = "edit_ip_id"
        self.edit_ip_id.textChanged.connect(self.save_edit_text)
        grid_work_type.addWidget(self.edit_ip_id, 1, 1)

        grid_work_type.addWidget(QLabel('동시 개수'), 2, 0)
        self.edit_worker_cnt.res_id = "edit_worker_cnt"
        self.edit_worker_cnt.textChanged.connect(self.save_edit_text)

        grid_work_type.addWidget(self.edit_worker_cnt, 2, 1)
        gb_details.setLayout(grid_work_type)

        # 설정 값 레이아웃
        hb_preference.addLayout(vh_start)
        hb_preference.addWidget(groupbox)
        hb_preference.addWidget(gb_details)

        # 레이아웃 순서
        vb_main.addLayout(vb_log)
        vb_main.addLayout(vb_device_info)
        vb_main.addLayout(hb_preference)

        self.setLayout(vb_main)
        self.setWindowTitle('Mango')
        self.setWindowIcon(QIcon('res/ico.png'))
        self.setGeometry(300, 300, 850, 500)
        self.show()

    # UI - edit text 연동
    def save_edit_text(self):
        self.save_ini(self.sender().res_id, self.sender().text())

    # UI - radio button 연동
    def save_ip_type(self):
        self.ip_type = self.sender().res_id
        self.save_ini("ip_type", self.sender().res_id)

    # UI - start button 연동
    def start_work(self):
        # 작업 시작
        try:
            worker_cnt = int(self.edit_worker_cnt.text())
        except:
            worker_cnt = 0
        for worker_idx in range(0, worker_cnt):
            if worker_idx not in self.threads:
                worker = Worker(idx=worker_idx, device_id=self.edit_device_id.text(), ip_id=self.edit_ip_id.text(), ip_type=self.ip_type)

            # UI 연동
            worker.print_log.connect(self.print_log)
            worker.print_device_info.connect(self.print_device_info)

            # 작업 등록
            self.threads[worker.idx] = worker
            worker.start()

    # 로그 - 출력
    def print_log(self, content:str):
        print(content)
        alertHtml = "<font color=\"DeepPink\">";
        notifyHtml = "<font color=\"Lime\">";
        infoHtml = "<font color=\"Aqua\">";
        endHtml = "</font><br>";

        cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.text_log.appendHtml(f'{cur_time}&nbsp;&nbsp;{content}')

    # 작업 상태 - 출력
    def print_device_info(self, idx, state, account_id='', userdata_id=''):
        print(idx, state, account_id, userdata_id)
        if state == "시작":
            cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.start_time_list[idx] = cur_time

        if idx in self.start_time_list:
            self.table.setItem(idx, 0, QTableWidgetItem(self.start_time_list[idx]))
        self.table.setItem(idx, 1, QTableWidgetItem(state))
        self.table.setItem(idx, 2, QTableWidgetItem(account_id))
        self.table.setItem(idx, 3, QTableWidgetItem(userdata_id))



class Worker(QtCore.QThread):
    print_log = QtCore.pyqtSignal(object)
    print_device_info = QtCore.pyqtSignal(int,object,object,object)

    def __init__(self, idx, device_id, ip_id, ip_type):
        QtCore.QThread.__init__(self)
        self.idx = idx
        self.device_id = device_id
        self.ip_id = ip_id
        self.ip_type = ip_type

    def run(self):
        self.print_log.emit(f'{self.idx, self.device_id, self.ip_id, self.ip_type} 작업시작')
        while True:
            controller = ChromeController()
            self.print_device_info.emit(self.idx, "시작", '', '')
            time.sleep(2)
            self.print_device_info.emit(self.idx, "동작", 'tldhsdl33', 'aaasssaassd')
            time.sleep(2)
            self.print_device_info.emit(self.idx, "완료", 'tldhsdl33', 'aaasssaassd')
            time.sleep(2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainActivity()
    sys.exit(app.exec_())




