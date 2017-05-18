import os, sys, re, shutil
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree, tostring

def stripMatch( str ):
	return str.replace("(","").replace(")","").replace("[","").replace("]","")

rootdir = sys.argv[1]
imagedir = sys.argv[2]

spectrumdata = {}

root = Element('gameList')
gameList = ElementTree(root)

if not (os.path.exists(os.path.join(rootdir,'images'))):
	os.mkdir(os.path.join(rootdir,'images'))

files = os.listdir(rootdir)
for file in sorted(files):
	if os.path.isfile(os.path.join(rootdir,file)):
		m = re.match("^(?P<name>[\w\s\-',\.\+\&\!\[\]]+) (?P<year>\(\d{4}\))?(?P<company>\([\w\s\-',\.\+\&\!\[\]]+\))?(?P<aka>\(aka [\w\s\-',\.\+\&\!\[\]]+\))?(?P<lang>\([a-zA-Z]{2,4}\))?(?P<spectrum>\([\s\dkK,\+32]+\))?(?P<meta>.*)\.(?P<extension>\w{3})$",file)
		if m and m.group('name'):
			game = SubElement(root, 'game')
			path = SubElement(game, 'path')
			name = SubElement(game, 'name')
			name.text = m.group('name')
			path.text = './' + file
			imagePath = os.path.join(imagedir, name.text + '.jpg').replace('..','.')
			foundImage = False
			if os.path.isfile(imagePath):
				foundImage = True
			else: 
				imagePath = imagePath.replace('III','3').replace('II','2')
				if os.path.isfile(imagePath):
					foundImage = True
				else:
					n = re.match("^(?P<simpleName>[a-zA-Z \.\']+) -.*$",name.text)
					if n and n.group('simpleName'):
						simpleName = n.group('simpleName')
						imagePath = os.path.join(imagedir,simpleName + '.jpg').replace('..','.')
						if os.path.isfile(imagePath):
							foundImage = True
						else:
							imagePath = imagePath.replace('III','3').replace('II','2')
							if os.path.isfile(imagePath):
								foundImage = True
			if foundImage:
				retroPath = './images/' + name.text + '.jpg'
				destPath = os.path.join(rootdir,retroPath)
				if not os.path.isfile(destPath):
					shutil.copy(imagePath,destPath)
				image = SubElement(game,'image')
				image.text = retroPath
			else:
				print("Cannot find image for " + m.group('name') + " using " + imagePath)
			if m.group('year'):
				year = stripMatch(m.group('year'))
				releaseDate = SubElement(game,'releaseDate')
				releaseDate.text = year + '0101T000000'
			if m.group('company'):
				company = stripMatch(m.group('company'))
				publisher = SubElement(game,'publisher')
				publisher.text = company
			if m.group('aka') or m.group('meta'):
				description = SubElement(game,'desc')
				descriptionText = ""
				if m.group('aka'):
					aka = stripMatch(m.group('aka'))
					descriptionText += aka + os.linesep
				if m.group('meta'):
					meta = stripMatch(m.group('meta').replace(")["," ").replace("]["," "))
					descriptionText += meta + os.linesep
				description.text = descriptionText
			
gameList.write(os.path.join(rootdir,'gamelist.xml.unformatted'),'us-ascii',True)
