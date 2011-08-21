
import random, urllib, sys, stat, time, os

def generateWallpaper():
	
	#download cloud
	#download nasa image for this month
	#download nasa topo
	#downloadClouds("clouds/clouds.jpg")
	downloadNasaMonthly("nasaimages", 9)
	

def downloadNasaMonthlyTopo():
	"""
	http://eoimages.gsfc.nasa.gov/ve/7124/world.topo.200401.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7125/world.topo.200402.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7126/world.topo.200403.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7127/world.topo.200404.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7128/world.topo.200405.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7129/world.topo.200406.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7130/world.topo.200407.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7131/world.topo.200408.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7132/world.topo.200409.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7133/world.topo.200410.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7134/world.topo.200411.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7135/world.topo.200412.3x5400x2700.jpg
	"""


def downloadNasaMonthlyTopoBary():
	"""
	http://eoimages.gsfc.nasa.gov/ve/7100/world.topo.bathy.200401.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7101/world.topo.bathy.200402.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7102/world.topo.bathy.200403.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7103/world.topo.bathy.200404.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7104/world.topo.bathy.200405.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7105/world.topo.bathy.200406.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7106/world.topo.bathy.200407.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7107/world.topo.bathy.200408.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7108/world.topo.bathy.200409.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7109/world.topo.bathy.200410.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7110/world.topo.bathy.200411.3x5400x2700.jpg
	http://eoimages.gsfc.nasa.gov/ve/7111/world.topo.bathy.200412.3x5400x2700.jpg
	"""


def downloadNasaMonthly(nasaDirectory, indexer):
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
					"http://eoimages.gsfc.nasa.gov/ve/7123/world.200412.3x5400x2700.jpg"],
				"topo" : "http://earthobservatory.nasa.gov/Features/BlueMarble/images_bmng/8km/world.topo.200407.3x5400x2700.jpg" 
			    }
	print os.path.exists(os.path.join(nasaDirectory, "plain", str(indexer) + ".jpg"))


def downloadClouds(fileName):

	hoursInterval = 3
	maxRetries = 3
	cloudFile = "clouds/clouds.jpg"

	# The list of mirrors. Add new ones here.
	mirrors = [  "http://xplanet-sydney.inside.net/clouds_2048.jpg",
		     "http://xplanet-lasvegas.inside.net/clouds_2048.jpg",
		     "http://home.megapass.co.kr/~gitto88/cloud_data/clouds_2048.jpg",
		     "http://home.megapass.co.kr/~holywatr/cloud_data/clouds_2048.jpg",
		     "http://www.wizabit.eclipse.co.uk/xplanet/files/mirror/clouds_2048.jpg",
		     "ftp://ftp.iastate.edu/pub/xplanet/clouds_2048.jpg",
		     "http://xplanet.explore-the-world.net/clouds_2048.jpg" ]

	# set output file name

	if(fileName):
		outputFile = fileName
	else:
		outputFile = cloudFile

	try:
		s = os.stat(outputFile)
		mtime = s[stat.ST_MTIME]
		fs = s[stat.ST_SIZE]
		found = True
	except:
		mtime = 0
		fs = 0
		found = False
		pass

	if time.time() - mtime < hoursInterval * 3600 and fs > 400000:
		sys.stderr.write("Cloud file is up to date\n")
		return	

	for a in range(maxRetries):
		try:
			url = mirrors [ random.randint(0, len(mirrors)-1) ]
			sys.stderr.write("Using %s\nDownloading...\n" % url)
			urllib.urlretrieve(url, outputFile)
			break
		except:
			pass
		pass



if __name__ == '__main__':
	generateWallpaper()
