# BME590 Final Project
## Cervical Cancer Screening
## Authors: Moseph Jackson-Atogi, Tamma Ketsiri

[Include description of project here]

### Files Included
The following is a detailed list of files implemented in this project:

+ `abnormal.txt` - output file from find_critical_vals.py containing "critical" pixel ranges for each color component

+ `cervical_main.py` - main program that determines if an input image of a stained cervix is cancerous or not

+ `cervical.py` - contains all functions implemented in both cervical_main.py and create_svm.py

+ `create_svm.py` - file for creating a support vector based on known cervical images

+ `find_critical_vals.py` - determines "critical" pixels from an image combining distinguishing yellow region of dysplasia images and their RGB components

+ `helpers.py` - includes various helper functions used for both testing and functionality in the main program

+ `test_cervical.py` - contains all unit tests for cervical.py

+ `TrainingData/` - folder containing all test images used for SVM creation

### Running Main
In order to properly run the main program do the following:


### Running Tests
In order to properly run the unit tests do the following:

`py.test -v`
