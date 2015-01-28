import urllib.request,os
seq = range(1,15)
dest_dir = r'C:/Users/graham/Dropbox/DOCS/data/Large Scale Optimization'

def get_urls(seq):
	url = r'http://users.ece.utexas.edu/~cmcaram/EE381V_2012F/Lecture_{}_Scribe_Notes.final.pdf'.format
	return map(url,seq)

def get_files(seq):
	name = os.path.join(dest_dir,r'L{} Large Scale Optimization.pdf').format
	return map(name,seq)

def download(url,file):
	request_spec = urllib.request.Request(url)
	request_spec.add_header("User-Agent","Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11")
	print("urllib.request.Request")
	items = request_spec.__dict__.items()
	for key,val in items:
		print('\t{} = {}'.format(key,val))
	try:
		print("\n\nATTEMPTING TO OPEN URL REQUEST\n\n")
		socket = urllib.request.urlopen(request_spec)
		print("urllib.request.urlopen(Request)")
		items = socket.__dict__.items()
		for key,val in items:
			print('\t{} = {}'.format(key,val))
		print("\n\nDOWNLOADING DATA\n\n")
		web_data = socket.read()
		
		data_dir = os.path.split(file)[0]
		if len(data_dir) > 0 and not os.path.isdir(data_dir):
			print("creating directory: {}".format(data_dir))
			os.mkdir(data_dir)
		print("\n\nSAVING DATA: {}\n\n".format(file))
		FILE = open(file,"wb")
		FILE.write(web_data)
		FILE.close()
		print("\n\nDATA SAVED\n\n")
	except urllib.error.HTTPError as e:
		print('{}\t\turl={}'.format(e,url))
def download_many(urls,files):
	urls = list(urls)
	files = list(files)
	for i in range(len(urls)):
		download(urls[i],files[i])
download_many(get_urls(seq),get_files(seq))

