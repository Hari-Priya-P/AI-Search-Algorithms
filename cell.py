class Cell:

	def __init__(cell, value):
		"""
		value = 0 => empty cell
		value = 1 => occupied cell
		value = 2 => burning cell
		"""
		cell.value = value
		cell.parent = None
		cell.visited = False