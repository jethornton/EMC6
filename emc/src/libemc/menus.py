
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import Qt
app = Qt.QApplication([])

def file_open(parent):
	options = QFileDialog.Options()
	options |= QFileDialog.DontUseNativeDialog
	fileName, _ = QFileDialog.getOpenFileName(None,"Open File", "","All Files (*);;G code Files (*.ngc)", options=options)
	if fileName:
		print(fileName)

