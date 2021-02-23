
# maplistGenerator

Simple python script to update and maintain the mapcycle and maplist files for games such as CS:GO.

  

# What it can do:

* Fetch the maps in the maps folder (including the workshop folder) and generate mapcycle.txt and maplist.txt accordingly.

* It supports a blacklist of the maps to avoid adding non needed game default maps.

* It will show you how many maps were added, and how many maps were removed.

  

# Requirements:

* python 3 (Was tested only on python 3.6.9 but other versions should work as well).

  

# Usage:

* Edit the ``gameRootFolder`` variable in ``maplistGenerator.py`` to point directly into the game root folder, relative to the ``maplistGenerator.py`` script (Only ``/`` as a separator!). 
* You can also edit the ``blackListPath`` parameter to blacklist default files you don't want to add to the fastdl. 
* Then you can run the ``maplistGenerator.py`` script, and it should update your mapcyclte.txt and maplist.txt files. 
* You can also run the script with the ``workshop``parameter, like so: ``python3 maplistGenerator.py workshop``, which will make the script look through the workshop folder as well.
