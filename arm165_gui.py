import sys,random
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ARM165 Control")
        self.resize(800,600)
        w=QWidget()
        self.setCentralWidget(w)
        l=QVBoxLayout(w)
        self.pose=QLabel("Actual tool pose: --")
        self.pose.setStyleSheet("font-size:16px;")
        l.addWidget(self.pose)
        self.logs=QTextEdit()
        self.logs.setMaximumHeight(250)
        l.addWidget(self.logs)
        b=QHBoxLayout()
        self.cart=QPushButton("Manual Cart")
        self.joint=QPushButton("Manual Joint")
        self.grip=QPushButton("Gripper ON")
        self.pause=QPushButton("Pause")
        self.stop=QPushButton("Stop")
        b.addWidget(self.cart)
        b.addWidget(self.joint)
        b.addWidget(self.grip)
        b.addWidget(self.pause)
        b.addWidget(self.stop)
        l.addLayout(b)
        self.timer=QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(500)
        self.cart.clicked.connect(lambda:self.log("Manual Cart"))
        self.joint.clicked.connect(lambda:self.log("Manual Joint"))
        self.grip.clicked.connect(lambda:self.log("Gripper ON"))
        self.pause.clicked.connect(lambda:self.log("Pause"))
        self.stop.clicked.connect(lambda:self.log("Stop"))
        self.log_list=[]
        self.statusBar().showMessage("Сязь с 192.168.1.10")
    
    def update(self):
        pose=[round(random.uniform(-0.5,0.8),3) for _ in range(6)]
        self.pose.setText(f"Actual tool pose: X:{pose[0]} Y:{pose[1]} Z:{pose[2]} RX:{pose[3]} RY:{pose[4]} RZ:{pose[5]}")
        self.log(f"Pose: {pose}")
    
    def log(self,msg):
        t=datetime.now().strftime("%H:%M:%S")
        self.log_list.append(f"{t} {msg}")
        self.logs.setPlainText("\n".join(self.log_list[-20:]))

app=QApplication(sys.argv)
gui=GUI()
gui.show()
sys.exit(app.exec_())
