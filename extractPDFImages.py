#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extractPDFImages.py

Created by Jaime Stark on 7/6/2022

This script comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to
redistribute it under certain conditions.
See 'LICENSE.txt' for details.

DESCRIPTION
This script is used to extract images from PDFs. If the image has a
soft mask, the script will attempt to apply it.  The resulting images
are output in a new folder named after the PDF.  

To use this script, you must have pdfimages installed and executable.

This script will extract the images from all PDFs in the same folder as
the script.

By default, the script will merge soft masks, remove duplicate images,
and filter out images under a certain size (default = 325x325 pixels).

USAGE
python3 extractPDFImages.py [WIDTH] [HEIGHT]
"""

import PIL.Image
import os
import sys
import subprocess
import hashlib

def filterSize(width, height, path):
    print("  - Filtering out images under", width, "x", height, "pixels")
    imgfiles = sorted(os.listdir(path))
    for imgfile in imgfiles:
        if imgfile.lower().endswith(".png") or imgfile.lower().endswith('.jpg') or imgfile.lower().endswith(".tif") or imgfile.lower().endswith(".jp2"):
            img = PIL.Image.open(path + "/" + imgfile)
            w, h = img.size
            if (w < width) or (h < height):
                img.close()
                os.remove(path + "/" + imgfile)
            else:
                img.close()

def removeDuplicates(path):
    print("  - Removing duplicates")
    duplicates = []
    hash_keys = dict()
    
    for index, imgfile in enumerate(os.listdir(path)):
        if imgfile.lower().endswith(".png") or imgfile.lower().endswith(".jpg") or imgfile.lower().endswith(".tif") or imgfile.lower().endswith(".jp2"):
			# print(imgfile)
            with open(path + "/" + imgfile, 'rb') as f:
                filehash = hashlib.md5(f.read()).hexdigest()
                if filehash not in hash_keys:
                    hash_keys[filehash] = index
					# print(imgfile, "not a duplicate")
                else:
                    duplicates.append((index, hash_keys[filehash]))
					# print(imgfile, "is a duplicate")
                
    file_list = os.listdir(path)
		# print(duplicates)
    for duplicate in duplicates:
        # print(file_list[duplicate[0]], "is duplicate of", file_list[duplicate[1]])
        os.remove(path + "/" + file_list[duplicate[0]])

def autoMergeMask(merge_list, path):
    print("  - Merging soft masks")
    imgfiles = sorted(os.listdir(path))
    for i, imgfile in enumerate(imgfiles):
        if imgfile.lower().endswith(".png") or imgfile.lower().endswith('.jpg') or imgfile.lower().endswith(".tif") or imgfile.lower().endswith(".jp2"):
            # print(imgfile)
            smask_num = imgfile[:-4].rpartition("-")[2].lstrip("0")
            if smask_num in merge_list:
                # print("SMASK", smask_num)  

                image_num = int(smask_num) - 1
                smask_file = path + "/" + imgfile
                smask = PIL.Image.open(smask_file).convert("L")
                image_file_prefix = path + "/" + imgfile[:-4].rpartition('-')[0] + "-" + zeroFill(str(image_num))
                try:
                    image_file = image_file_prefix + ".png"
                    image = PIL.Image.open(image_file)
                except:
                    try:
                        image_file = image_file_prefix + ".jpg"
                        image = PIL.Image.open(image_file)
                    except:
                        try:
                            image_file = image_file_prefix + ".tif"
                            image = PIL.Image.open(image_file)
                        except:
                            try: 
                                image_file = image_file_prefix + ".jp2"
                                image = PIL.Image.open(image_file)
                            except:
                                print("  - WARNING:", image_file_prefix, "does not exist to merge with SMASK - ", smask_file)
                                continue
                
                if smask.size != image.size:
                    print("  - WARNING:", image_file, "is not the same size as", smask_file)
                    continue
                
                image.putalpha(smask)

                os.remove(smask_file)
                os.remove(image_file)
                   
                image.save(image_file[:-4] + ".png")
                image.close()
                smask.close()
        
def zeroFill(strnum):
    while len(strnum) < 3:
        strnum = "0" + strnum
    return(strnum)

def createFilePrefix(name):
    "Create prefix from PDF filename"
    name0 = name.replace(".pdf", "")
    name1 = name0.replace(" - ", "_")
    name2 = name1.replace(" ", "_")
    return(name2)

def createMergeList(output):
    merge_list = []
    output_lines = output.decode("utf-8").split('\n')
    for i,line in enumerate(output_lines):
        if i <= 1:
            continue
        newline = line.split()
		# print(newline)
        try:
            if newline[2] == "smask":
                merge_list.append(newline[1])
        except:
            continue
    return(merge_list)

def renamePDF(filename):
    file = filename
    newfilename = file
    if "\'" in newfilename:
        newfilename = newfilename.replace("\'", "")
    if "," in filename:
        newfilename = newfilename.replace(",", "")
    os.rename(filename, newfilename)
    return(newfilename)

try:
    if len(sys.argv) == 2 :
        width, height = int(sys.argv[1]), int(sys.argv[1])
    elif len(sys.argv) == 3:
        width, height = int(sys.argv[1]), int(sys.argv[2])
    else:
        width, height = 325, 325
except:
    print("Invalid size dimensions. Integers only.")
    width, height = 325, 325

print(width, height)

files = sorted(os.listdir("."))

for i, file in enumerate(files):
    if file.lower().endswith(".pdf"):
        print(file)
        filename = renamePDF(file)
        print("#" + str(i) + ": " + filename)
        output = subprocess.check_output(['pdfimages', '-list', filename])
        
        merge_list = createMergeList(output)
        
        root = createFilePrefix(filename)
        
        if os.path.exists(root) == False:
            os.makedirs(root)
    
        command = 'pdfimages -all -p \"../' + filename + '\" ' + root
        
        os.chdir(root)
        
        os.system(command)
        
        os.chdir("..")
        
        autoMergeMask(merge_list, root)
        
        removeDuplicates(root)
        
        filterSize(width, height, root)
        
print("FINISHED")