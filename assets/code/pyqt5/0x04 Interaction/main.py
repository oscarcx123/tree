import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

import HelloWorld

def click_success():
    print("啊哈哈哈我终于成功了！")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = HelloWorld.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.pushButton.clicked.connect(click_success)
    sys.exit(app.exec_())