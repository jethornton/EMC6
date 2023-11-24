from functools import partial

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QAction

from libemc import commands

def connect(parent):
	controls = {'estop_pb': 'estop_toggle',
	'power_pb': 'power_toggle'}
	pushbuttons = []
	children = parent.findChildren(QPushButton)
	for child in children:
		pushbuttons.append(child.objectName())

	for pb in pushbuttons:
		if pb in controls:
			getattr(parent, pb).clicked.connect(partial(getattr(commands, controls[pb]), parent))

	# Menu Items
	actions = []
	for action in parent.findChildren(QAction):
		if action.objectName():
			actions.append(action.objectName())
	#print(actions)

