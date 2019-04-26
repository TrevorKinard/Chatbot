"""
    This program is a basic demonstration of the Murphy Cult chatbot system. Upon starting the program, 5 new
    chatbots will be added to the chat room with new random names and a random denomination. The denomination
    adds a bit more personalized options to the individual bots responses. Next, an application window will
    open, showing how many bots are in each denomination, a debate window, and a start button. There is also
    dialog window with a description of the program. Clicking the start button causes the chat room to open, and
    the bots start talking to each other. They will continue talking to each other, debating the merits of
    Murpholicism, until the application is closed.

    Authors:
    Zack Thompson
    Trevor Kinard
    Brandon Michelsen
"""

# Import the necessary files for creating an application window
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from random import choice
from time import sleep
import sys
from ChatBots import ChatBotFactory


class GUI(QMainWindow):
    # Initialize the window
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Murpholicism Chatbot Civilization')
        self.setMinimumSize(.5 * app.desktop().screenGeometry().width(),
                            (5 / 9) * app.desktop().screenGeometry().height())

        # Center window
        window = self.frameGeometry()
        window.moveCenter(QDesktopWidget().availableGeometry().center())

        # Initialize used variables
        self.inquisitors = 0
        self.clerics = 0
        self.zealots = 0
        self.openmindeds = 0
        self.bots = []

        self.initUI()

    def initUI(self):
        # Menu Bar
        # Create menu bar
        self.mainMenu = self.menuBar()
        # Create help Menu Item
        self.helpitem = QAction('Help', self)
        self.mainMenu.addAction(self.helpitem)
        self.helpitem.triggered.connect(lambda: self.createDialog(title="About", message='About'))

        # Start program button
        self.start_btn = QPushButton('Start the Program', self)
        # Connect the button the main loop function
        self.start_btn.clicked.connect(self.main_loop)

        # Label for debate area
        self.label_debate = QLabel('Debate Room', self)
        self.label_debate.setAlignment(Qt.AlignCenter)

        # Group Label & Size (Inquisitors)
        self.label_Inq = QLabel('Inquisitors', self)
        self.label_Inq.setAlignment(Qt.AlignCenter)
        self.size_Inq = QLabel('1', self)
        self.size_Inq.setAlignment(Qt.AlignCenter)

        # Group Label & Size (Clerics)
        self.label_Cler = QLabel('Clerics', self)
        self.label_Cler.setAlignment(Qt.AlignCenter)
        self.size_Cler = QLabel('1', self)
        self.size_Cler.setAlignment(Qt.AlignCenter)

        # Group Label & Size (Zealots)
        self.label_Zeal = QLabel('Zealots', self)
        self.label_Zeal.setAlignment(Qt.AlignCenter)
        self.size_Zeal = QLabel('1', self)
        self.size_Zeal.setAlignment(Qt.AlignCenter)

        # Group Label & Size (Open Minded)
        self.label_OpMin = QLabel('Open Minded', self)
        self.label_OpMin.setAlignment(Qt.AlignCenter)
        self.size_OpMin = QLabel('1', self)
        self.size_OpMin.setAlignment(Qt.AlignCenter)

        # Chatbot dialog output box
        self.dialog = QTextBrowser(self)

        self.generate_bots()

    # Create a message dialog box
    def createDialog(self, title="", message=""):
        dialog = ScrollMessageBox()
        dialog.setText(open('Data/' + message).read())
        dialog.setWindowTitle(title)

        dialog.exec_()

    # Function to generate new bots
    def generate_bots(self):
        # Generate 5 new bots
        for i in range(5):
            self.bots.append(ChatBotFactory())

            # Track how many bots are added to each group
            if str(self.bots[i]) == "Inquisitor":
                self.inquisitors += 1
            elif str(self.bots[i]) == "Cleric":
                self.clerics += 1
            elif str(self.bots[i]) == "Zealot":
                self.zealots += 1
            else:
                self.openmindeds += 1

            # Update the avatars to show the proper amount of bots in each group
            self.size_Inq.setText(str(self.inquisitors))
            self.size_Cler.setText(str(self.clerics))
            self.size_Zeal.setText(str(self.zealots))
            self.size_OpMin.setText(str(self.openmindeds))

            # Update the window
            QApplication.processEvents()

    # Function for running all the bots
    def main_loop(self):
        # Start conversation
        bot = choice(self.bots)
        conv = bot.random_response()
        self.dialog.append(bot.name + " (" + str(bot) + "): " + str(conv))

        # Create thread to run Chatbots
        self.chatterer = Chatter(conv, self.bots, 0)
        # Update text output from emitted data
        self.chatterer.signal.connect(self.dialog.append)
        # Update group numbers
        self.chatterer.signal_Inq.connect(self.size_Inq.setText)
        self.chatterer.signal_Cler.connect(self.size_Cler.setText)
        self.chatterer.signal_Zeal.connect(self.size_Zeal.setText)
        self.chatterer.signal_OpMin.connect(self.size_OpMin.setText)

        self.chatterer.start()

        # Update the window
        QApplication.processEvents()

    # Resize Gui elements during GUI resizing events
    def resizeEvent(self, *args, **kwargs):
        # Resize Button
        self.start_btn.setGeometry(4, 25, self.width() - 8, 20)

        # Resize label
        self.label_debate.setGeometry(4, self.start_btn.height() + self.start_btn.y() + 8, self.width() - 8, 20)

        # Resize Group labels
        self.label_Inq.setGeometry(4, self.label_debate.height() + self.label_debate.y() + 8, self.width() / 4 - 4, 20)
        self.size_Inq.setGeometry(self.label_Inq.x(), self.label_Inq.y() + self.label_Inq.height() + 4, self.label_Inq.width(), self.label_Inq.height())

        self.label_Cler.setGeometry(self.label_Inq.width() + self.label_Inq.x() + 4, self.label_debate.height() + self.label_debate.y() + 8, self.width() / 4 - 4, 20)
        self.size_Cler.setGeometry(self.label_Cler.x(), self.label_Cler.y() + self.label_Cler.height() + 4, self.label_Cler.width(), self.label_Cler.height())

        self.label_Zeal.setGeometry(self.label_Cler.width() + self.label_Cler.x() + 4, self.label_debate.height() + self.label_debate.y() + 8, self.width() / 4 - 4, 20)
        self.size_Zeal.setGeometry(self.label_Zeal.x(), self.label_Zeal.y() + self.label_Zeal.height() + 4, self.label_Zeal.width(), self.label_Zeal.height())

        self.label_OpMin.setGeometry(self.label_Zeal.width() + self.label_Zeal.x() + 4, self.label_debate.height() + self.label_debate.y() + 8, self.width() / 4 - 4, 20)
        self.size_OpMin.setGeometry(self.label_OpMin.x(), self.label_OpMin.y() + self.label_OpMin.height() + 4, self.label_OpMin.width(), self.label_OpMin.height())

        # Resize output text box
        self.dialog.setGeometry(4, self.size_OpMin.height() + self.size_OpMin.y() + 8, self.width() - 8, self.height() - (self.size_OpMin.height() + self.size_OpMin.y() + 12))


