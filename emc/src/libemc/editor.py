from PyQt6.QtGui import QTextCursor, QTextBlockFormat, QColor

def highlight_line(parent):
	""" Sets the highlighting of a given line number in the QTextEdit"""
	format_normal = QTextBlockFormat()
	format_normal.setBackground(QColor('white'))
	highlight_format = QTextBlockFormat()
	highlight_format.setBackground(QColor('yellow'))
	motion_line = parent.status.motion_line

	cursor = parent.gcode_pte.textCursor()
	cursor.select(QTextCursor.SelectionType.Document)
	cursor.setBlockFormat(format_normal)

	cursor = QTextCursor(parent.gcode_pte.document().findBlockByNumber(motion_line))
	cursor.setBlockFormat(highlight_format)
	parent.gcode_pte.setTextCursor(cursor)

def move_cursor(parent):
	format_normal = QTextBlockFormat()
	format_normal.setBackground(QColor('white'))
	highlight_format = QTextBlockFormat()
	highlight_format.setBackground(QColor('yellow'))
	motion_line = parent.status.motion_line

	cursor = parent.gcode_pte.textCursor()
	cursor.select(QTextCursor.SelectionType.Document)
	cursor.setBlockFormat(format_normal)
	cursor = parent.gcode_pte.textCursor()
	next_block = cursor.blockNumber()
	cursor = QTextCursor(parent.gcode_pte.document().findBlockByNumber(next_block))
	cursor.setBlockFormat(highlight_format)
	print(next_block)
	#cursor.setPosition(5, QTextCursor.MoveMode.MoveAnchor)
	#cursor.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor)

def clear_highlight(parent):
	format_normal = QTextBlockFormat()
	format_normal.setBackground(QColor('white'))
	cursor = parent.gcode_pte.textCursor()
	cursor.select(QTextCursor.SelectionType.Document)
	cursor.setBlockFormat(format_normal)

