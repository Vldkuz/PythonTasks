from front.front import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ColorChanger()
    window.show()
    sys.exit(app.exec())
