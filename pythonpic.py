import re
import os
import piexif
#exif format: "YYYY:MM:DD HH:MM:SS

def find_format(date):
	date = date.lower()
	#print(date)
	
	dateString = None
	
	#2022_1127_1323xxxx
	m = re.search(r'^\d\d\d\d_\d\d\d\d_\d\d\d\d', date)
	if m != None:
		m = m.group()
		dateString = '{}:{}:{} {}:{}:00'.format(m[0:4], m[5:7], m[7:9], m[10:12], m[12:14])
		print(1)
	
	#photo-2022-09-28-18-18-15xxx
	m = re.search(r'\d\d\d\d-\d\d-\d\d-\d\d-\d\d', date)
	if m != None:
		m = m.group()
		dateString = '{}:{}:{} {}:{}:00'.format(m[0:4], m[5:7], m[8:10], m[11:13], m[14:16])
		print(2)
	
	#image-20221505-1429xxx
	m = re.search(r'^image-\d\d\d\d\d\d\d\d-\d\d\d\d', date)
	if m != None:
		m = m.group()
		dateString = '{}:{}:{} {}:{}:00'.format(m[6:10], m[12:14], m[10:12], m[15:17], m[17:19])
		print(3)
		
	#img-20220406-xxx
	#a controler si mois ou jour
	m = re.search(r'^img-\d\d\d\d\d\d\d\d', date)
	if m != None:
		m = m.group()
		dateString = '{}:{}:{} 10:00:00'.format(m[4:8], m[8:10], m[10:12])
		print(4)
		
	#20180619-0652-xxx
	m = re.search(r'^\d\d\d\d\d\d\d\d-\d\d\d\d', date)
	if m != None:
		m = m.group()
		dateString = '{}:{}:{} {}:{}:00'.format(m[0:4], m[4:6], m[6:8], m[9:11], m[11:13])
		print(5)
		
	return dateString

# list files in directory
files = os.listdir(os.getcwd())

for file in files:
    # make sure file is an image
    if file.lower().endswith(('.jpg', '.jpeg')):
        
        exif_dict = piexif.load(file)
        
        #get date taken
        dateTaken = exif_dict['Exif'][36867]
        if dateTaken is "":
        	exif_dict['Exif'][36867] = "2089:09:29 10:10:10"
        	exif_bytes = piexif.dump(exif_dict)
        	piexif.insert(exif_bytes, file)


