
class emc_control:
	def __init__(self, parent, emc):
		self.emc = emc
		self.command = emc.command()
		self.status = emc.stat()
		self.error = emc.error_channel()

	def estop_toggle(self):
		#state(int)
		#Set the machine state. Machine state should be STATE_ESTOP, STATE_ESTOP_RESET, STATE_ON, or STATE_OFF.
		self.command.state(self.emc.STATE_ESTOP_RESET)

