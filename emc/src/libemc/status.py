from PyQt6.QtGui import QTextCursor, QTextBlockFormat, QColor
from PyQt6.QtWidgets import QTextEdit

def update(parent):
	task_mode = {1: 'MANUAL', 2: 'AUTO', 3: 'MDI'}
	if parent.status_lb_exists:
		parent.status_lb.setText(task_mode[parent.status.task_mode])
	if parent.dro_lb_x_exists:
		parent.dro_lb_x.setText(f'{parent.status.position[0]:.4f}')
	if parent.dro_lb_y_exists:
		parent.dro_lb_y.setText(f'{parent.status.position[1]:.4f}')
	if parent.dro_lb_z_exists:
		parent.dro_lb_z.setText(f'{parent.status.position[2]:.4f}')

	state_mode = {1: 'DONE', 2: 'EXEC', 3: 'ERROR'}
	parent.state_lb.setText(f'{state_mode[parent.status.state]}')
	if parent.status.state == parent.emc.RCS_EXEC:
		parent.actionReload.setEnabled(False)
	else:
		parent.actionReload.setEnabled(True)

	if parent.motion_line_lb_exists:
		parent.motion_line_lb.setText(f'{parent.status.motion_line}')

	if parent.gcode_pte_exists:
		n = parent.status.motion_line
		if n != parent.last_line:
			format_normal = QTextBlockFormat()
			format_normal.setBackground(QColor('white'))
			highlight_format = QTextBlockFormat()
			highlight_format.setBackground(QColor('yellow'))
			motion_line = parent.status.motion_line

			cursor = parent.gcode_pte.textCursor()
			cursor.select(QTextCursor.SelectionType.Document)
			cursor.setBlockFormat(format_normal)
			cursor = QTextCursor(parent.gcode_pte.document().findBlockByNumber(motion_line))
			cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.MoveAnchor)
			cursor.setBlockFormat(highlight_format)
			parent.gcode_pte.setTextCursor(cursor)
			parent.last_line = n
		
		pass
		'''
		highlight_format = QTextBlockFormat()
		highlight_format.setBackground(QColor('yellow'))

		cursor = parent.gcode_pte.textCursor()
		cursor.clearSelection()

		n = parent.status.motion_line
		doc = parent.gcode_pte.document()
		#print(doc.blockCount())
		#cursor = QTextCursor(doc)
		#cursor.select(doc)
		cursor = QTextCursor(doc.findBlockByLineNumber(n - 1))
		parent.gcode_pte.setTextCursor(cursor)
		cursor.setBlockFormat(highlight_format)
		'''


		""" Sets the highlighting of a given line number in the QTextEdit"""
		#cursor = self.editor.textCursor()
		#cursor.select(QTextCursor.Document)
		#cursor.setBlockFormat(self.format_normal)

		#cursor = QTextCursor(self.editor.document().findBlockByNumber(lineNumber))

		''''
		selection = QTextEdit.ExtraSelection();
		selection.format.setBackground(colorValues['currentLineHighlight'])
		selection.format.setProperty(QTextFormat.FullWidthSelection, True)
		selection.cursor = self.textCursor()
		selection.cursor.clearSelection()
		parent.gcode_pte.setExtraSelections([selection])
		'''



