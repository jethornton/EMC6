import os

from PyQt5.QtWidgets import QFileDialog
from PyQt5 import Qt
app = Qt.QApplication([])

def file_open(parent):
	if os.path.isdir(os.path.expanduser('~/linuxcnc/nc_files')):
		gcode_dir = os.path.expanduser('~/linuxcnc/nc_files')
	else:
		gcode_dir = os.path.expanduser('~/')
	fileName = QFileDialog.getOpenFileName(None,
	caption="Select Configuration INI File", directory=gcode_dir,
	filter='*.ngc *.NGC', options=QFileDialog.DontUseNativeDialog,)
	gcode_file = fileName[0]
	if gcode_file:
		parent.command.program_open(gcode_file)

	base = os.path.basename(gcode_file)
	if parent.file_lb_exists:
		parent.file_lb.setText(f'G code: {base}')

	'''
	options = QFileDialog.Options()
	options |= QFileDialog.DontUseNativeDialog
	fileName, _ = QFileDialog.getOpenFileName(None,"Open File", "","All Files (*);;G code Files (*.ngc)", options=options)
	if fileName:
		print(fileName)
	'''
