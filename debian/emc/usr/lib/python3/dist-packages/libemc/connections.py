from functools import partial

from libemc import commands

def connect(parent):
	parent.estop_pb.clicked.connect(partial(commands.emc_control.estop_toggle, parent))