# Custom message dialog
class ScrollMessageBox(QMessageBox):
    def __init__(self, *args, **kwargs):
        # Load in parent clss
        QMessageBox.__init__(self, *args, **kwargs)

        # Add scroll area
        scroll = QScrollArea(self)
        # Set scroll area resizable
        scroll.setWidgetResizable(True)

        # Widget to hold the content
        self.content = QWidget()
        # Set widget to scroll area
        scroll.setWidget(self.content)
        # create layout for content
        self.grid = QVBoxLayout(self.content)

        self.layout().addWidget(scroll, 0, 0, 1, self.layout().columnCount())
        self.setStyleSheet("QScrollArea{min-width:300 px; min-height: 300px}")

    def setText(self, p_str):
        label = QLabel(p_str, self)
        label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.grid.addWidget(label)


# Thread to run debating
class Chatter(QThread):
    # Signals linked to main thread
    signal = pyqtSignal(str)
    signal_Inq = pyqtSignal(str)
    signal_Cler = pyqtSignal(str)
    signal_Zeal = pyqtSignal(str)
    signal_OpMin = pyqtSignal(str)

    def __init__(self, conv, bots, time_count):
        QThread.__init__(self)
        # Save passed variables in class
        self.conv = conv
        self.bots = bots
        self.time_count = time_count

    def run(self):
        while True:
            conv_bot = choice(self.bots)

            # Replace twp old Chatbots with new ones
            if not self.time_count % 50 and self.time_count:
                self.bots[choice(range(len(self.bots)))] = ChatBotFactory()
                self.bots[choice(range(len(self.bots)))] = ChatBotFactory()
            # If a certain amount of time has passed, generate a random response (keeps the conversation dynamic)
            elif not self.time_count % 10 and self.time_count:
                self.conv = conv_bot.random_response()
            else:
                # Otherwise, continue with the previous conversation
                self.conv = conv_bot.response(self.conv)

            # Return response to main process
            self.signal.emit(conv_bot.name + " (" + str(conv_bot) + "): " + str(self.conv))

            # Update the time count
            self.time_count += 1
            sleep(0.5)

    def track_bots(self):
        for i in range(len(self.bots)):
            # Track how many bots are added to each group
            if str(self.bots[i]) == "Inquisitor":
                self.inquisitors += 1
            elif str(self.bots[i]) == "Cleric":
                self.clerics += 1
            elif str(self.bots[i]) == "Zealot":
                self.zealots += 1
            else:
                self.openmindeds += 1

            # Update the avatars to show the proper amount of bots in each group
            self.signal_Inq.emit(str(self.inquisitors))
            self.signal_Cler.emit(str(self.clerics))
            self.signal_Zeal.emit(str(self.zealots))
            self.signal_OpMin.emit(str(self.openmindeds))


if __name__ == "__main__":
    # Multi-Resolution Support
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Create GUI
    app = QApplication(sys.argv)
    Athena = GUI()
    Athena.show()
    sys.exit(app.exec_())