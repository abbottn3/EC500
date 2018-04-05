import json
import TwitterSummarization

import sys
reload(sys)
sys.setdefaultencoding('utf8')

files2delete = []
handles = ['katyperry', 'justinbieber', 'BarackObama', 'YouTube', 'Cristiano', 'jtimberlake', 'NeilTyson', 'BillNye', 'ElonMusk', 'cnnbrk',
'BillGates', 'Oprah', 'BrunoMars', 'Drake', 'espn', 'MileyCyrus', 'KevinHart4real', 'instagram', 'taylorswift13', 'ladygaga']
for user in handles:
	t_handle = user

	# Grabs pic URLs
	pic_urls = TwitterSummarization.twitterDL(t_handle)

	# Returns dictionary of applicable descriptions
	if len(pic_urls) != 0:
		description_dict = TwitterSummarization.gVision_and_FFMPEG(pic_urls, t_handle)

	files2delte = TwitterSummarization.get_files()
	# Delete leftover files
	for delfile in files2delete:
		os.remove(delfile)
