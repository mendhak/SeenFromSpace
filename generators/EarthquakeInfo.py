class EarthquakeInfo(object):

	def __init__(self):
		self.showLocation = None
		self.daysAgo = None
		self.minimumMagnitude = None

	@property
	def ShowLocation(self):
		return self.showLocation

	@ShowLocation.setter
	def ShowLocation(self, value):
		self.showLocation = value

	@property
	def DaysAgo(self):
		return self.daysAgo

	@DaysAgo.setter
	def DaysAgo(self, value):
		if value >= 7:
			value = 7
		self.daysAgo = value

	@property
	def MinimumMagnitude(self):
		return self.minimumMagnitude

	@MinimumMagnitude.setter
	def MinimumMagnitude(self, value):
		if value <= 3:
			value = 3
		self.minimumMagnitude = value