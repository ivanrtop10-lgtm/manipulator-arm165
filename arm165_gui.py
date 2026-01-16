import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtCore import QTimer
import random
from datetime import datetime

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui',self)
        self.t=QTimer()
        self.t.timeout.connect(self.p)
        self.t.start(500)
        self.manualCartButton.clicked.connect(lambda:self.l("Manual Cart"))
        self.manualJointButton.clicked.connect(lambda:self.l("Manual Joint"))
        self.gripperOnButton.clicked.connect(lambda:self.l("Gripper ON"))
        self.pauseButton.clicked.connect(lambda:self.l("Pause"))
        self.stopButton.clicked.connect(lambda:self.l("Stop"))
        self.logs=[]
    
    def p(self):
        pose=[round(random.uniform(-0.5,0.8),3)for _ in range(6)]
        self.poseLabel.setText(f"Actual tool pose: X:{pose[0]:.3f} Y:{pose[1]:.3f} Z:{pose[2]:.3f} RX:{pose[3]:.3f} RY:{pose[4]:.3f} RZ:{pose[5]:.3f}")
        self.l(f"Pose: {pose}")
    
    def l(self,msg):
        t=datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"{t} {msg}")
        self.logText.setPlainText("\n".join(self.logs[-20:]))

app=QApplication(sys.argv)
w=GUI()
w.show()
sys.exit(app.exec_())
