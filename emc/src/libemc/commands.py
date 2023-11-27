
import linuxcnc
command = linuxcnc.command()

def estop_toggle(parent):
	if parent.status.task_state == linuxcnc.STATE_ESTOP:
		command.state(linuxcnc.STATE_ESTOP_RESET)
		parent.estop_pb.setStyleSheet('background-color: rgba(0, 255, 0, 25%);')
		parent.power_pb.setEnabled(True)
	else:
		command.state(linuxcnc.STATE_ESTOP)
		parent.estop_pb.setStyleSheet('background-color: rgba(255, 0, 0, 25%);')
		parent.power_pb.setEnabled(False)
		parent.power_pb.setStyleSheet('background-color: ;')
		parent.power_pb.setText('Power Off')

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
	}

def power_toggle(parent):
	if parent.status.task_state == linuxcnc.STATE_ESTOP_RESET:
		command.state(linuxcnc.STATE_ON)
		parent.power_pb.setStyleSheet('background-color: rgba(0, 255, 0, 25%);')
		parent.power_pb.setText('Power On')
		if parent.status.file:
			parent.run_pb.setEnabled(True)
			parent.step_pb.setEnabled(True)
		parent.home_pb_0.setEnabled(True)
		parent.home_pb_1.setEnabled(True)
		parent.home_pb_2.setEnabled(True)
	else:
		command.state(linuxcnc.STATE_OFF)
		parent.power_pb.setStyleSheet('background-color: ;')
		parent.power_pb.setText('Power Off')

def run(parent):
	if parent.status.task_state == linuxcnc.STATE_ON:
		if parent.status.task_mode != linuxcnc.MODE_AUTO:
			parent.command.mode(linuxcnc.MODE_AUTO)
		parent.command.auto(linuxcnc.AUTO_RUN, 0)

def step(parent):
	if parent.status.task_state == linuxcnc.STATE_ON:
		if parent.status.task_mode != linuxcnc.MODE_AUTO:
			parent.command.mode(linuxcnc.MODE_AUTO)
		parent.command.auto(linuxcnc.AUTO_STEP)

def pause(parent):
	if parent.status.state == linuxcnc.RCS_EXEC: # program is running
		parent.command.auto(linuxcnc.AUTO_PAUSE)

def resume(parent):
	if parent.status.paused:
		parent.command.auto(linuxcnc.AUTO_RESUME)

def stop(parent):
	parent.command.abort()

def home(parent):
	joint = int(parent.sender().objectName()[-1])
	if parent.status.homed[joint] == 0:
		parent.command.home(joint)
		parent.sender().setStyleSheet('background-color: rgba(0, 255, 0, 25%);')

	# homed (returns tuple of integers) - currently homed joints, 0 = not homed, 1 = homed.
	# home(int) home a given joint.






