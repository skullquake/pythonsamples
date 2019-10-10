import math 
class Circle():
	def __init__(self,r=0):
		"""
		ctor
		"""
		self.r=r


	def set_r(self,r=0):
		"""
		set r
		"""
		self.r=r
		return

	def get_r(self):
		"""
		get r
		"""
		return self.r


	def get_area(self):
		"""
		computes area
		"""
		if isinstance(self.r, int) or isinstance(self.r, float):
			#todo assert radius >= 0
			return self.r*math.pow(math.pi, 2)
		else:
			raise AssertionError("Invalid radius")
		return

	def get_circ(self):
		"""
		computes circumference
		"""
		if isinstance(self.r, int) or isinstance(self.r, float):
			#todo assert radius >= 0
 			return 2*math.pi*self.r
		raise AssertionError("Invalid radius")
  
	def __str__(self):
		"""
		ascii art
		"""
		ret=""
		for i in range((2 * self.r)+1): 
			for j in range((2 * self.r)+1): 
				dist = math.sqrt((i - self.r) * (i - self.r) + (j - self.r) * (j - self.r)) 
				if (dist > self.r - 0.5 and dist < self.r + 0.5):  
					ret+="██"
				else: 
					ret+="▒▒"
			ret+="\n"
		ret="\u001b[31m"+ret+"\u001b[0m"
		return ret
