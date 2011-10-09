from CenterAreaType import CenterAreaType

class CenterAreaInfo(object):

	def __init__(self):
		self.latitude = 0
		self.longitude = 0

	@property
	def AreaType(self):
		return self.areaType

	@AreaType.setter
	def AreaType(self, value):
		self.areaType = value

	@property
	def Latitude(self):
		if self.latitude is None:
			self.latitude = 0
		return self.latitude

	@Latitude.setter
	def Latitude(self, value):
		if value is None:
			value = 0
		if value >= 90:
			value = 90
		if value <= -90:
			value = -90

		self.latitude = value

	@property
	def Longitude(self):
		if self.longitude is None:
			self.longitude = 0
		return self.longitude

	@Longitude.setter
	def Longitude(self, value):
		if value is None:
			value = 0
		if value >= 180:
			value = 180
		if value <= -180:
			value = -180
			
		self.longitude = value

		
