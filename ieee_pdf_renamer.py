import os
import re
import requests
import bs4

# make list of the files in the current directory
dir_files = str(os.listdir(os.getcwd()))

# search list for IEEE PDF files
pdf_files = re.findall(r'[0-9]{8}.pdf', dir_files)
pdf_nums = [pdf_files.replace(".pdf", "") for pdf_files in pdf_files]

if len(pdf_files) > 0:
	# gen URL for accessing IEEE Xplore, scrape title data, and rename file
	for num, old_path in zip(pdf_nums, pdf_files):
		# gen URL for accessing IEEE Xplore
		num_url = num.lstrip('0')
		access_URL = 'https://ieeexplore.ieee.org/document/' + num_url
		# scrape title data
		get_url_info = requests.get(access_URL)
		soup = bs4.BeautifulSoup(get_url_info.text, 'html.parser')
		webtitle = soup.title.text
		title = re.sub(r' - IEEE.*', "", webtitle) # remove journal title
		# genarate new filename
		title2 = re.sub(r'[\/:,;*?"<>|]', "", title) # del f***ing char
		new_path = re.sub(r' ', "_", title2) + ".pdf" # add underbar
		# rename
		os.rename(old_path, new_path)
		# plot result
		print("Done. \"" + old_path + "\" -> \"" + new_path + "\"")
else: # Not Found
	print("No PDF files detected.")
