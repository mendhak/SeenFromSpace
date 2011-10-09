class ProjectionType:
	"""ancient, azimuthal, bonne,
equal_area, gnomonic, hemisphere, icosagnomonic, lambert, mercator,
mollweide, orthographic, peters, polyconic, rectangular, or tsc"""
	ANCIENT="ancient"               #hemispheres
	HEMISPHERE="hemisphere"         #hemispheres
	ORTHOGRAPHIC="orthographic"     #one hemisphere
	"""Shows one side of the globe, you can use MiddleArea.Default or set a latitude-longitude to determine what's in focus"""

	EQUALAREA="equal_area"          #squished hemisphere
	MOLLWEIDE="mollweide"           #ellipse
	LAMBERT="lambert"               #rect

	MERCATOR="mercator"             #rect
	"""The most common rectangular representation"""

	
	PETERS="peters"                 #rect
	RECTANGULAR="rectangular"       #rect