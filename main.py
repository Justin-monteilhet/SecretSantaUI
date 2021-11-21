import sys
from collections import Counter
from PIL import Image

from PyQt6.QtWidgets import (
        QApplication,
        QWidget,
        QLineEdit,
        QPushButton,
        QTextEdit,
        QVBoxLayout,
        QLabel,
        QMainWindow,
        QDialog,
        QDialogButtonBox,
        QScrollArea
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

AlignCenter = Qt.AlignmentFlag.AlignCenter
ScrollBarAlwaysOn, ScrollBarAlwaysOff = Qt.ScrollBarPolicy.ScrollBarAlwaysOn, Qt.ScrollBarPolicy.ScrollBarAlwaysOff

from cmdVersion import list_to_couples

class ErrorDialog(QDialog):
    def __init__(self, msg:str):
        super().__init__()

        self.setWindowTitle("Erreur")

        QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        message = QLabel(msg)
        message.setStyleSheet('color : black;')
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class App(QMainWindow):

    def __init__(self):
        super().__init__()

        self.icon = QIcon('./icon.ico')
        self.title = 'Père Noël Canadien'
        self.changeSize((500, 100))
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)

        self.widget = QWidget(self)
        self.widget.setProperty('background', True)
        self.setCentralWidget(self.scroll)
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.background = './background.jpg'

        self.scroll.setWidget(self.widget)
        self.widgets = None
        self.updateWidgets(self.getWidget('baseWidget'))

        self.numberPlayers = None
        self.registeredPlayers = None

    def updateWidgets(self, widgets):
        self.clearLayout()
        for wid in widgets.values() : self.layout.addWidget(wid)
        self.widgets = widgets
        self.resizeBackground()

    def sendNumber(self):
        txt = self.widgets.get('inputNumber').text()
        if txt.isdigit():
            self.numberPlayers = int(txt)
        else:
            self.execErrorDialog('Veuillez entrer un nombre.')
            self.updateWidgets(self.getWidget('baseWidget'))
            return

        if self.numberPlayers < 3 :
            self.execErrorDialog('Veuillez entrer un nombre supérieur à 2.')
            self.updateWidgets(self.getWidget('baseWidget'))
            return

        self.changeSize((500, 300))
        self.updateWidgets(self.getWidget('registerPlayersWidget'))

    def sendPlayers(self):
        players = [textInput.text() for textInput in filter(lambda w:isinstance(w, QLineEdit), self.widgets.values())]
        if not all(map(bool, players)) or not all([i == 1 for i in Counter(players).values()]) :    # check for occurences and input emptyness
            self.execErrorDialog('Veuillez remplir tous les champs par des noms uniques.')
            return

        self.registeredPlayers = list(map(str.title, players))
        self.changeSize((500, 200))
        self.updateWidgets(self.getWidget('finalWidget'))

    def changeSize(self, s):
        self.size = s
        self.setFixedSize(QSize(*self.size))

    @staticmethod
    def execErrorDialog(s:str):
        dlg = ErrorDialog(s)
        dlg.setWindowTitle('Erreur')

        dlg.exec()

    def clearLayout(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

    def getWidget(self, w:str):

        elements = {}

        if w == 'baseWidget' :

            elements['inputNumberLabel'] = QLabel('Nombre de joueurs : ')
            elements['inputNumber'] =  QLineEdit()
            elements['sendNumber'] = QPushButton('Valider', clicked=self.sendNumber)

            elements.get('inputNumberLabel').setAlignment(AlignCenter)
            elements.get('inputNumber').setAlignment(AlignCenter)

        elif w == 'registerPlayersWidget':
            for i in range(1, self.numberPlayers+1):
                elements[f'label{i}'] = QLabel(f'Joueur {i}')
                elements[f'input{i}'] = QLineEdit()

            elements['sendPlayers'] = QPushButton('Valider', clicked=self.sendPlayers)
            for item, value in elements.items():
                if item.startswith('label') or item.startswith('input'): value.setAlignment(AlignCenter)

        elif w == 'finalWidget':
            textEdit = QTextEdit()
            binomes = list_to_couples(self.registeredPlayers)
            output = '<br/>'.join([f'{giver} offre à {given}.' for giver, given in binomes.items()])
            textEdit.setHtml(output)
            textEdit.setReadOnly(True)

            elements['headLabel'] = QLabel('Voici les différents binômes :')
            elements['binomesOutput'] = textEdit

            elements.get('headLabel').setAlignment(AlignCenter)
            elements.get('binomesOutput').setAlignment(AlignCenter)

        else : return

        # for item, value in elements.items():
        #     if isinstance(value, QLabel):
        #         value.setStyleSheet("color : white; font-size : 15px; font-weight: bold;")
        #
        #     if isinstance(value, QLineEdit):
        #         value.setStyleSheet("background-color : #507856; color : white; font-size : 13px;")
        #
        #     if isinstance(value, QTextEdit):
        #         value.setStyleSheet("background-color : #507856; font-size : 15px;")
        #
        #     if isinstance(value, QPushButton):
        #         value.setStyleSheet("background-color : #1E792C;")

        return elements

    def resizeBackground(self):
        bg = Image.open(self.background)
        bgSize = bg.size
        winSize = self.size
        ratios = (winSize[0] / bgSize[0], winSize[1] / bgSize[1])
        bgSize = bgSize[0] * max(ratios), bgSize[1] * max(ratios)
        bgSize = map(int, bgSize)
        bg = bg.resize(bgSize, Image.ANTIALIAS)
        bg.save(self.background)

app = QApplication(sys.argv)
window = App()

stylesheet = f"""
            
            QWidget[background="true"]{{
                background-image : url({window.background});
                height:auto;
                width:auto;
            }}
            

            QLabel{{
                color : white; 
                font-size : 15px; 
                font-weight: bold;
            }}

            QLineEdit{{
                background-color : #507856; 
                color : white; 
                font-size : 13px;
            }}

            QTextEdit{{
                background-color : #507856; 
                font-size : 15px;
            }}

            QPushButton{{
                background-color : #1E792C;
            }}

"""

app.setStyleSheet(stylesheet)

window.show()
app.exec()
