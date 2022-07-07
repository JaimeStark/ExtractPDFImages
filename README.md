# ExtractPDFImages
A script to extract images from PDFs, apply soft mask, remove duplicates, and filter out images below a certain size.

Created by Jaime Stark on 7/6/2022

This script comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to
redistribute it under certain conditions.
See 'LICENSE.txt' for details.

## Description
This script is used to extract images from PDFs. If the image has a
soft mask, the script will attempt to apply it.  The resulting images
are output in a new folder named after the PDF.  

To use this script, you must have [pdfimages](https://en.wikipedia.org/wiki/Pdfimages) installed and executable.

This script will extract the images from all PDFs in the same folder as
the script.

By default, the script will merge soft masks, remove duplicate images,
and filter out images under a certain size (default = 325x325 pixels).

## Usage
`python3 extractPDFImages.py [WIDTH] [HEIGHT]`
