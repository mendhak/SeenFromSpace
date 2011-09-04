import datetime
import os
import random
import urllib
import sys
import time
from xml.etree.ElementTree import ElementTree
import re
import dateutil

class NasaImageType:
	PLAIN=1
	TOPO=2
	TOPOBATHY=3

class NightImageType:
	DIM=1
	INTENSE=2

class generator:


	def __init__(self, workingDirectory):
		self.workingDirectory = workingDirectory
		#Read from earth configuration
		self.nasaImageType = NasaImageType.TOPOBATHY
		self.nightImageType = NightImageType.INTENSE
		self.quakeMinMagnitude = 5
		self.quakeDaysAgo = 1

	def getDayMap(self):

		subFolder = "topobathy"
	
		if self.nasaImageType == NasaImageType.PLAIN:
			subFolder = "plain"
		elif self.nasaImageType == NasaImageType.TOPO:
			subFolder = "topo"
		else:
			subFolder = "topobathy"
	
		currentMonth = datetime.datetime.now().month
		currentMapDirectory = os.path.join(self.workingDirectory, "nasaimages", subFolder)
		currentMapFile = os.path.join(currentMapDirectory, str(currentMonth) + ".jpg")

		print "Checking for", currentMapFile

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

			print "Not found, downloading " + downloadImg

			try:
				urllib.urlretrieve(downloadImg, currentMapFile)
			except:
				sys.stderr.write("Could not download " + downloadImg + "\n")
				currentMapFile = None

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
		monthlyTopoBathyFiles = {
					1 : "http://eoimages.gsfc.nasa.gov/ve/7100/world.topo.bathy.200401.3x5400x2700.jpg",
					2 : "http://eoimages.gsfc.nasa.gov/ve/7101/world.topo.bathy.200402.3x5400x2700.jpg",
					3 : "http://eoimages.gsfc.nasa.gov/ve/7102/world.topo.bathy.200403.3x5400x2700.jpg",
					4 : "http://eoimages.gsfc.nasa.gov/ve/7103/world.topo.bathy.200404.3x5400x2700.jpg",
					5 : "http://eoimages.gsfc.nasa.gov/ve/7104/world.topo.bathy.200405.3x5400x2700.jpg",
					6 : "http://eoimages.gsfc.nasa.gov/ve/7105/world.topo.bathy.200406.3x5400x2700.jpg",
					7 : "http://eoimages.gsfc.nasa.gov/ve/7106/world.topo.bathy.200407.3x5400x2700.jpg",
					8 : "http://eoimages.gsfc.nasa.gov/ve/7107/world.topo.bathy.200408.3x5400x2700.jpg",
					9 : "http://eoimages.gsfc.nasa.gov/ve/7108/world.topo.bathy.200409.3x5400x2700.jpg",
					10 : "http://eoimages.gsfc.nasa.gov/ve/7109/world.topo.bathy.200410.3x5400x2700.jpg",
					11 : "http://eoimages.gsfc.nasa.gov/ve/7110/world.topo.bathy.200411.3x5400x2700.jpg",
					12 : "http://eoimages.gsfc.nasa.gov/ve/7111/world.topo.bathy.200412.3x5400x2700.jpg"
					}
		return monthlyTopoBathyFiles[month]


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
		currentTopoFile = os.path.join(currentTopoDirectory, "topo.jpg")

		print "Checking for",  currentTopoFile

		if os.path.exists(currentTopoFile):
			return currentTopoFile
		else:
			if not os.path.exists(currentTopoDirectory):
				os.makedirs(currentTopoDirectory)
			topoMapUrl = "http://earthobservatory.nasa.gov/Features/BlueMarble/images_bmng/8km/world.topo.200407.3x5400x2700.jpg"
			print "Not found, downloading " + topoMapUrl
			urllib.urlretrieve(topoMapUrl, currentTopoFile)
			return currentTopoFile


	def getNightMap(self):
		suffix = "intense"
		if self.nightImageType == NightImageType.DIM:
			suffix = "dim"
		else:
			suffix = "intense"
				
		nightMapFile = os.path.join(self.workingDirectory, "static", "night_" + suffix + ".jpg")
		print "Checking for",  nightMapFile
		if os.path.exists(nightMapFile):
			return nightMapFile


	def getCloudMap(self):
		maxRetries = 3
		currentCloudDirectory = os.path.join(self.workingDirectory, "clouds")
		cloudFile = os.path.join(currentCloudDirectory, "clouds.jpg")

		self.createDirectory(currentCloudDirectory)

		if not self.isNewDownloadRequired(cloudFile, 3, 400000):

			mirrors = [  "http://xplanet-sydney.inside.net/clouds_2048.jpg",
			     "http://xplanet-lasvegas.inside.net/clouds_2048.jpg",
			     "http://home.megapass.co.kr/~gitto88/cloud_data/clouds_2048.jpg",
			     "http://home.megapass.co.kr/~holywatr/cloud_data/clouds_2048.jpg",
			     "http://www.wizabit.eclipse.co.uk/xplanet/files/mirror/clouds_2048.jpg",
			     "ftp://ftp.iastate.edu/pub/xplanet/clouds_2048.jpg",
			     "http://xplanet.explore-the-world.net/clouds_2048.jpg" ]

			for a in range(maxRetries):
				try:
					url = mirrors [ random.randint(0, len(mirrors)-1) ]
					print "Downloading", url
					urllib.urlretrieve(url, cloudFile)
					break
				except:
					sys.stderr.write("Could not get cloud file\n")


		return cloudFile




	def getEarthquakeList(self):
		hoursInterval = 1
		maxRetries = 2
		currentQuakeDirectory = os.path.join(self.workingDirectory, "quakes")
		quakeFile = os.path.join(currentQuakeDirectory, "quakes.txt")
		quakeXml = os.path.join(currentQuakeDirectory, "quakes.xml")
	
		self.createDirectory(currentQuakeDirectory)

		if not self.isNewDownloadRequired(quakeFile, 1, None):
			try:
				print "Downloading quake file from http://earthquake.usgs.gov/earthquakes/catalogs/7day-M2.5.xml"
				urllib.urlretrieve("http://earthquake.usgs.gov/earthquakes/catalogs/7day-M2.5.xml", quakeXml)
			except:
				print "Could not download quake file"

		quakeFileContents = ""
		tree = ElementTree()

		try:
			tree.parse(quakeXml)
		except:
			print "Could not parse the quake XML file"
			tree = None

		if tree:
	
			items = tree.findall("{http://www.w3.org/2005/Atom}entry")

			for i in items:
				subject = i.find("{http://www.w3.org/2005/Atom}title")
				r = re.match("M ([0-9\.]+), (.+)", subject.text)
				magnitude = float(r.group(1))
				if magnitude >= self.quakeMinMagnitude:
					locationDesc = r.group(2)
					point = i.find("{http://www.georss.org/georss}point")
					pubDateNode = i.find("{http://www.w3.org/2005/Atom}updated")
					pubDate = dateutil.parser.parse(pubDateNode.text)
					minDate = datetime.datetime.utcnow()-datetime.timedelta(days=self.quakeDaysAgo)
					if minDate.replace(tzinfo=None) < pubDate.replace(tzinfo=None):
						quakeFileContents += "{0} \"{1}\" color=Red align=Above\n".format(point.text, str(magnitude))

	
			print "Writing", quakeFile
			with open(quakeFile, 'w') as tempQuake:
				tempQuake.write(quakeFileContents)

		return quakeFile



	def createDirectory(self, directory):
		if not os.path.exists(directory):
			os.makedirs(directory)

	def isNewDownloadRequired(self, fileToCheck, maxAgeInHours, minFileSize):

		if minFileSize == None:
			minFileSize = 0
	
		try:
			print "Checking timestamps on", fileToCheck
			fileStats = os.stat(fileToCheck)
			lastModified = fileStats[stat.ST_MTIME]
			fileSize = fileStats[stat.ST_SIZE]
		
		except:
			lastModified = 0
			fileSize = 0

		if time.time() - lastModified < maxAgeInHours * 3600 and fileSize > minFileSize:
			print fileToCheck, "is up to date"
			return True
		else:
			return False
	

