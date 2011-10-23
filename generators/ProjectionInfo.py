from ProjectionType import ProjectionType

class ProjectionInfo(object):
	def __init__(self):
		self.cropTop = 0
		self.cropBottom = 0

	@property
	def Projection(self):
		return self.projectionType

	@Projection.setter
	def Projection(self, value):
		self.projectionType = value
		self.zoomLevel = 45

		if self.projectionType == ProjectionType.ORTHOGRAPHIC:
			self.cropTop = 0
			self.cropBottom = 0

		if self.projectionType == ProjectionType.MERCATOR:
			self.cropTop = 150
			self.cropBottom = 200

	@property
	def CropTop(self):
		return self.cropTop

	@property
	def CropBottom(self):
		return self.cropBottom

	@property
	def ZoomLevel(self):
		return self.zoomLevel