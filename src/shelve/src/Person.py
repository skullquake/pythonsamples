class Person:
	"""
	Person class
	"""
	def __init__(self,name="<unknown>"):
		self.name=name
	def __str__(self):
		return self.name
	def __repr__(self):
		return self.__str__()
	def setName(self,name):
		self.name=name
	def getName(self):
		return self.name
