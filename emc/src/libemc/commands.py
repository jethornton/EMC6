
import linuxcnc
#command = linuxcnc.command()

TRAJ_MODE_COORD = 2
TRAJ_MODE_FREE = 1
TRAJ_MODE_TELEOP = 3
MODE_MDI = 3
MODE_AUTO = 2
MODE_MANUAL = 1
TELEOP_DISABLE = 0
TELEOP_ENABLE = 1
JOG_STOP = 0
JOG_CONTINUOUS = 1
JOG_INCREMENT = 2

def set_mode(parent, mode):
	if parent.status.task_mode != mode:
		parent.command.mode(mode)
		parent.command.wait_complete()

def set_motion_teleop(parent, value):
	# 1:teleop, 0: joint
	parent.command.teleop_enable(value)
	parent.command.wait_complete()
	parent.status.poll()

def estop_toggle(parent):
	if parent.status.task_state == linuxcnc.STATE_ESTOP:
		parent.command.state(linuxcnc.STATE_ESTOP_RESET)
		parent.estop_pb.setStyleSheet('background-color: rgba(0, 255, 0, 25%);')
		parent.power_pb.setEnabled(True)
	else:
		parent.command.state(linuxcnc.STATE_ESTOP)
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
		parent.command.state(linuxcnc.STATE_ON)
		parent.power_pb.setStyleSheet('background-color: rgba(0, 255, 0, 25%);')
		parent.power_pb.setText('Power On')
		if parent.status.file:
			parent.run_pb.setEnabled(True)
			parent.step_pb.setEnabled(True)
		for i in range(parent.joints):
			getattr(parent, f'home_pb_{i}').setEnabled(True)
	else:
		parent.command.state(linuxcnc.STATE_OFF)
		parent.power_pb.setStyleSheet('background-color: ;')
		parent.power_pb.setText('Power Off')

def run(parent):
	if parent.status.task_state == linuxcnc.STATE_ON:
		if parent.status.task_mode != linuxcnc.MODE_AUTO:
			parent.command.mode(linuxcnc.MODE_AUTO)
		parent.pause_pb.setEnabled(True)
		print('run')
		parent.command.auto(linuxcnc.AUTO_RUN, 0)

def step(parent):
	if parent.status.task_state == linuxcnc.STATE_ON:
		if parent.status.task_mode != linuxcnc.MODE_AUTO:
			parent.command.mode(linuxcnc.MODE_AUTO)
		parent.command.auto(linuxcnc.AUTO_STEP)

def pause(parent):
	if parent.status.state == linuxcnc.RCS_EXEC: # program is running
		parent.resume_pb.setEnabled(True)
		parent.pause_pb.setEnabled(False)
		parent.command.auto(linuxcnc.AUTO_PAUSE)

def resume(parent):
	if parent.status.paused:
		parent.resume_pb.setEnabled(False)
		parent.pause_pb.setEnabled(True)
		parent.command.auto(linuxcnc.AUTO_RESUME)

def stop(parent):
	parent.command.abort()

def all_homed(parent):
	isHomed=True
	num_joints = parent.status.joints
	for i,h in enumerate(parent.status.homed):
		if i >= num_joints: break
		isHomed = isHomed and h
	return isHomed

def home(parent):
	joint = int(parent.sender().objectName()[-1])
	if parent.status.homed[joint] == 0:
		if parent.status.task_mode != linuxcnc.MODE_MANUAL:
			parent.command.mode(MODE_MANUAL)
		#if parent.status.motion_mode != linuxcnc.TRAJ_MODE_FREE:
		#	parent.command.traj_mode(linuxcnc.TRAJ_MODE_FREE)
		parent.command.home(joint)
		parent.command.wait_complete()
		parent.sender().setStyleSheet('background-color: rgba(0, 255, 0, 25%);')
		getattr(parent, f'unhome_pb_{joint}').setEnabled(True)
		parent.unhome_all_pb.setEnabled(True)

	# homed (returns tuple of integers) - currently homed joints, 0 = not homed, 1 = homed.
	parent.status.poll()
	#print(f'Homed: {parent.status.homed}')
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

def unhome_all(parent):
		set_mode(parent, MODE_MANUAL)
		parent.command.teleop_enable(TELEOP_DISABLE)
		parent.command.wait_complete()
		parent.command.unhome(-1)
		for i in range(parent.joints):
			getattr(parent, f'home_pb_{i}').setStyleSheet('background-color: ;')
			getattr(parent, f'unhome_pb_{i}').setEnabled(False)
		parent.unhome_all_pb.setEnabled(False)

def get_jog_mode(parent):
	parent.status.poll()
	if parent.status.kinematics_type == linuxcnc.KINEMATICS_IDENTITY and all_homed(parent):
		  teleop_mode = 1
		  jjogmode = False
	else:
		  # check motion_mode since other guis (halui) could alter it
		  if parent.status.motion_mode == linuxcnc.TRAJ_MODE_FREE:
		      teleop_mode = 0
		      jjogmode = True
		  else:
		      teleop_mode = 1
		      jjogmode = False
	if (   (    jjogmode and parent.status.motion_mode != linuxcnc.TRAJ_MODE_FREE)
		  or (not jjogmode and parent.status.motion_mode != linuxcnc.TRAJ_MODE_TELEOP) ):
		  set_motion_teleop(parent, teleop_mode)
	return jjogmode


def jog(parent):
	jog_command = parent.sender().objectName().split('_')
	joint = int(jog_command[-1])
	jog_type = parent.jog_modes_cb.currentData()
	increment = parent.jog_increments_cb.currentData()
	if 'minus' in jog_command:
		increment = -increment
	jjogmode = get_jog_mode(parent)
	if parent.sender().isDown():
		if jog_type == 'incremental':
			parent.command.jog(JOG_INCREMENT, jjogmode, joint, 10, increment)
		elif jog_type == 'continuous':
			parent.command.jog(JOG_CONTINUOUS, jjogmode, joint, 10)

	else:
		parent.command.jog(JOG_STOP, jjogmode, joint)

'''
            jjogmode = get_jog_mode()
            for idx in cjogindices:
                 c.jog(linuxcnc.JOG_STOP, jjogmode,idx)


 jog(command-constant, bool, int[, float[, float]])

    Syntax

        jog(command, jjogmode, joint_num_or_axis_index, velocity[, distance])
        jog(linuxcnc.JOG_STOP, jjogmode, joint_num_or_axis_index)
        jog(linuxcnc.JOG_CONTINUOUS, jjogmode, joint_num_or_axis_index, velocity)
        jog(linuxcnc.JOG_INCREMENT, jjogmode, joint_num_or_axis_index, velocity, distance)
    Command Constants

        linuxcnc.JOG_STOP
        linuxcnc.JOG_CONTINUOUS
        linuxcnc.JOG_INCREMENT
    jjogmode

        True

            request individual joint jog (requires teleop_enable(0))
        False

            request axis Cartesian coordinate jog (requires teleop_enable(1))

    joint_num_or_axis_index

        For joint jog (jjogmode=1)

            joint_number
        For axis Cartesian coordinate jog (jjogmode=0)

            zero-based index of the axis coordinate with respect to the known coordinate letters XYZABCUVW (x=>0,y=>1,z=>2,a=>3,b=>4,c=>5,u=>6,v=>7,w=>8)
'''



