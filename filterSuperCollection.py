import os
import pprint
import re
import shutil
import sys

rootdir = sys.argv[1]
spectrumdata = {}
filtercount = 0
nocompatcount = 0
russiancount = 0

if not (os.path.exists(os.path.join(rootdir,'Filtered'))):
	os.mkdir(os.path.join(rootdir,'Filtered'))

if not (os.path.exists(os.path.join(rootdir,'NoTZXorZ80'))):
	os.mkdir(os.path.join(rootdir,'NoTZXorZ80'))

for file in os.listdir(rootdir):
	if os.path.isfile(os.path.join(rootdir,file)):
		m = re.search('(?P<filename>.*) \((?P<versioninfo>.*)\.(?P<extension>.{3})',file)
		if (m):
			gamename = m.group('filename')
			gameinfo = '(' + m.group('versioninfo')
			gameextension = m.group('extension')
			# Remove russian games.
			if (re.search('\(ru\)',gameinfo)):
				russiancount += 1
				fullname = gamename + ' ' + gameinfo + '.' + gameextension
				print("Removing russian: " + fullname)
				shutil.move(os.path.join(rootdir,fullname),os.path.join(rootdir,'Filtered'))
			elif gamename not in spectrumdata:
				spectrumdata.update({ gamename: {gameinfo : [gameextension]}})
			else:
				if gameinfo not in spectrumdata[gamename]:
					spectrumdata[gamename].update({gameinfo : [gameextension]})
				else:
					spectrumdata[gamename][gameinfo].append(gameextension)
				
for gamename in spectrumdata:
	for gameinfo in spectrumdata[gamename]:
		foundtzx = False
		foundz80 = False
		foundtap = False
		if 'tzx' in spectrumdata[gamename][gameinfo]:
			foundtzx = True
			spectrumdata[gamename][gameinfo].remove('tzx')
		elif 'z80' in spectrumdata[gamename][gameinfo]:
			foundz80 = True
			spectrumdata[gamename][gameinfo].remove('z80')
		if (foundtzx or foundz80) and spectrumdata[gamename][gameinfo]:
			for gameextension in spectrumdata[gamename][gameinfo]:
				filtercount += 1
				shutil.move(os.path.join(rootdir,gamename + ' ' + gameinfo + '.' + gameextension),os.path.join(rootdir,'Filtered'))
		elif spectrumdata[gamename][gameinfo]:
			for gameextension in spectrumdata[gamename][gameinfo]:
				nocompatcount += 1
				shutil.move(os.path.join(rootdir,gamename + ' ' + gameinfo + '.' + gameextension),os.path.join(rootdir,'NoTZXorZ80'))
				
#pp = pprint.PrettyPrinter(indent=2)
#pp.pprint(spectrumdata)
print("Filtered {} games".format(filtercount))
print("NoTZXorZ80 {} games".format(nocompatcount))
print("Removed {} russians".format(russiancount))
