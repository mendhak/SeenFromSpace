#!/usr/bin/python

import random, urllib, sys, stat, time, os, datetime, subprocess, re
from xml.etree.ElementTree import ElementTree
import dateutil.parser
from generators import earth




def setWallpaper(imagePath):
	print "Setting wallpaper"

	retVal = subprocess.call(["gconftool-2", 
					"--set", "/desktop/gnome/background/picture_filename", imagePath, 
					"--type", "string"])
	


def generateWallpaper():
     
	workingDirectory = os.path.join(os.getenv("HOME"), ".seenfromspace")
	programDirectory = os.path.abspath(os.path.dirname(sys.argv[0]))

	copyStaticFiles(programDirectory, workingDirectory)	

	gen = earth.generator(workingDirectory)
	dayMap = gen.getDayMap()
	topoMap = gen.getBumpMap()
	nightMap = gen.getNightMap()
	cloudMap = gen.getCloudMap()
	quakeMarker = gen.getEarthquakeList()

	config = getXPlanetConfig(workingDirectory, dayMap, topoMap, nightMap, cloudMap, quakeMarker)

	xplanetPath = os.path.join(workingDirectory, "xplanet.jpg")
	cropPath = os.path.join(workingDirectory, "crop.jpg")
	finalPath = os.path.join(workingDirectory, "final.jpg")

	if config:
		print "Invoking xplanet"
		retVal = subprocess.call(["xplanet", 
					"-config", config, 
					"-projection", "mercatorial", 
					"-quality", "95", 
					"-verbosity", "-1", 
					"-geometry", "2400x1200", 
					"-num_times", "1", 
					"-body", "earth", 
					"-output", xplanetPath ])

		print "Cropping bottom"
		retVal = subprocess.call(["convert", "-crop", "2400x1200+0-150", xplanetPath, cropPath])

		print "Cropping top"
		retVal = subprocess.call(["convert", "-crop", "2400x1200+0+100", "-resize", "1280x800!", cropPath, finalPath ])
		
		print "Deleting temporary files"
		os.remove(cropPath)
		os.remove(xplanetPath)
		os.remove(config)
		setWallpaper(finalPath)
	

def copyStaticFiles(programDirectory, workingDirectory):
	print "Copying static files from {0}/static to {1}/static".format(programDirectory, workingDirectory)
	subprocess.call(["cp", "-r", os.path.join(programDirectory, "static"), os.path.join(workingDirectory, "static")])


def getXPlanetConfig(workingDirectory, dayMap, topoMap, nightMap, cloudMap, quakeMarker):
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
	if quakeMarker:
		configContents += "marker_file=" + quakeMarker +  "\n"
	configContents += "marker_fontsize=28\n"
	
	configFile = os.path.join(workingDirectory, "temp.config")
	print "Creating", configFile
	with open(configFile, 'w') as tempConfig:
		tempConfig.write(configContents)
		return configFile



if __name__ == '__main__':
	generateWallpaper()
