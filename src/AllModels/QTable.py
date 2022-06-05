import sys

from PySide6 import QtCore, QtWidgets

class MyWidget(QtWidgets.QWidget):
    
    def __init__(self,interf=None):
        super().__init__()
        self.interf=interf

        self.button = QtWidgets.QPushButton("OK")
        
        self.button.setObjectName("evilButton")
        self.text = QtWidgets.QLabel("How many ships you want to separate",
                                     alignment=QtCore.Qt.AlignCenter)
        self.box=QtWidgets.QLineEdit()
        

        self.layout = QtWidgets.QVBoxLayout(self)

        self.layout.addWidget(self.text)
        self.layout.addWidget(self.box)
        self.layout.addWidget(self.button)
        
        self.button.clicked.connect(self.magic)

        self.setStyleSheet("""
        QPushButton#evilButton{
            border-style: outset;
            border-width: 2px;
            border-color: #EAE99B;
        }

        QPushButton#evilButton:pressed {
            background-color: #0E0F1C;
        };
        
        color: #EAE99B;
        background-color: #1B2445;
        """)
        self.button.setStyleSheet("evilButton")

    @QtCore.Slot()
    def magic(self):

        try:
            value=int(self.box.text())
            if value >=500:
                self.interf.value=value
            
        except:pass
        

def startQT(interf):
    app = QtWidgets.QApplication([])
    
    widget = MyWidget(interf)
    widget.resize(200, 100)
    
    
    
    
    widget.show()
    
    sys.exit(app.exec())

if __name__=="__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(200, 100)
    widget.show()
    
    sys.exit(app.exec())