from PyQt6.QtWidgets import QLabel

import linuxcnc

from libemc import commands

def set_labels(parent):
	label_list = ['status_lb', 'file_lb',]
	children = parent.findChildren(QLabel)
	found_label_list = []
	for child in children:
		found_label_list.append(child.objectName())

	for label in label_list:
		if label in found_label_list:
			setattr(parent, f'{label}_exists', True)
		else:
			setattr(parent, f'{label}_exists', False)

	#print(parent.status_lb_exists)
	#print(parent.status_lb.text())
	#print(linuxcnc.MODE_MDI)
	#print(linuxcnc.MODE_AUTO)
	#print(linuxcnc.MODE_MANUAL)


def set_buttons(parent):
	if parent.status.task_state == linuxcnc.STATE_ESTOP_RESET:
		commands.estop_toggle(parent)


def print_constants(parent):
	print(f'MODE_MANUAL = {parent.emc.MODE_MANUAL}')
	print(f'TRAJ_MODE_COORD = {parent.emc.TRAJ_MODE_COORD}')
	print(f'TRAJ_MODE_FREE = {parent.emc.TRAJ_MODE_FREE}')
	print(f'TRAJ_MODE_TELEOP = {parent.emc.TRAJ_MODE_TELEOP}')
	print(f'MODE_MDI = {parent.emc.MODE_MDI}')
	print(f'MODE_AUTO = {parent.emc.MODE_AUTO}')
	print(f'MODE_MANUAL = {parent.emc.MODE_MANUAL}')

