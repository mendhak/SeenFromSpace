import datetime
import os
import random
import urllib, urllib.request
import sys
import time
from xml.etree.ElementTree import ElementTree
import re
from dateutil import parser  #pip install 'python-dateutil < 2.0'
from . NightImageType import NightImageType
from . NasaImageType import NasaImageType
from . CenterAreaType import CenterAreaType
from . ProjectionType import ProjectionType
from . ProjectionInfo import ProjectionInfo
from . EarthquakeInfo import EarthquakeInfo
from . SatelliteInfo import SatelliteInfo
from . CenterAreaInfo import CenterAreaInfo

#TODO: Storm could be better sourced, probably from NOAA or Wunderground
#TODO: Preconfigured satellites
#TODO: Generated date time
#TODO: Save generated images in archive folder
#TODO: Generate cloud yourself? http://www.sat.dundee.ac.uk/geobrowse/geobrowse.php

class generator:

	def __init__(self, workingDirectory):

		self.workingDirectory = workingDirectory

		#Read from earth configuration
		self.nasaImageType = NasaImageType.TOPOBATHY
		self.nightImageType = NightImageType.INTENSE

		self.dimensions = "2400x1200" #"1440x900"

		self.projection = ProjectionInfo()
		self.projection.Projection = ProjectionType.MERCATOR

		self.center = CenterAreaInfo()
		self.center.areaType = CenterAreaType.Default
		self.center.Latitude = None #-10
		self.center.Longitude = None #-30

		self.quake = EarthquakeInfo()
		self.quake.DaysAgo = 1
		self.quake.MinimumMagnitude = 6
		self.quake.ShowLocation = True

		self.satellites = []

		issSatellite = SatelliteInfo()
		issSatellite.Designation = "25544"
		issSatellite.Name = "ISS!"
		issSatellite.ShowVisibilityCircle = True
		issSatellite.TrailMinutes = 51
		issSatellite.Image = "/home/mendhak/Code/SeenFromSpace/static/iss.png"
		self.satellites.append(issSatellite)

		self.satellites.append(SatelliteInfo())
		self.satellites[1].Designation = "20580"
		self.satellites[1].Name = "HUBBLE"
		self.satellites[1].ShowVisibilityCircle = False
		self.satellites[1].TrailMinutes = 10
		self.satellites[1].TextColor  = "green"
		self.satellites[1].Image = "/home/mendhak/Code/SeenFromSpace/static/hst.png"

	def getDayMap(self):

		if self.nasaImageType == NasaImageType.PLAIN:
			subFolder = "plain"
		elif self.nasaImageType == NasaImageType.TOPO:
			subFolder = "topo"
		elif self.nasaImageType == NasaImageType.TOPOBATHY:
			subFolder = "topobathy"
		else:
			subFolder = None

		if subFolder:

			currentMonth = datetime.datetime.now().month
			currentMapDirectory = os.path.join(self.workingDirectory, "nasaimages", subFolder)
			currentMapFile = os.path.join(currentMapDirectory, str(currentMonth) + ".jpg")

			print("Checking for", currentMapFile)

			if os.path.exists(currentMapFile):
				return currentMapFile
			else:
				if not os.path.exists(currentMapDirectory):
					os.makedirs(currentMapDirectory)

				if self.nasaImageType == NasaImageType.PLAIN:
					downloadImg = self.getNasaMonthlyPlainUrl(currentMonth)
				elif self.nasaImageType == NasaImageType.TOPO:
					downloadImg = self.getNasaMonthlyTopoUrl(currentMonth)
				else:
					downloadImg = self.getNasaMonthlyTopoBathyUrl(currentMonth)

				print("Not found, downloading " + downloadImg)

				try:
					urllib.request.urlretrieve(downloadImg, currentMapFile)
				except:
					sys.stderr.write("Could not download " + downloadImg + "\n")
					currentMapFile = None

				return currentMapFile
		else:
			currentMapFile = os.path.join(self.workingDirectory ,"static", "earth-summer.jpg")
			return currentMapFile


	def getNasaMonthlyTopoUrl(self, month):
		monthlyTopoFiles = {
					1 : "http://eoimages.gsfc.nasa.gov/ve/7124/world.topo.200401.3x5400x2700.jpg",
					2 : "http://eoimages.gsfc.nasa.gov/ve/7125/world.topo.200402.3x5400x2700.jpg",
					3 : "http://eoimages.gsfc.nasa.gov/ve/7126/world.topo.200403.3x5400x2700.jpg",
					4 : "http://eoimages.gsfc.nasa.gov/ve/7127/world.topo.200404.3x5400x2700.jpg",
					5 : "http://eoimages.gsfc.nasa.gov/ve/7128/world.topo.200405.3x5400x2700.jpg",
					6 : "http://eoimages.gsfc.nasa.gov/ve/7129/world.topo.200406.3x5400x2700.jpg",
					7 : "http://eoimages.gsfc.nasa.gov/ve/7130/world.topo.200407.3x5400x2700.jpg",
					8 : "http://eoimages.gsfc.nasa.gov/ve/7131/world.topo.200408.3x5400x2700.jpg",
					9 : "http://eoimages.gsfc.nasa.gov/ve/7132/world.topo.200409.3x5400x2700.jpg",
					10 : "http://eoimages.gsfc.nasa.gov/ve/7133/world.topo.200410.3x5400x2700.jpg",
					11 : "http://eoimages.gsfc.nasa.gov/ve/7134/world.topo.200411.3x5400x2700.jpg",
					12 : "http://eoimages.gsfc.nasa.gov/ve/7135/world.topo.200412.3x5400x2700.jpg"
				   }
		return monthlyTopoFiles[month]


	def getNasaMonthlyTopoBathyUrl(self, month):
		return "https://neo.sci.gsfc.nasa.gov/archive/bluemarble/bmng/world_8km/world.topo.bathy.2004{}.3x5400x2700.jpg".format("%02d" % month)


	def getNasaMonthlyPlainUrl(self, month):
		monthlyPlainFiles = {
					1 : ["http://earthobservatory.nasa.gov/Features/BlueMarble/images_bmng/8km/world.200401.3x5400x2700.jpg", 
						"http://eoimages.gsfc.nasa.gov/ve/7112/world.200401.3x5400x2700.jpg"],
					2 : ["http://earthobservatory.nasa.gov/Features/BlueMarble/images_bmng/8km/world.200402.3x5400x2700.jpg",
						"http://eoimages.gsfc.nasa.gov/ve/7113/world.200402.3x5400x2700.jpg"],
					3 : ["http://earthobservatory.nasa.gov/Features/BlueMarble/images_bmng/8km/world.200403.3x5400x2700.jpg",
						"http://eoimages.gsfc.nasa.gov/ve/7114/world.200403.3x5400x2700.jpg"],
					4 : ["http://earthobservatory.nasa.gov/Features/BlueMarble/images_bmng/8km/world.200404.3x5400x2700.jpg",
						"http://eoimages.gsfc.nasa.gov/ve/7115/world.200404.3x5400x2700.jpg"],
					5 : ["http://earthobservatory.nasa.gov/Features/BlueMarble/images_bmng/8km/world.200405.3x5400x2700.jpg",
						"http://eoimages.gsfc.nasa.gov/ve/7116/world.200405.3x5400x2700.jpg"],
					6 : ["http://earthobservatory.nasa.gov/Features/BlueMarble/images_bmng/8km/world.200406.3x5400x2700.jpg", 
						"http://eoimages.gsfc.nasa.gov/ve/7117/world.200406.3x5400x2700.jpg"],
					7 : ["http://earthobservatory.nasa.gov/Features/BlueMarble/images_bmng/8km/world.200407.3x5400x2700.jpg", 
						"http://eoimages.gsfc.nasa.gov/ve/7118/world.200407.3x5400x2700.jpg"],
					8 : ["http://earthobservatory.nasa.gov/Features/BlueMarble/images_bmng/8km/world.200408.3x5400x2700.jpg",
						"http://eoimages.gsfc.nasa.gov/ve/7119/world.200408.3x5400x2700.jpg"],
					9 : ["http://earthobservatory.nasa.gov/Features/BlueMarble/images_bmng/8km/world.200409.3x5400x2700.jpg",
						"http://eoimages.gsfc.nasa.gov/ve/7120/world.200409.3x5400x2700.jpg"],
					10 : ["http://earthobservatory.nasa.gov/Features/BlueMarble/images_bmng/8km/world.200410.3x5400x2700.jpg",
						"http://eoimages.gsfc.nasa.gov/ve/7121/world.200410.3x5400x2700.jpg"],
					11 : ["http://earthobservatory.nasa.gov/Features/BlueMarble/images_bmng/8km/world.200411.3x5400x2700.jpg", 
						"http://eoimages.gsfc.nasa.gov/ve/7122/world.200411.3x5400x2700.jpg"],
					12 : ["http://earthobservatory.nasa.gov/Features/BlueMarble/images_bmng/8km/world.200412.3x5400x2700.jpg",
						"http://eoimages.gsfc.nasa.gov/ve/7123/world.200412.3x5400x2700.jpg"]

					}
		return monthlyPlainFiles[month][random.randint(0, 1)]




	def getBumpMap(self):
		currentTopoDirectory = os.path.join(self.workingDirectory, "nasaimages")
		currentTopoFile = os.path.join(currentTopoDirectory, "topo.png")

		print("Checking for",  currentTopoFile)

		if os.path.exists(currentTopoFile):
			return currentTopoFile
		else:
			if not os.path.exists(currentTopoDirectory):
				os.makedirs(currentTopoDirectory)
			topoMapUrl = "https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73751/world.topo.bathy.200407.3x5400x2700.png"
			print("Not found, downloading " + topoMapUrl)
			urllib.request.urlretrieve(topoMapUrl, currentTopoFile)
			return currentTopoFile


	def getNightMap(self):
		if self.nightImageType == NightImageType.DIM:
			suffix = "dim"
		else:
			suffix = "intense"

		nightMapFile = os.path.join(self.workingDirectory, "static", "night_" + suffix + ".jpg")
		print("Checking for",  nightMapFile)
		if os.path.exists(nightMapFile):
			return nightMapFile


	def getCloudMap(self):
		maxRetries = 3
		currentCloudDirectory = os.path.join(self.workingDirectory, "clouds")
		cloudFile = os.path.join(currentCloudDirectory, "clouds.jpg")

		self.createDirectory(currentCloudDirectory)

		if not self.isNewDownloadRequired(cloudFile, 3, 400000):

			mirrors = [
				 "http://home.megapass.co.kr/~gitto88/cloud_data/clouds_2048.jpg",
				 "http://home.megapass.co.kr/~holywatr/cloud_data/clouds_2048.jpg",
				 "ftp://ftp.iastate.edu/pub/xplanet/clouds_2048.jpg",
			     "http://xplanet.sourceforge.net/clouds/clouds_2048.jpg"
				  ]

			for a in range(maxRetries):
				try:
					url = mirrors [ random.randint(0, len(mirrors)-1) ]
					print("Downloading", url)
					urllib.request.urlretrieve(url, cloudFile)
					break
				except:
					sys.stderr.write("Could not get cloud file\n")


		return cloudFile

	def getSatellitesList(self):
		currentSatellitesDirectory = os.path.join(self.workingDirectory, "satellites")
		satelliteFile = os.path.join(currentSatellitesDirectory, "satellites.txt")
		satelliteTLE = os.path.join(currentSatellitesDirectory, satelliteFile + ".tle")
		satelliteImage = os.path.join(self.workingDirectory, "static/sat.png")

		self.createDirectory(currentSatellitesDirectory)

		if not self.isNewDownloadRequired(satelliteTLE, 6, None):
			try:
				print("Downloading satellite TLE file from http://celestrak.com/NORAD/elements/visual.txt")
				urllib.request.urlretrieve("http://celestrak.com/NORAD/elements/visual.txt", satelliteTLE)
			except:
				print("Could not download satellite TLE file")

		satelliteFileContents = ""
		if os.path.exists(satelliteTLE):

			for s in self.satellites:
				visibilityParameter = ""
				if s.ShowVisibilityCircle:
					visibilityParameter = "altcirc=0"
				if s.Image:
					satelliteImage = s.Image
				satelliteFileContents += "{0} \"{1}\" image={2} transparent={{0,0,0}} trail={{orbit,-{3},0,{3}}} color={4} {5}\n".format(s.Designation, s.Name, satelliteImage, s.TrailMinutes, s.TextColor, visibilityParameter)

		print("Writing", satelliteFile)
		with open(satelliteFile, 'w') as tempSat:
			tempSat.write(satelliteFileContents)

		return satelliteFile


	def getArcs(self):
		self.arcs = []
		self.arcs.append(self.getStormArcs())
		return self.arcs

	def getStormArcs(self):
		currentStormDirectory = os.path.join(self.workingDirectory, "storms")
		stormArcFile = os.path.join(currentStormDirectory, "stormarcs.txt")

		self.createDirectory(currentStormDirectory)

		if not self.isNewDownloadRequired(stormArcFile, 1, None):
			try:
				print("Downloading storm arc file from http://www.wizabit.eclipse.co.uk/xplanet/files/local/arcs/storm")
				urllib.request.urlretrieve("http://www.wizabit.eclipse.co.uk/xplanet/files/local/arcs/storm", stormArcFile)
			except:
				print("Could not download storm arc file")

		return stormArcFile


		



	def getMarkers(self):
		self.markers = []
		self.markers.append(self.getEarthquakeList())
		self.markers.append(self.getStormList())
		return self.markers

	def getStormList(self):
		currentStormDirectory = os.path.join(self.workingDirectory, "storms")
		stormFile = os.path.join(currentStormDirectory, "storms.txt")

		self.createDirectory(currentStormDirectory)

		if not self.isNewDownloadRequired(stormFile, 3, None):
			try:
				print("Downloading storm file from http://www.wizabit.eclipse.co.uk/xplanet/files/local/storm")
				urllib.request.urlretrieve("http://www.wizabit.eclipse.co.uk/xplanet/files/local/storm", stormFile)
			except:
				print("Could not download storm file")

		return stormFile


	def getEarthquakeList(self):
		currentQuakeDirectory = os.path.join(self.workingDirectory, "quakes")
		quakeFile = os.path.join(currentQuakeDirectory, "quakes.txt")
		quakeXml = os.path.join(currentQuakeDirectory, "quakes.xml")

		self.createDirectory(currentQuakeDirectory)

		if not self.isNewDownloadRequired(quakeXml, 1, None):
			try:
				print("Downloading quake file from https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.xml")
				urllib.request.urlretrieve("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.xml", quakeXml)
			except:
				print("Could not download quake file")

		quakeFileContents = ""
		tree = ElementTree()

		try:
			tree.parse(quakeXml)
		except:
			print("Could not parse the quake XML file")
			tree = None

		if tree:

			items = tree.findall("{http://www.w3.org/2005/Atom}entry")

			for i in items:
				subject = i.find("{http://www.w3.org/2005/Atom}title")
				r = re.match("M ([0-9\.]+), (.+)", subject.text)
				magnitude = float(r.group(1))
				if magnitude >= self.quake.MinimumMagnitude:
					locationDesc = r.group(2)
					point = i.find("{http://www.georss.org/georss}point")
					pubDateNode = i.find("{http://www.w3.org/2005/Atom}updated")
					pubDate = parser.parse(pubDateNode.text)
					minDate = datetime.datetime.utcnow()-datetime.timedelta(days=self.quake.DaysAgo)
					if minDate.replace(tzinfo=None) < pubDate.replace(tzinfo=None):
						quakeFileContents += "{0} \"{1}\" color=0xFF3333 align=Above symbolsize=3\n".format(point.text, str(magnitude))
						if self.quake.ShowLocation:
							quakeFileContents += "{0} \"{1}\" color=0xFF3333 align=Below\n".format(point.text, locationDesc)


			print("Writing", quakeFile)
			with open(quakeFile, 'w') as tempQuake:
				tempQuake.write(quakeFileContents)

		return quakeFile


	def getProjection(self):
		return self.projection.Projection

	def getDimensions(self):
		return self.dimensions

	def getOrigin(self):
		if self.center.AreaType == CenterAreaType.Default:
			return None
		if self.center.AreaType == CenterAreaType.DaySide:
			return "sun"
		if self.center.AreaType == CenterAreaType.NightSide:
			return "-sun"

		return None

	def getLatitude(self):
		return self.center.Latitude

	def getLongitude(self):
		return self.center.Longitude

	def getZoom(self):
		return self.projection.ZoomLevel

	def getCropTop(self):
		return self.projection.CropTop

	def getCropBottom(self):
		return self.projection.CropBottom

	def createDirectory(self, directory):
		if not os.path.exists(directory):
			os.makedirs(directory)

	def isNewDownloadRequired(self, fileToCheck, maxAgeInHours, minFileSize):

		if minFileSize is None:
			minFileSize = 0

		try:
			print("Checking timestamps on", fileToCheck)
			lastModified = os.path.getmtime(fileToCheck)
			fileSize = os.path.getsize(fileToCheck)
		except:
			print('Error while reading timestamps')
			print("Unexpected error:", sys.exc_info()[0])
			lastModified = 0
			fileSize = 0

		if time.time() - lastModified < maxAgeInHours * 3600 and fileSize > minFileSize:
			print(fileToCheck, "is up to date")
			return True
		else:
			return False

