
import linuxcnc
command = linuxcnc.command()

def estop_toggle(parent):
	if parent.status.task_state == linuxcnc.STATE_ESTOP:
		command.state(linuxcnc.STATE_ESTOP_RESET)
		parent.estop_pb.setStyleSheet('background-color: green;')
		parent.power_pb.setEnabled(True)
	else:
		command.state(linuxcnc.STATE_ESTOP)
		parent.estop_pb.setStyleSheet('background-color: red;')
		parent.power_pb.setEnabled(False)
		parent.power_pb.setStyleSheet('background-color: ;')
		parent.power_pb.setText('Power Off')

def power_toggle(parent):
	if parent.status.task_state == linuxcnc. STATE_ESTOP_RESET:
		command.state(linuxcnc.STATE_ON)
		parent.power_pb.setStyleSheet('background-color: green;')
		parent.power_pb.setText('Power On')
	else:
		command.state(linuxcnc.STATE_OFF)
		parent.power_pb.setStyleSheet('background-color: ;')
		parent.power_pb.setText('Power Off')


