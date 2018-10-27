# image_edit
#### Edit single image or bunch of images at once

### Version 0.2.0
- Add `version` function
- Implement `convert` function
- Implement `dir-convert` function
- Program structure modify

##### Options
- convert
- compress
- resize
- dir-convert
- dir-compress
- dir-resize
- version


##### convert
Convert image to **jpeg** format.

    image_edit.py convert INPUTFILE OUTPUTFILE

##### compress
Compress image in **jpeg** format.  
`QUALITY` should be value between `1` and `95`.  
Default value of `QUALITY` is `75` if not specified.

    image_edit.py compress INPUTFILE OUTPUTFILE [QUALITY]

##### resize
Resize image's width and height by dividing to `PROPORTION`.  
`PROPORTION` should be a positive integer.  
Default value of `PROPORTION` is `2` if not specified.   

    image_edit.py resize INPUTFILE OUTPUTFILE [PROPORTION]

##### dir-convert
Convert images in a directory to **jpeg** format

    image_edit.py dir-convert INPUTDIR OUTPUTDIR

##### dir-compress
Compress images of **jpeg** format in a directory.  
`QUALITY` should be value between `1` and `95`

    image_edit.py dir-compress INPUTDIR OUTPUTDIR [QUALITY]

##### dir-resize
Resize images in a directory by dividing width and height to `PROPORTION`.  
`PROPORTION` should be a positive integer.  
Default value of `PROPORTION` is `2` if not specified.  

    image_edit.py dir-resize INPUTDIR OUTPUTDIR [PROPORTION]

##### version
Show current version of the program

    image_edit.py version
