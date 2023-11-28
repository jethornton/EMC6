
import linuxcnc
command = linuxcnc.command()

TRAJ_MODE_COORD = 2
TRAJ_MODE_FREE = 1
TRAJ_MODE_TELEOP = 3
MODE_MDI = 3
MODE_AUTO = 2
MODE_MANUAL = 1
TELEOP_DISABLE = 0
TELEOP_ENABLE = 1

def set_mode(parent, mode):
	if parent.status.task_mode != mode:
		parent.command.mode(mode)
		parent.command.wait_complete()

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
		if parent.status.task_mode != linuxcnc.MODE_MANUAL:
			parent.command.mode(MODE_MANUAL)
		#if parent.status.motion_mode != linuxcnc.TRAJ_MODE_FREE:
		#	parent.command.traj_mode(linuxcnc.TRAJ_MODE_FREE)
		parent.command.home(joint)
		parent.sender().setStyleSheet('background-color: rgba(0, 255, 0, 25%);')
		getattr(parent, f'unhome_pb_{joint}').setEnabled(True)

	# homed (returns tuple of integers) - currently homed joints, 0 = not homed, 1 = homed.
	# home(int) home a given joint.

def unhome(parent):
	joint = int(parent.sender().objectName()[-1])
	if parent.status.homed[joint] == 1:
		set_mode(parent, MODE_MANUAL)
		parent.command.teleop_enable(TELEOP_DISABLE)
		parent.command.wait_complete()
		parent.command.unhome(joint)
		getattr(parent, f'home_pb_{joint}').setStyleSheet('background-color: ;')
		getattr(parent, f'unhome_pb_{joint}').setEnabled(False)





