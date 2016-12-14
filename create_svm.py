# This file is for creating the SVM that will be used in cervical_main.py
import cervical as cer
import helpers as helps
from logging import info

dysplasia = "dysplasia"
healthy = "healthy"
training = "trainingdata"


def main():
    # Parse CLA & init log file always comes first!
    main_args = cer.parse_SVM_CLA()
    dirname = main_args.directory
    critfile = main_args.crit_file

    helps.init_log_file(training, "Moss", "INFO")

    # 1. Initialize empty lists for both dysplasia and healthy images
    # These lists will contain counts for each image of how many critical
    # pixels each contains
    allDysplasia = []
    allHealthy = []

    # 2. Parse critical values file
    critVals = cer.parse_critical(critfile)

    # 3. Cylce through all dysplasia images in TrainingData directory
    dys_n = 0
    while True:

        imgname = helps.create_image_name(dysplasia, dys_n)
        filename = dirname+imgname

        # 3a. Read in image
        rgbimage = cer.read_image(filename)
        if rgbimage is None:
            break

        # 3b. Count how many pixels are in critical range
        density = cer.critical_pixel_density(rgbimage, critVals)

        # 3c. Log count for image and append list
        allDysplasia.append(density)
        info(filename)
        info("Critical p: %.5f\n" % density)

        dys_n += 1

    # 4. Cycle through all healthy images in TrainingData and repeat 2a-g
    hea_n = 0
    while True:

        imgname = helps.create_image_name(healthy, hea_n)
        filename = dirname+imgname

        # 4a. Read in image
        rgbimage = cer.read_image(filename)
        if rgbimage is None:
            break

        # 4b. Count how many pixels are in critical range
        density = cer.critical_pixel_density(rgbimage, critVals)

        # 4c. Log count for image and append list
        allHealthy.append(density)
        info(filename)
        info("Critical p: %.5f\n" % density)

        hea_n += 1

    # 5. Any further analysis here

    # 6. Plot and create SVM

    info("EXIT_SUCCESS")

if __name__ == "__main__":
    main()