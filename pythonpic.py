#!/usr/bin/env python3
import re
import os
import piexif
#exif format: "YYYY:MM:DD HH:MM:SS

'''
Use regex to extract data from 
name
'''
def find_format(date):
	date = date.lower()
	#print(date)
	
	dateString = None
	
	#2022_1127_1323xxxx
	m = re.search(r'^\d\d\d\d_\d\d\d\d_\d\d\d\d', date)
	if m != None:
		m = m.group()
		dateString = '{}:{}:{} {}:{}:00'.format(m[0:4], m[5:7], m[7:9], m[10:12], m[12:14])
	
	#photo-2022-09-28-18-18-15xxx
	m = re.search(r'\d\d\d\d-\d\d-\d\d-\d\d-\d\d', date)
	if m != None:
		m = m.group()
		dateString = '{}:{}:{} {}:{}:00'.format(m[0:4], m[5:7], m[8:10], m[11:13], m[14:16])
	
	#image-20221505-1429xxx
	m = re.search(r'^image-\d\d\d\d\d\d\d\d-\d\d\d\d', date)
	if m != None:
		m = m.group()
		dateString = '{}:{}:{} {}:{}:00'.format(m[6:10], m[12:14], m[10:12], m[15:17], m[17:19])
		
	#img-20220414-xxx
	m = re.search(r'^img-\d\d\d\d\d\d\d\d', date)
	if m != None:
		m = m.group()
		dateString = '{}:{}:{} 10:00:00'.format(m[4:8], m[8:10], m[10:12])
		
	#20180619-0652-xxx
	m = re.search(r'^\d\d\d\d\d\d\d\d-\d\d\d\d', date)
	if m != None:
		m = m.group()
		dateString = '{}:{}:{} {}:{}:00'.format(m[0:4], m[4:6], m[6:8], m[9:11], m[11:13])
		
	return dateString

'''
List all pictures in a file 
Extract creation date from name (if possible)
Add the exif data if not existing
'''
def dateCreate():
    # list files in directory
    files = os.listdir(os.getcwd())

    filesModified = 0
    for file in files:
        
        #take only images
        if file.lower().endswith(('.jpg', '.jpeg')):
            
            exif_dict = piexif.load(file)

            #if dateCreated does not exit as exif info
            #check if it can be computed from file name
            #if yes, create and update exif info.
            #if not do nothing
            if 36867 not in exif_dict['Exif'].keys():
                dateString = find_format(file)
                if dateString is not None:
                    exif_dict['Exif'][36867] = dateString
                    exif_bytes = piexif.dump(exif_dict)
                    piexif.insert(exif_bytes, file)
                    print('{} -> {}'.format(dateString, file))
                    filesModified += 1
                    
    print('{} files have been modified'.format(str(filesModified)))


while(True):
    print('Choose')
    print('[0] to exit')
    print('[1] to create exif data createDate based on name')
    
    print('>> ', end="")
    
    ex = input()
    if ex == '0':
        print('Bye!')
        break
    elif ex == '1':
        dateCreate()
        print('Process completed, bye!')
        break