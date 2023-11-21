from functools import partial

from libemc import commands

def connect(parent):
	parent.estop_pb.clicked.connect(partial(commands.estop_toggle, parent))

