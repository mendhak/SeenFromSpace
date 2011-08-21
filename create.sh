#!/bin/bash


cd /home/mendhak/Code/SeenFromSpace/

python clouds/download_clouds.py "clouds/clouds.jpg"
xplanet -config default -projection mercatorial -quality 95 -verbosity 0 -geometry 2400x1200 -num_times 1 -body earth -output xplanet.jpg 

convert -crop 2400x1200+0-150 xplanet.jpg crop1.jpg
convert -crop 2400x1200+0+100 -resize 1440x900! crop1.jpg final.jpg
#mv final.jpg final.jpg
rm -f crop1.jpg
rm -f xplanet.jpg


