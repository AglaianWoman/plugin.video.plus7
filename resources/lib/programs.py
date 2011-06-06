import sys
import config
import utils
import comm

try:
	import xbmc, xbmcgui, xbmcplugin
except ImportError:
	pass # for PC debugging

def make_programs_list(url):
	params = utils.get_url(url)	

	try:
		program_list = comm.get_series(params["series_id"])
		# fill media list
		ok = fill_programs_list(program_list)
	except:
		# oops print error message
		print "ERROR: %s (%d) - %s" % (sys.exc_info()[2].tb_frame.f_code.co_name, sys.exc_info()[2].tb_lineno, sys.exc_info()[1])
		ok = False

	# send notification we're finished, successfully or unsuccessfully
	xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=ok)


def fill_programs_list(programs):
	try:	
		ok = True
		for prog in programs:

			p = comm.get_program(prog.url_path)
			item_info = p.get_xbmc_list_item()
			item_url = p.make_xbmc_url()

			listitem=xbmcgui.ListItem(label=p.get_list_title(), iconImage=p.get_thumbnail(), thumbnailImage=p.get_thumbnail())
			listitem.setInfo('video', item_info)

			# Build the URL for the program, including the list_info
			url = "%s?play=true&%s" % (sys.argv[0], item_url)

			# Add the program item to the list
			ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=listitem, isFolder=False, totalItems=len(programs))
	except:
		# user cancelled dialog or an error occurred
		print "ERROR: %s (%d) - %s" % ( sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
		ok = False
	return ok
