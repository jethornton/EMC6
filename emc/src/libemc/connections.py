from functools import partial

from PyQt6.QtWidgets import QPushButton

from libemc import commands

def connect(parent):

	connections = {'estop_pb': 'estop_toggle',
	'energise_pb': 'power_toggle'}
	pushbuttons = []
	children = parent.findChildren(QPushButton)
	for child in children:
		pushbuttons.append(child.objectName())

	for pb in pushbuttons:
		if pb in connections:
			#print(pb)
			#print(connections[pb])
			getattr(parent, pb).clicked.connect(partial(getattr(commands, connections[pb]), parent))
	#parent.estop_pb.clicked.connect(partial(commands.estop_toggle, parent))

