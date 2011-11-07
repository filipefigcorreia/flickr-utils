#!/usr/bin/python

#My Flickr Set Downloader
#NOTE: To change the image size you'll have to mess around with the URL stuff below. 
#      This should be handled by variables but I'm feeling lazy today.

import flickrapi
import urllib2

api_key  =  'THISISANAPIKEY' #get your own! http://www.flickr.com/services/api/misc.api_keys.html
setID='72157606154373202' #This is where you put your set ID. There should be a better way to do this

flickr = flickrapi.FlickrAPI(api_key)
photoSet = flickr.photosets_getPhotos(photoset_id=setID)
photoSet = photoSet[0]

def download( url ):
	file_name = url.split('/')[-1]
	u = urllib2.urlopen(url)
	f = open(file_name, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print "Downloading: %s Bytes: %s" % (file_name, file_size)

	file_size_dl = 0
	block_sz = 8192
	while True:
	    buffer = u.read(block_sz)
	    if not buffer:
		break

	    file_size_dl += len(buffer)
	    f.write(buffer)
	    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
	    status = status + chr(8)*(len(status)+1)
	    print status,

	f.close()
	return

for photo in photoSet:
	photoID = photo.attrib['id']
	photoInfo = flickr.photos_getInfo(photo_id=photoID)
	photoInfo = photoInfo[0]
	oSecret=photoInfo.attrib['originalsecret']

	download("http://farm%s.static.flickr.com/%s/%s_%s_o.jpg" % (photo.attrib['farm'], photo.attrib['server'], photo.attrib['id'],oSecret))