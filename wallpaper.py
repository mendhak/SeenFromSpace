#!/usr/bin/python

import random, urllib, sys, stat, time, os, datetime

class NasaImageType:
	PLAIN=1
	TOPO=2
	TOPOBATHY=3


def generateWallpaper():
	pathname = os.path.dirname(sys.argv[0])        
	scriptDirectory = os.path.abspath(pathname)
	#download cloud
	#download nasa image for this month
	#download nasa topo
	#downloadClouds("clouds/clouds.jpg")

	dayMap = getNasaDayMap(scriptDirectory, "nasaimages", NasaImageType.PLAIN)
	topoMap = getNasaBumpMap(scriptDirectory, "nasaimages")
	nightMap = getStaticNightMap(scriptDirectory, "static", True)
	cloudMap = getCloudMap(scriptDirectory, "clouds")
	print cloudMap


def getCloudMap(scriptDirectory, cloudDirectory):

	hoursInterval = 3
	maxRetries = 3
	currentCloudDirectory = os.path.join(scriptDirectory, cloudDirectory)
	cloudFile = os.path.join(currentCloudDirectory, "clouds.jpg")

	if not os.path.exists(currentCloudDirectory):
		os.makedirs(currentCloudDirectory)


	mirrors = [  "http://xplanet-sydney.inside.net/clouds_2048.jpg",
		     "http://xplanet-lasvegas.inside.net/clouds_2048.jpg",
		     "http://home.megapass.co.kr/~gitto88/cloud_data/clouds_2048.jpg",
		     "http://home.megapass.co.kr/~holywatr/cloud_data/clouds_2048.jpg",
		     "http://www.wizabit.eclipse.co.uk/xplanet/files/mirror/clouds_2048.jpg",
		     "ftp://ftp.iastate.edu/pub/xplanet/clouds_2048.jpg",
		     "http://xplanet.explore-the-world.net/clouds_2048.jpg" ]


	

	try:
		print "Checking timestamp on", cloudFile
		fileStats = os.stat(cloudFile)
		lastModified = fileStats[stat.ST_MTIME]
		fileSize = fileStats[stat.ST_SIZE]
		found = True
	except:
		lastModified = 0
		fileSize = 0
		found = False

	if time.time() - lastModified < hoursInterval * 3600 and fileSize > 400000:
		print "Cloud file is up to date"

	else:		
		for a in range(maxRetries):
			try:
				url = mirrors [ random.randint(0, len(mirrors)-1) ]
				print "Downloading", url
				urllib.urlretrieve(url, cloudFile)
				break
			except:
				sys.stderr.write("Could not get cloud file\n")


	return cloudFile


def getStaticNightMap(scriptDirectory, staticDirectory, intenseVersion):
	suffix = "intense"
	if not intenseVersion:
		suffix = "dim"
	else:
		suffix = "intense"
				
	nightMapFile = os.path.join(scriptDirectory, staticDirectory, "night_" + suffix + ".jpg")
	print "Checking for",  nightMapFile
	if os.path.exists(nightMapFile):
		return nightMapFile


def getNasaDayMap(scriptDirectory, nasaDirectory, nasaImageType):

	subFolder = "topobathy"
	
	if nasaImageType == NasaImageType.PLAIN:
		subFolder = "plain"
	elif nasaImageType == NasaImageType.TOPO:
		subFolder = "topo"
	else:
		subFolder = "topobathy"
	
	currentMonth = datetime.datetime.now().month
	currentMapDirectory = os.path.join(scriptDirectory, nasaDirectory, subFolder)
	currentMapFile = os.path.join(currentMapDirectory, str(currentMonth) + ".jpg")

	print "Checking for", currentMapFile

	if os.path.exists(currentMapFile):
		return currentMapFile	
	else:
		if not os.path.exists(currentMapDirectory):
			os.makedirs(currentMapDirectory)

		if nasaImageType == NasaImageType.PLAIN:
			downloadImg = getNasaMonthlyPlainUrl(currentMonth)
		elif nasaImageType == NasaImageType.TOPO:
			downloadImg = getNasaMonthlyTopoUrl(currentMonth)
		else:
			downloadImg = getNasaMonthlyTopoBathyUrl(currentMonth)

		print "Not found, downloading " + downloadImg
		urllib.urlretrieve(downloadImg, currentMapFile)
		return currentMapFile

def getNasaBumpMap(scriptDirectory, nasaDirectory):
	currentTopoDirectory = os.path.join(scriptDirectory, nasaDirectory)
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

def getNasaMonthlyTopoUrl(month):
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


def getNasaMonthlyTopoBathyUrl(month):
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


def getNasaMonthlyPlainUrl(month):
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




if __name__ == '__main__':
	generateWallpaper()
