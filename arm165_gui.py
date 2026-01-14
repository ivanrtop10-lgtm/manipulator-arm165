# GUI для ARM165 - модуль A
import sys, time, random
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class RobotGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ARM165 Control")
        self.resize(700, 500)
        
        w = QWidget()
        self.setCentralWidget(w)
        layout = QVBoxLayout(w)
        
        self.pose_label = QLabel("Поза: ожидание...")
        self.pose_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.pose_label)
        
        self.logs_table = QTableWidget(0, 2)
        self.logs_table.setHorizontalHeaderLabels(["Время", "Действие"])
        layout.addWidget(self.logs_table)
        
        btn_layout = QHBoxLayout()
        self.cart_btn = QPushButton("Manual Cart")
        self.joint_btn = QPushButton("Manual Joint")
        self.grip_btn = QPushButton("Gripper ON")
        self.pause_btn = QPushButton("Pause")
        self.stop_btn = QPushButton("Stop")
        
        btn_layout.addWidget(self.cart_btn)
        btn_layout.addWidget(self.joint_btn)
        btn_layout.addWidget(self.grip_btn)
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_pose)
        self.timer.start(300)
        
        self.cart_btn.clicked.connect(self.cart_click)
        self.joint_btn.clicked.connect(self.joint_click)
        self.grip_btn.clicked.connect(self.grip_click)
        self.pause_btn.clicked.connect(self.pause_click)
        self.stop_btn.clicked.connect(self.stop_click)
        
        self.statusBar().showMessage("Подключен к 192.168.1.10")
    
    def update_pose(self):
        pose = [random.uniform(0, 1) for _ in range(6)]
        x, y, z = pose[:3]
        self.pose_label.setText(f"X:{x:.2f} Y:{y:.2f} Z:{z:.2f} RX:{pose[3]:.2f} RY:{pose[4]:.2f} RZ:{pose[5]:.2f}")
        self.add_log(f"Pose {pose}")
    
    def add_log(self, text):
        row = self.logs_table.rowCount()
        self.logs_table.insertRow(row)
        self.logs_table.setItem(row, 0, QTableWidgetItem(datetime.now().strftime("%H:%M:%S")))
        self.logs_table.setItem(row, 1, QTableWidgetItem(text))
        if row > 20:
            self.logs_table.removeRow(0)
    
    def cart_click(self):
        self.add_log("Manual Cart включен")
    
    def joint_click(self):
        self.add_log("Manual Joint включен")
    
    def grip_click(self):
        self.add_log("Gripper ON")
    
    def pause_click(self):
        self.add_log("Пауза")
    
    def stop_click(self):
        self.add_log("Стоп")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RobotGUI()
    window.show()
    sys.exit(app.exec_())
