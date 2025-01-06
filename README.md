# MarkerBasedSegmentation

## Segmenting the image
### Use whatever method you want to segment and save it as a *_mask.tif* file, or adjust following scripts to match the structure

## Making the markers
### Use the *make_markers.py* script
### Hopefully the csv file and directory structure is similar, but if not the concept can be used and loading can be adjusted
### It creates a *_classes.tif* image that has the centroids filled with the class numbers

## Watershedding the markers
### Use the *marker_watershed.m* to split the segmentation masks with the classes markers
### I had much more experience watershedding in matlab, but the same concept can be done in python but I'm not sure exactly how to do it
### Lmk if you have Qs I'll help where I can
