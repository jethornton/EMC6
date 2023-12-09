from functools import partial

from PyQt6.QtWidgets import QPushButton, QPlainTextEdit, QListWidget
from PyQt6.QtGui import QAction

from libemc import commands
from libemc import menus
from libemc import editor
from libemc import utilities

def connect(parent):

	controls = {'estop_pb': 'estop_toggle',
	'power_pb': 'power_toggle',
	'run_pb': 'run',
	'step_pb': 'step',
	'pause_pb': 'pause',
	'resume_pb': 'resume',
	'stop_pb': 'stop',
	'home_pb_0': 'home',
	'home_pb_1': 'home',
	'home_pb_2': 'home',
	'unhome_all_pb': 'unhome_all',
	'unhome_pb_0': 'unhome',
	'unhome_pb_1': 'unhome',
	'unhome_pb_2': 'unhome',
	'run_mdi_pb': 'run_mdi',
	}
	pushbuttons = []
	children = parent.findChildren(QPushButton)
	for child in children:
		pushbuttons.append(child.objectName())

	for pb in pushbuttons:
		if pb in controls:
			getattr(parent, pb).clicked.connect(partial(getattr(commands, controls[pb]), parent))

	jog_buttons = {
	'jog_plus_pb_0': 'jog',
	'jog_minus_pb_0': 'jog',
	'jog_plus_pb_1': 'jog',
	'jog_minus_pb_1': 'jog',
	'jog_plus_pb_2': 'jog',
	'jog_minus_pb_2': 'jog',
	}

	for pb in pushbuttons:
		if pb in jog_buttons:
			getattr(parent, pb).pressed.connect(partial(getattr(commands, jog_buttons[pb]), parent))
			getattr(parent, pb).released.connect(partial(getattr(commands, jog_buttons[pb]), parent))

	# Menu Items
	menu_actions = {'actionOpen': 'file_open', 'actionReload': 'file_reload'}
	action_list = []
	for action in parent.findChildren(QAction):
		if action.objectName():
			action_list.append(action.objectName())

	for action in action_list:
		if action in menu_actions:
			getattr(parent, action).triggered.connect(partial(getattr(menus, menu_actions[action]), parent))

	list_widgets = {'mdi_history_lw': 'add_mdi'}
	list_widgets_list = []
	for list_widget in parent.findChildren(QListWidget):
		if list_widget.objectName():
			list_widgets_list.append(list_widget.objectName())

	for item in list_widgets_list:
		if item in list_widgets:
			getattr(parent, item).itemSelectionChanged.connect(partial(getattr(utilities, list_widgets[item]), parent))


	# combo boxes
	combo_dict = {'jog_mode_cb': 'load_jog_modes'}


	# plain text edits
	# ptes = {'gcode_pte': 'gcode_viewer'}
	#if parent.findChild(QPlainTextEdit, 'gcode_pte'):
	#./	parent.gcode_pte.cursorPositionChanged.connect(partial(editor.highlight_line, parent))


