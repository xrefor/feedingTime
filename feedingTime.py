import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from datetime import datetime

FILENAME = "feedLog.log"

class feedingTime(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        layout = QVBoxLayout()
        #PyQt Elements
        self.feedList = QListWidget()
        self.label = QLabel(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),self)
        self.button = QPushButton("Add time")
        self.info = QLabel("Baby was last fed:")
        self.buttonDelete = QPushButton("Delete oldest")
        #Add Widgets
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.info)
        layout.addWidget(self.feedList)
        layout.addWidget(self.buttonDelete)
        self.setLayout(layout)
        #Timer counting every second, showing date in realtime
        self.timer = QTimer(self.label)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.displayTime)
        self.timer.start()

        self.button.clicked.connect(self.feedAdd)
        self.buttonDelete.clicked.connect(self.deleteOldest)

        self.loadOldData()

    def deleteOldest(self):
        self.feedList.takeItem(self.feedList.count() - 1)
        lines = open(FILENAME).readlines()
        with open(FILENAME, 'w') as f:
            f.writelines(lines[1:])

    def feedAdd(self):
        date = self.label.text()
        self.feedList.addItem(date)
        f = open(FILENAME, 'a')
        f.write(date + '\n')
        f.close()
        self.feedList.sortItems(Qt.DescendingOrder) # change to AscendingOrder if want inverted order

    def fillData(self, lines):
        for line in lines:
            self.feedList.addItem(line.rstrip())

    def loadOldData(self):
        try:
            file = open(FILENAME)
            lines = file.readlines()
            self.fillData(lines)
        except IOError:
            print "File" + FILENAME + "not found, skipping..."

    def displayTime(self):
        self.label.setText(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = feedingTime()
    dialog.show()
    sys.exit(app.exec_())
