import os
import re
import requests
import bs4

# make list of the files in the current directory
dir_files = str(os.listdir(os.getcwd()))
# search list for IEEE PDF files and arXiv PDF files
pdf_files = re.findall(r'\d{8}\.pdf|\d{4}\.\d{5}.pdf', dir_files) #fetch numbered pdf
pdf_num = [pdf_files.replace(".pdf", "") for pdf_files in pdf_files] #remove file extension
if len(pdf_files) > 0: #exist pdf file(s)
	# gen URL for accessing IEEE Xplore, scrape title data, and rename file
	for num, old_path in zip(pdf_num, pdf_files):
		if re.match(r'\d{4}\.\d{5}',num): #arXiv pdf		
			# gen URL for accessing arXiv
			access_URL = 'https://arxiv.org/abs/' + num
			# scrape title data
			get_url_info = requests.get(access_URL)
			soup = bs4.BeautifulSoup(get_url_info.text, 'html.parser')
			webtitle = soup.title.text
			title = re.sub(r'\[\d{4}.\d{5}\] ', "", webtitle)
		elif re.match(r'\d{8}',num): #IEEE PDF
			# gen URL for accessing IEEE Xplore
			num_url = num.lstrip('0')
			access_URL = 'https://ieeexplore.ieee.org/document/' + num_url
			# scrape title data
			get_url_info = requests.get(access_URL)
			soup = bs4.BeautifulSoup(get_url_info.text, 'html.parser')
			webtitle = soup.title.text
			title = re.sub(r' - IEEE.*', "", webtitle) # remove journal title
		else: #unsupported PDF
			print("{}.pdf is not supported currently".format(pdf_num))
			continue
		# genarate new filename
		title2 = re.sub(r'[\/:,;*?"<>|]', "", title) # del f***ing char
		new_path = re.sub(r' ', "_", title2) + ".pdf" # add underbar
		# rename
		os.rename(old_path, new_path)
		# plot result
		print("Done. \"" + old_path + "\" -> \"" + new_path + "\"")
else: # Not Found
	print("No PDF files detected.")
