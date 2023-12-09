from functools import partial

from PyQt6.QtWidgets import QLabel, QComboBox, QPlainTextEdit, QListWidget
from PyQt6.QtGui import QTextCursor

import linuxcnc

from libemc import commands
from libemc import editor

def set_labels(parent):
	label_list = ['status_lb', 'file_lb',
	'dro_lb_x', 'dro_lb_y', 'dro_lb_z',
	'motion_line_lb', 'start_line_lb']
	children = parent.findChildren(QLabel)
	found_label_list = []
	for child in children:
		found_label_list.append(child.objectName())

	for label in label_list:
		if label in found_label_list:
			setattr(parent, f'{label}_exists', True)
		else:
			setattr(parent, f'{label}_exists', False)

def load_combos(parent):
	combo_list = ['jog_modes_cb', 'jog_increments_cb']
	children = parent.findChildren(QComboBox)
	found_combo_list = []
	for child in children:
		found_combo_list.append(child.objectName())
	if 'jog_modes_cb' in found_combo_list:
		parent.jog_modes_cb.addItem('Incremental', 'incremental')
		parent.jog_modes_cb.addItem('Continuous', 'continuous')

	if 'jog_increments_cb' in found_combo_list:
		increments = parent.inifile.find('DISPLAY', 'INCREMENTS') or False
		if increments:
			for item in increments.split():
				data = ''
				for char in item:
					if char.isdigit() or char == '.':
						data += char
				parent.jog_increments_cb.addItem(item, float(data))

def set_buttons(parent):
	if parent.status.task_state == linuxcnc.STATE_ESTOP_RESET:
		commands.estop_toggle(parent)

def get_list_widgets(parent):
	if parent.findChild(QListWidget, 'mdi_history_lw').objectName():
		parent.mdi_history_lw_exists = True
	else:
		parent.mdi_history_lw_exists = False

def get_pte(parent):
	if parent.findChild(QPlainTextEdit, 'gcode_pte'):
		parent.gcode_pte_exists = True
		parent.last_line = parent.status.motion_line
		parent.gcode_pte.setCenterOnScroll(True)
		parent.gcode_pte.ensureCursorVisible()
		parent.gcode_pte.viewport().installEventFilter(parent)
		if parent.status.file:
			with open(parent.status.file) as f:
				while line := f.readline():
					parent.gcode_pte.appendPlainText(line.strip())
			cursor = parent.gcode_pte.textCursor()
			cursor.movePosition(QTextCursor.MoveOperation.Start)
			parent.gcode_pte.setTextCursor(cursor)
	else:
		parent.gcode_pte_exists = False

def print_constants(parent):
	print(f'MODE_MANUAL = {parent.emc.MODE_MANUAL}')
	print(f'TRAJ_MODE_COORD = {parent.emc.TRAJ_MODE_COORD}')
	print(f'TRAJ_MODE_FREE = {parent.emc.TRAJ_MODE_FREE}')
	print(f'TRAJ_MODE_TELEOP = {parent.emc.TRAJ_MODE_TELEOP}')
	print(f'MODE_MDI = {parent.emc.MODE_MDI}')
	print(f'MODE_AUTO = {parent.emc.MODE_AUTO}')
	print(f'MODE_MANUAL = {parent.emc.MODE_MANUAL}')
	print(f'JOG_STOP = {parent.emc.JOG_STOP}')
	print(f'JOG_CONTINUOUS = {parent.emc.JOG_CONTINUOUS}')
	print(f'JOG_INCREMENT = {parent.emc.JOG_INCREMENT}')

