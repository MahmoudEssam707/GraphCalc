from PySide2.QtWidgets import QApplication
import sys
from gui import FunctionPlotterApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FunctionPlotterApp()
    ex.show()
    sys.exit(app.exec_())