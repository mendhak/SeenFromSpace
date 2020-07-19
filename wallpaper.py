#!/usr/bin/python

import os
import sys
import subprocess
from generators import earth



def setWallpaper(imagePath):
	print("Setting wallpaper")

	retVal = subprocess.call(["gconftool-2", 
					"--set", "/desktop/gnome/background/picture_filename", imagePath,
	                "--set", "/desktop/gnome/background/picture_options", "stretched",
					"--type", "string"
					])
	


def generateWallpaper():
     
	workingDirectory = os.path.join(os.getcwd(), ".seenfromspace")
	programDirectory = os.path.abspath(os.path.dirname(sys.argv[0]))

	copyStaticFiles(programDirectory, workingDirectory)	

	gen = earth.generator(workingDirectory)
	dayMap = gen.getDayMap()
	topoMap = gen.getBumpMap()
	nightMap = gen.getNightMap()
	cloudMap = gen.getCloudMap()
	
	quakeMarker = gen.getEarthquakeList()

	markers = gen.getMarkers()

	arcs = gen.getArcs()

	projection = gen.getProjection()
	dimensions = gen.getDimensions()

	latitude = gen.getLatitude()
	longitude = gen.getLongitude()
	origin = gen.getOrigin()
	zoom = gen.getZoom()
	cropTop = gen.getCropTop()
	cropBottom = gen.getCropBottom()
	satelliteFile = gen.getSatellitesList()

	config = getXPlanetConfig(workingDirectory, dayMap, topoMap, nightMap, cloudMap, markers, arcs, satelliteFile)

	xplanetPath = os.path.join(workingDirectory, "xplanet.jpg")
	cropPath = os.path.join(workingDirectory, "crop.jpg")
	finalPath = os.path.join(workingDirectory, "final.jpg")



	if config:
		print("Invoking xplanet")
		xargs = ["xplanet", 
					"-config", config, 
					"-projection", projection, 
					"-quality", "100", 
					"-verbosity", "-1", 
					"-geometry", "2400x1200", 
					"-num_times", "1", 
					"-body", "earth", 
					"-radius", str(zoom),
					"-output", xplanetPath ]
		
		if latitude:
			xargs.append("-latitude")
			xargs.append(str(latitude))
		if longitude:
			xargs.append("-longitude")
			xargs.append(str(longitude))

		if origin:
			xargs.append("-origin")
			xargs.append(origin)

		retVal = subprocess.call(xargs)

		if cropBottom:
			print("Cropping bottom")
			retVal = subprocess.call(["convert", "-crop", "2400x1200+0-" + str(cropBottom), xplanetPath, xplanetPath])

		if cropTop:
			print("Cropping top")
			retVal = subprocess.call(["convert", "-crop", "2400x1200+0+" + str(cropTop), xplanetPath, xplanetPath ])

		print("Resizing")
		retVal = subprocess.call(["convert", "-resize", dimensions + "!", xplanetPath, finalPath])
		
		print("Deleting temporary files")
		os.remove(xplanetPath)
		os.remove(config)
		#setWallpaper(finalPath)
	

def copyStaticFiles(programDirectory, workingDirectory):
	print("Copying static files from {0}/static to {1}/static".format(programDirectory, workingDirectory))
	if not os.path.exists(workingDirectory):
		os.makedirs(workingDirectory)

	subprocess.call(["cp", "-r", os.path.join(programDirectory, "static"), os.path.join(workingDirectory, "static")])


def getXPlanetConfig(workingDirectory, dayMap, topoMap, nightMap, cloudMap, markers, arcs, satelliteFile):
	configContents = "[earth]\n"
	configContents += "shade=45\n"
	configContents += "twilight=11\n"
	configContents += "map=" + dayMap + "\n"
	if nightMap:
		configContents += "night_map=" + nightMap + "\n"
	if topoMap:
		configContents += "bump_map=" + topoMap + "\n"
	if cloudMap:
		configContents += "cloud_map=" + cloudMap + "\n"
	configContents += "cloud_gamma=1.2\n"
	configContents += "cloud_threshold=123\n"
	if markers:
		for marker in markers:
			configContents += "marker_file=" + marker +  "\n"

	configContents += "marker_fontsize=24\n"

	if arcs:
		for arc in arcs:
			configContents += "arc_file=" + arc + "\n"

	if satelliteFile:
		configContents += "satellite_file=" + satelliteFile + "\n"
	
	configFile = os.path.join(workingDirectory, "temp.config")
	print("Creating", configFile)
	with open(configFile, 'w') as tempConfig:
		tempConfig.write(configContents)
		return configFile



if __name__ == '__main__':
	generateWallpaper()
