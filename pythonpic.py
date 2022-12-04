#!/usr/bin/env python3
import re
import os
import piexif
#exif format: "YYYY:MM:DD HH:MM:SS

'''
Return list of images in the current folder
'''
def listimg():
    # list files in directory
    files = os.listdir(os.getcwd())
    files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.heic'))]
    print(files)
    return files

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
    
    #get all images in folder
    for file in listimg():
            
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


'''
Rename the file based on the 
Exif dateCreated tag

working on this function
'''
def rename():

    for file in listimg():
            
        exif_dict = piexif.load(file)

        #if dateCreated does not exit as exif info
        #check if it can be computed from file name
        #if yes, create and update exif info.
        #if not do nothing
        if 36867 in exif_dict['Exif'].keys():
            dateString = exif_dict['Exif'][36867]
            #os.rename(file, newname)

'''
Convert all heic files into jpg using imagemagick
heic are deleted once converted
'''
def convertHeic():
    
    #test if imageMagick is installed
    testim = os.popen('mogrify -version').read()
    if 'ImageMagick' not in testim:
        print('Please install ImageMagick. Click any key to confirm and exit', end=': ')
        ex = input()
        exit(0)
    
    files = [f for f in listimg() if f.lower().endswith(('.heic'))]
    countc = 0
    for f in files:
        cmd = 'mogrify -format jpg {}'.format(f)
        os.system(cmd)
        os.remove(f)
        countc += 1
        
    print('{} heic files have been converted into jpg'.format(str(countc)))
        

while(True):
    print('Choose')
    print('[0] to exit')
    print('[1] to create exif data createDate based on name')
    print('[2] to test the script')
    print('[3] to convert heic into jpg')
    
    print('>> ', end="")
    
    ex = input()
    if ex == '0':
        print('Bye!')
        break
    elif ex == '1':
        dateCreate()
        print('Process completed, bye!')
        break
    elif ex == '2':
        listimg()
        break
    elif ex == '3':
        convertHeic()
        break