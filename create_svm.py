# This file is for creating the SVM that will be used in cervical_main.py

# parse CLA always comes first!

# 1. Initialize empty lists for both dysplasia and healthy images
# These lists will have elements that are dictionaries whose keys have values
# that are also dictionaries in order to map a channel to a statistical value
# (i.e key=blue, value={mode:x, mean:y, median:z})

# 2. Cylce through all dysplasia images in TrainingData directory

# 2a. extract RGB + grayscale (ignore zeros)

# 2b. Blue channel analysis

# 2c. Green channel analysis

# 2d. Red channel analysis

# 2e. Grayscale channel analysis

# 2f. Update/append list for dysplasia images

# 3. Cycle through all healthy images in TrainingData and repeat 2a-f for them

# 4. Any further analysis here

# 5. Plot and create SVM
