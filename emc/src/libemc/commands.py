
import linuxcnc
command = linuxcnc.command()

def estop_toggle(parent):
	if parent.status.task_state == linuxcnc.STATE_ESTOP:
		command.state(linuxcnc.STATE_ESTOP_RESET)
		#estop_pb.setStyleSheet('border-style: inset;')
		parent.estop_pb.setStyleSheet('background-color: green;')
		parent.energise_pb.setEnabled(True)
		#print('red')
	else:
		command.state(linuxcnc.STATE_ESTOP)
		#self.estop_pb.setStyleSheet('border-style: outset;')
		#self.estop_pb.setStyleSheet('border: 1px inset black;')
		#self.estop_pb.setStyleSheet('background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0')
		parent.estop_pb.setStyleSheet('background-color: red;')
		parent.energise_pb.setEnabled(False)
		parent.energise_pb.setStyleSheet('background-color: ;')
		#print('green')

def power_toggle(parent):
	print(parent.status.task_state)
	#print(linuxcnc.STATE_OFF)
	#print(linuxcnc.STATE_ON)
	if parent.status.task_state == linuxcnc. STATE_ESTOP_RESET:
		command.state(linuxcnc.STATE_ON)
		parent.energise_pb.setStyleSheet('background-color: green;')
		#print('h')
	else:
		command.state(linuxcnc.STATE_OFF)
		parent.energise_pb.setStyleSheet('background-color: ;')
		#print('t')

