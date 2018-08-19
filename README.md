# image_edit
#### Edit single image or bunch of images at once

### Version 0.1.0

##### Options
- compress
- resize
- dir-compress
- dir-resize

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

##### dir-compress
Compress images of **jpeg** format in a directory.  
`QUALITY` should be value between `1` and `95`

    image_edit.py dir-compress INPUTDIR OUTPUTDIR [QUALITY]

##### dir-resize
Resize images in a directory by dividing width and height to `PROPORTION`.  
`PROPORTION` should be a positive integer.  
Default value of `PROPORTION` is `2` if not specified.  

    image_edit.py dir-resize INPUTDIR OUTPUTDIR [PROPORTION]
