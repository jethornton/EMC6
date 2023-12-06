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
		text = open(gcode_file).read()
		parent.gcode_pte.setPlainText(text)

	base = os.path.basename(gcode_file)
	if parent.file_lb_exists:
		parent.file_lb.setText(f'G code: {base}')
		parent.file_lb.setCenterOnScroll(True)

def file_reload(parent):
	gcode_file = parent.status.file 
	print(gcode_file)
	# Force a sync of the interpreter, which writes out the var file.
	parent.command.task_plan_synch()
	parent.command.wait_complete()
	parent.command.program_open(gcode_file)

	'''
	options = QFileDialog.Options()
	options |= QFileDialog.DontUseNativeDialog
	fileName, _ = QFileDialog.getOpenFileName(None,"Open File", "","All Files (*);;G code Files (*.ngc)", options=options)
	if fileName:
		print(fileName)
	'''
