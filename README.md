import sys
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from fake_motion import RobotControl, Waypoint


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ARM165 Control")
        self.resize(800, 600)
        self.logs = []
        self.robot = RobotControl()
        self.robot.connect()
        self.path = [
            Waypoint([0.3, 0.2, 0.1, 0, 0, 1.57]),
            Waypoint([0.4, 0.0, 0.1, 0, 0, 1.57]),
            Waypoint([0.3, -0.2, 0.1, 0, 0, 1.57]),
        ]
        self.statusBar().showMessage("Связь с 192.168.1.10 (FAKE API)")
        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_pose)
        self.timer.start(500)

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.pose = QLabel("Actual tool pose: --")
        self.pose.setStyleSheet("font-size:16px;")
        layout.addWidget(self.pose)

        self.log_box = QTextEdit(readOnly=True)
        self.log_box.setMaximumHeight(250)
        layout.addWidget(self.log_box)

        btn_layout = QHBoxLayout()
        self.btns = {
            "cart": QPushButton("Manual Cart"),
            "joint": QPushButton("Manual Joint"),
            "grip": QPushButton("Gripper ON"),
            "pause": QPushButton("Pause"),
            "stop": QPushButton("Stop"),
            "play": QPushButton("Play path"),
        }

        for btn in self.btns.values():
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)
        self.connect_buttons()

    def connect_buttons(self):
        self.btns["cart"].clicked.connect(self.on_cart)
        self.btns["joint"].clicked.connect(self.on_joint)
        self.btns["grip"].clicked.connect(self.on_grip)
        self.btns["pause"].clicked.connect(self.on_pause)
        self.btns["stop"].clicked.connect(self.on_stop)
        self.btns["play"].clicked.connect(self.on_play)

    def update_pose(self):
        pos = self.robot.getToolPosition()
        x, y, z, rx, ry, rz = pos
        self.pose.setText(
            f"Actual tool pose: X:{x:.3f} Y:{y:.3f} Z:{z:.3f} RX:{rx:.3f} RY:{ry:.3f} RZ:{rz:.3f}"
        )
        self.add_log(f"Pose: {pos}")

    def add_log(self, msg):
        t = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"{t} {msg}")
        self.log_box.setPlainText("\n".join(self.logs[-30:]))

    def on_cart(self):
        self.robot.manualCartMode()
        self.add_log("Manual Cart mode")

    def on_joint(self):
        self.robot.manualJointMode()
        self.add_log("Manual Joint mode")

    def on_grip(self):
        if self.robot.tool_on:
            self.robot.toolOFF()
            self.add_log("Gripper OFF")
        else:
            self.robot.toolON()
            self.add_log("Gripper ON")

    def on_pause(self):
        self.robot.pause()
        self.add_log("Program pause")

    def on_stop(self):
        self.robot.stop()
        self.add_log("Program stop")

    def on_play(self):
        self.robot.clearProgram()
        for wp in self.path:
            self.robot.addMoveToPointL([wp])
        self.robot.play()
        self.add_log("Play dataset path")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
