import os

from PyQt5.QtWidgets import QFileDialog
from PyQt5 import Qt
app = Qt.QApplication([])

from libemc import editor

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

def file_reload(parent):
	gcode_file = parent.status.file 
	# Force a sync of the interpreter, which writes out the var file.
	parent.command.task_plan_synch()
	parent.command.wait_complete()
	parent.command.program_open(gcode_file)
	if parent.start_line_lb_exists:
		parent.start_line_lb.setText('')
	editor.clear_highlight(parent)


