# 2012-04-12 Niko Ehrenfeuchter
# Save all open windows as TIFF files, either as single TIF or as TIFF stack,
# depending on the content of the window (decided separately for each window).

# TODO:
#  * split code into setup() and run()
#  * let the user select a file and decide how it should be split (channel,
#    timepoints, positions, ...) and save it instead of using all open windows

from ij import IJ
from ij.io import FileSaver
from os import path

PluginTitle = '"Save all images" plugin'

def run():
	msg = "<html>"
	
	wm = WindowManager
	wcount = wm.getWindowCount()
	if wcount == 0:
		msg += "No windows open, nothing to do.<br/>"
		IJ.showMessage(PluginTitle, msg)
		return
	msg += "Number of open windows: " + str(wcount) + "<br/>"

	# let the User choose a directory to store the files
	target = DirectoryChooser("Choose target directory").getDirectory()
	if target is None:
		# User canceled the dialog
		msg += "<br/>No directory chosen, aborting.<br/>"
		IJ.showMessage(PluginTitle, msg)
		return
	msg += "Selected '" + target + "'as destination folder.<br/>"
	
	# determine padding width for filenames
	pad = len(str(wcount))

	for i in range(wcount):
		# image ID lists start with 1 instead of 0, so for convenience:
		wid = i + 1
		imp = wm.getImage(wid)
		imgid = wm.getNthImageID(wid)
		#print "window id:", wid, ", imageID:", wm.getNthImageID(wid)
		
		# Construct filename
		filename = 'tile_' + str(wid).zfill(pad) + '.tif'
		filepath = target + '/' + filename
		fs = FileSaver(imp)
		if imp.getImageStackSize() > 1:
			if not fs.saveAsTiffStack(filepath):
				IJ.error("<html>Error saving current image, stopping.")
				return
		else:
			if not fs.saveAsTiff(filepath):
				IJ.error("<html>Error saving current image, stopping.")
				return
	
	msg += "<br/>Successfully saved " + str(wcount) + " files.<br/>"
	IJ.showMessage(PluginTitle, msg)

run()
