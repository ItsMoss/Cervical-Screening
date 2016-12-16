# BME590 Final Project
## Cervical Cancer Screening
## Authors: Moseph Jackson-Atogi, Tamma Ketsiri

The goal of this project is to be able to successfully classify clinical images of cervices as healthy or dysplastic. The cervices are stained with Lugol's iodine to help with diagnosis. Dysplastic cervix images should contain more yellowish blotches, while healthy cervix images should remain more brown in response to Lugol's iodine staining. From this known difference in color, along with a priori knowledge of test cervix images that are either healthy or dysplastic, we have developed two programs: one that is responsible for creating a support vector based of test images for training, and a second (main) program that uses the support vector from the trainiing images and is able to take in a new image and classify it as healthy or dysplastic. For our support vector creation we focus on two parameters:
1. Critical pixel density
2. Blue channel mode

The critical pixel density that we refer to is essentially calculating the proportion of pixels in a given image, relative to the amount of pixels that make up the ROI (or cervix), that fall into a "critical" range. The critical range is basically a range for each color component that encompasses the majority of yellowish (dysplastic) regions within an image. For each pixel where all three color components fall into their respective critical ranges, they are considered a "critical" pixel

The blue channel mode is basically looking at the mode, or most common intensity, in the blue channel only, for a given image. This is determined after removing glare from an image, which largely due to the blue component.

After these parameters are determined for any given image, they can be compared against the support vector and a classification of healthy or dysplastic can be output!

### Files Included
The following is a detailed list of files implemented in this project:

+ `abnormal.txt` - output file from find_critical_vals.py containing "critical" pixel ranges for each color component

+ `cervical_main.py` - main program that determines if an input image of a stained cervix is cancerous or not

+ `cervical.py` - contains all functions implemented in both cervical_main.py and create_svm.py

+ `create_svm.py` - file for creating a support vector based on known cervical images

+ `find_critical_vals.py` - determines "critical" pixels from an image combining distinguishing yellow region of dysplasia images and their RGB components

+ `helpers.py` - includes various helper functions used for both testing and functionality in the main program

+ `requirements.txt` - all packages (dependencies) needed to run our program and test building for continuous integration

+ `test_cervical.py` - contains all unit tests for cervical.py

+ `TrainingData/` - folder containing all test images used for SVM creation

### Running Main
In order to properly run the main program do the following from your terminal:

`python cervical_main.py --help`

This will tell you what command line arguments are needed to successfully run the program.  Three arguments are allowed, one is mandatory. The mandatory aand first argument is the image filename of the cervix to be classified by program. Second is the support vector model to be used for classification. Currently only one exists, so that is the default value and can be ignored, but ideally we would have various support vectors using different combinations of parameters that the user could decide on to determine classification. Third argument is desired level of logging to log file created from running program. This is defaulted to INFO.


### Running Tests
In order to properly run the unit tests do the following:

`py.test -v`
