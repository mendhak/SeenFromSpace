

class SatelliteInfo(object):

	def __init__(self):
		self.designation = None
		self.name = None
		self.textColor = "yellow"
		self.showVisibilityCircle = False
		self.trailMinutes = 0
		self.image = None

	@property
	def Designation(self):
		return self.designation

	@Designation.setter
	def Designation(self,value):
		self.designation = value

	@property
	def Name(self):
		return self.name

	@Name.setter
	def Name(self, value):
		self.name = value

	@property
	def TextColor(self):
		return self.textColor

	@TextColor.setter
	def TextColor(self, value):
		self.textColor = value

	@property
	def ShowVisibilityCircle(self):
		return self.showVisibilityCircle

	@ShowVisibilityCircle.setter
	def ShowVisibilityCircle(self, value):
		self.showVisibilityCircle = value

	@property
	def TrailMinutes(self):
		return self.trailMinutes

	@TrailMinutes.setter
	def TrailMinutes(self, value):
		if value % 5:
			modVal = value % 5
			value = value + (5 - modVal)

		if value >= 45:
			value = 45

		self.trailMinutes = value

	@property
	def Image(self):
		return self.image

	@Image.setter
	def Image(self, value):
		self.image = value
