import os
from sys import argv

gameRootFolder = "./csgo"
blackListPath = "map_blacklist.txt"
mapcycleFileName = "mapcycle.txt"
maplistFileName = "maplist.txt"

ETCconstant = 9.5e-08
TotalMapsAdded = 0
TotalMapsRemoved = 0
BlackListedMapsIgnored = 0
ParseWorkshop = False
cmpReadSize = 128000


def initBlacklist(path_to_blacklist):
	BlackListedFiles = []
	if not os.path.exists(path_to_blacklist):
		print("BlackList not found at {}. ignoring...".format(path_to_blacklist))
	else:
		print("BlackList found at {}. Parsing files...".format(path_to_blacklist))
		with open(path_to_blacklist, "r") as blacklist:
			for line in blacklist:
				if not line[0] == "#":
					BlackListedFiles.append(line.strip())
		blacklist.close()
		print("Done parsing blacklisted files")
	return BlackListedFiles

def applyBlackList(BlackList, MapList):
	global BlackListedMapsIgnored
	AllowedMapList = []
	for Map in MapList:
		if Map in BlackList:
			BlackListedMapsIgnored += 1
			continue
		AllowedMapList.append(Map)
	return AllowedMapList

def readMapsFolder(gameroot, checkworkshop):
	workshop_maps = []
	mapsroot = os.path.join(gameroot, "maps/")
	non_workshop_maps = [f for f in os.listdir(mapsroot) if os.path.isfile(os.path.join(mapsroot, f))]
	if checkworkshop:
		workshop_maps_folders_only = []
		workshop_path = os.path.join(mapsroot, "workshop/")
		workshop_maps_folders = os.listdir(workshop_path)
		for folder in workshop_maps_folders:
			if os.path.isdir(os.path.join(workshop_path, folder)):
				workshop_maps_folders_only.append(folder)
		for workshop_map_id in workshop_maps_folders_only:
			workshopmapfiles = os.listdir(os.path.join(workshop_path, workshop_map_id))
			for Map in workshopmapfiles:
				if os.path.isfile(os.path.join(os.path.join(workshop_path, workshop_map_id), Map)):
					workshop_maps.append("workshop/{}/{}".format(workshop_map_id, Map))

	AllMaps = non_workshop_maps + workshop_maps
	AllMaps_purged = removeNonBSP(AllMaps)
	return AllMaps_purged

def removeNonBSP(FileList):
	PurgedList = []
	for file in FileList:
		file_extension = str(os.path.splitext(file)[1])
		if file_extension != ".bsp":
			continue
		PurgedList.append(file.replace('.bsp', ''))
	return PurgedList

def readMapList(gameroot):
	MapList = []
	maplistroot = os.path.join(gameroot, "maplist.txt")
	if not os.path.exists(maplistroot):
		print("Couldn't find the maplist file, ignoring...")
		return MapList
	with open(maplistroot, "r") as maplistfile:
		for line in maplistfile:
			if not line[0] == "#":
				MapList.append(line.strip())
	maplistfile.close()
	return MapList

def writeListToMaplist(gameroot, MapList):
	maplistFilePath = os.path.join(gameroot, "maplist.txt")
	with open(maplistFilePath, 'w') as maplist:
		for maps in MapList:
			maplist.write('%s\n' % maps)
	maplistCyclePath = os.path.join(gameroot, "mapcycle.txt")
	with open(maplistCyclePath, 'w') as mapcycle:
		for maps in MapList:
			mapcycle.write('%s\n' % maps)
	print("Done writing maps.")

def main():
	global TotalMapsAdded, TotalMapsRemoved, BlackListedMapsIgnored

	if not os.path.exists(gameRootFolder):
		print("Game root folder wasn't found!")
		return
	BlackListedFiles = initBlacklist(blackListPath)
	MapsFolderContent = readMapsFolder(gameRootFolder, ParseWorkshop)
	MapListContent = readMapList(gameRootFolder)
	if BlackListedFiles != []:
		print("Removing blacklisted files.")
		MapsFolderContent = applyBlackList(BlackListedFiles, MapsFolderContent)
		print("{} BlackListed maps were ignored.".format(BlackListedMapsIgnored))
	for old_map in MapListContent:
		if not old_map in MapsFolderContent:
			TotalMapsRemoved += 1
	for new_map in MapsFolderContent:
		if not new_map in MapListContent:
			TotalMapsAdded += 1
	writeListToMaplist(gameRootFolder, MapsFolderContent)
	print("{} maps were added and {} were removed".format(TotalMapsAdded, TotalMapsRemoved))

if __name__ == "__main__":
	if len(argv) >= 2 and argv[1] == "workshop":
		ParseWorkshop = True
	main()
