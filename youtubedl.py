# Youtube-DL by Regan Russell, 2015
#
# Based on Shell script guide from Dr. Mark Humphrys:
# http://computing.dcu.ie/~humphrys/Notes/UNIX/lab.youtube.html
#
# ITAG values via Fred C. Macall's YTCrack:
# http://users.ohiohills.com/fmacall/ytcrack.txt

import sys
import urllib.request
import urllib.parse
import re
import io

# Dictionary to determine file format based on ITAG value
fileFormats = {
	5	:	'flv',
	13  :	'3GP',
	18	:	'mp4',
	22	:	'mp4',
	34	:	'FLV',
	35	:	'FLV',
	36	:	'3GP',
	37	:	'mp4',
	38	:	'mp4',
	43	:	'webm',
	44	:	'webm',
	45	:	'webm',
	46	:	'webm',
	82	:	'mp4',
	83	:	'mp4',
	84	:	'mp4',
	85	:	'mp4',
	100	:	'webm',
	101	:	'webm',
	102	:	'webm',
	133	:	'mp4',
	134	:	'mp4',
	135	:	'mp4',
	136	:	'mp4',
	137	:	'mp4',
	139	:	'mp4',
	140	:	'mp4',
	141	:	'mp4',
	160	:	'mp4',
	171	:	'webm',
	172	:	'webm',
	242	:	'webm',
	243	:	'webm',
	244	:	'webm',
	245	:	'webm',
	246	:	'webm',
	247	:	'webm',
	248	:	'webm',
	249	:	'webm',
	250	:	'webm',
	251	:	'webm',
	264	:	'mp4',
	266	:	'mp4',
	271	:	'webm',
	272	:	'webm',
	278	:	'webm',
	298	:	'mp4',
	302	:	'webm',
}

# Parses startString line by line, searching for lines that
# contain stringToMatch. If a match is found, the containing
# string is added to the result, which is returned in the end
def parseLinesForMatch(startString, stringToMatch):
	resultString = ''
	buf = io.StringIO(startString)
	while True:
		line = buf.readline()
		if stringToMatch in line:
			resultString += line + '\n'

		if len(line) <= 0:
			break

	return resultString

# Check to make sure we were given enough arguments (required args are just a YouTube URL)
if len(sys.argv) < 2:
	print("Please enter a valid YouTube URL.")
	sys.exit()

# Check if the user specified a quality setting, otherwise default to .FLV
itag = 5
if len(sys.argv) >= 3:
	itag = int(sys.argv[2])

# HTTPS sometimes causes trouble, so convert any HTTPS URLs to HTTP
url = sys.argv[1].replace('https', 'http')

# Try opening a connection to the URL,
# exit the script if something goes wrong.
response = None
try:
	response = urllib.request.urlopen(url)
except:
	print("Error opening URL, exiting.")
	sys.exit()

# Loop through each line of the HTML response and extract lines
# that contain URLs, storing them in urlLines
urlLines = ''
for line in response:
	if 'url=' in line.decode("utf-8"):
		urlLines += line.decode("utf-8") + '\n'

urlLines = urlLines.replace("\"", '\n')			# Replace double quotes with newlines
urlLines = parseLinesForMatch(urlLines, 'url=')	# Trim down to lines that contain URLs
urlLines = urlLines.replace('\\u0026', '\n')	# Replace '\u0026' (Unicode &) with newlines
urlLines = parseLinesForMatch(urlLines, 'url=') # Trim down (again), looking for lines containing URLs
urlLines = parseLinesForMatch(urlLines, 'googlevideo.com') # Look for lines containing googlevideo.com references
urlLines = urlLines.replace('url=', '\n')		# Put each URL on its own new line

# Now we trim each line, removing everything that comes after
# a comma in each line, and making sure each remaining line
# is a link containing 'http'
oldLines = urlLines
urlLines = ''

buf = io.StringIO(oldLines)
while True:
	line = buf.readline().split(',', 1)[0]

	if 'http' in line:
		urlLines += line + '\n'

	if len(line) <= 0:
		break

# The URLs are percent-encoded, so we decode them here
urlLines = urllib.parse.unquote(urlLines)

# Check for itag= to indicate video quality,
# and find the link to the video we want
url = ''
buf = io.StringIO(urlLines)
while True:
	line = buf.readline()
	if ('itag=' + str(itag)) in line:
		url = line
		break

	if len(line) <= 0:
		break

# Finally, try to download the video file and save it to disk!
try:
	fileExt = '.flv'

	if not itag in fileFormats:
		print("Unsupported or invalid ITAG flag, saving as .flv by default")
	else:
		fileExt = fileFormats[itag]

	with urllib.request.urlopen(url) as response, open('video.' + fileExt, 'wb') as video_output:
		video_output.write(response.read())
except:
	print("Unable to download, maybe try a different quality setting?")
	print("Available ITAG values are as follows:")

	buf = io.StringIO(urlLines)
	while True:
		line = buf.readline()
		if 'itag=' in line:
			print(line[line.find('itag='):line.find('itag=') + 8].split('&')[0])

		if len(line) <= 0:
			break