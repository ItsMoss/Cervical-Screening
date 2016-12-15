# This file is for creating the SVM that will be used in cervical_main.py
import cervical as cer
import helpers as helps
from logging import info
import json
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from sklearn import svm

dysplasia = "dysplasia"
healthy = "healthy"
training = "trainingdata"


def svm_param1():

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

        # 3d. Extract RGB channels
        channels = cer.extract_RGB(rgbimage)

        # 3e. Calculate stats on each channel
        redstats = cer.channel_stats(channels["red"])
        greenstats = cer.channel_stats(channels["green"])
        bluestats = cer.channel_stats(channels["blue"])

        # 3f. Print stats
        helps.print_channel_stats(redstats, True)
        helps.print_channel_stats(greenstats, True)
        helps.print_channel_stats(bluestats, True)

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

        # 4d. Extract RGB channels
        channels = cer.extract_RGB(rgbimage)

        # 4e. Calculate stats on each channel
        redstats = cer.channel_stats(channels["red"])
        greenstats = cer.channel_stats(channels["green"])
        bluestats = cer.channel_stats(channels["blue"])

        # 4f. Print stats
        helps.print_channel_stats(redstats, True)
        helps.print_channel_stats(greenstats, True)
        helps.print_channel_stats(bluestats, True)

        hea_n += 1

        #5. Save parameter
        with open('svm_param1.txt', 'w') as f:
            json.dump({"dysplasia":allDysplasia, "healthy":allHealthy}, f)

    info("EXIT_SUCCESS")


def svm_param2():

    # parse CLA & init log file always comes first!
    main_args = cer.parse_SVM_CLA()
    dirname = main_args.directory

    helps.init_log_file(training, "Moss", "INFO")

    # 1. Initialize empty lists for both dysplasia and healthy images
    # These lists will have elements that are dictionaries to dictionaries to
    # dictionaries (this maps an image number to four channels (RGB and
    # grayscale), which map to a statistical value)
    allDysplasia = []
    allHealthy = []

    # 2. Cylce through all dysplasia images in TrainingData directory
    dys_n = 0
    while True:

        imgname = helps.create_image_name(dysplasia, dys_n)
        filename = dirname + imgname
        # 2a. extract RGB + grayscale
        rgbimage = cer.read_image(filename)
        gsimage = cer.read_image(filename, False)
        if rgbimage is None or gsimage is None:
            break

        info(filename)
        channels = cer.extract_RGB(rgbimage)
        channels["gray"] = cer.create_grayscale_channel(gsimage)

        # 2b. Blue channel analysis
        blue_channels = cer.remove_glare(channels["blue"], 240)
        bluestats = cer.channel_stats(blue_channels)
        info("BLUE")
        helps.print_channel_stats(bluestats, True)

        # 2c. Green channel analysis
        greenstats = cer.channel_stats(channels["green"])
        info("GREEN")
        helps.print_channel_stats(greenstats, True)

        # 2d. Red channel analysis
        redstats = cer.channel_stats(channels["red"])
        info("RED")
        helps.print_channel_stats(redstats, True)

        # 2e. Grayscale channel analysis
        graystats = cer.channel_stats(channels["gray"])
        info("GRAYSCALE")
        helps.print_channel_stats(graystats, True)

        # 2f. Create dictionary of dictionary of dictionary
        allstats = {"red": redstats,
                    "green": greenstats,
                    "blue": bluestats,
                    "gray": graystats}

        imagestats = {dys_n: allstats}

        # 2g. Update/append list for dysplasia images
        allDysplasia.append(imagestats)
        dys_n += 1

    # 3. Cycle through all healthy images in TrainingData and repeat 2a-g
    hea_n = 0
    while True:

        imgname = helps.create_image_name(healthy, hea_n)
        filename = dirname + imgname
        # 3a. extract RGB + grayscale
        rgbimage = cer.read_image(filename)
        gsimage = cer.read_image(filename, False)
        if rgbimage is None or gsimage is None:
            break

        info(filename)
        channels = cer.extract_RGB(rgbimage)
        channels["gray"] = cer.create_grayscale_channel(gsimage)

        # 3b. Blue channel analysis
        blue_channels = cer.remove_glare(channels["blue"], 240)
        bluestats = cer.channel_stats(blue_channels)
        info("BLUE")
        helps.print_channel_stats(bluestats, True)

        # 3c. Green channel analysis
        greenstats = cer.channel_stats(channels["green"])
        info("GREEN")
        helps.print_channel_stats(greenstats, True)

        # 3d. Red channel analysis
        redstats = cer.channel_stats(channels["red"])
        info("RED")
        helps.print_channel_stats(redstats, True)

        # 3e. Grayscale channel analysis
        graystats = cer.channel_stats(channels["gray"])
        info("GRAYSCALE")
        helps.print_channel_stats(graystats, True)

        # 3f. Create dictionary of dictionary of dictionary
        allstats = {"red": redstats,
                    "green": greenstats,
                    "blue": bluestats,
                    "gray": graystats}

        imagestats = {hea_n: allstats}

        # 3g. Update/append list for healthy images
        allHealthy.append(imagestats)
        hea_n += 1

        #4. Save parameter
        with open('svm_param2.txt', 'w') as f:
            json.dump({"dysplasia":allDysplasia, "healthy":allHealthy}, f)

    info("EXIT_SUCCESS")


def main():

    #1. Read in params data
    param1 = cer.read_jsonfile('svm_param1.txt')
    param2 = cer.read_jsonfile('svm_param2.txt')

    #2. Reorganize data
    x = param1['heathy']+param1['dysplasia']
    y1 = [0]* len(param1['heathy'])
    y2 = [0]* len(param1['dysplasia'])
    for i in range (0,len(param1['heathy'])):
        y1[i] = param2['heathy'][i][str(i)]['gray']['mean']

    for i in range (0, len(param1['dysplasia'])):
        y2[i] = param2['dysplasia'][i][str(i)]['gray']['mean']
    y = y1+y2

    fig1 = plt.scatter(x[0:12],y1, color = 'red')
    fig1 = plt.scatter(x[12:],y2, color = 'blue')
    plt.xlabel('critical-values')
    filename = 'gray-mean'
    plt.savefig(filename, bbox_inches='tight')
    plt.show(fig1)


    # #3. Find SVM
    # X = [0]*len(x)
    # for i in range (0, len(x)):
    #     X[i] = [x[i], y[i]]
    # X = np.array(X)
    #
    # Y = [0]*len(y1) + [1]*len(y2)
    #
    # clf = svm.SVC(kernel='linear', C=1.0)
    # clf.fit(X, Y)
    #
    # #4. Plot SVM
    # w = clf.coef_[0]
    # print(w)
    #
    # a = -w[0] / w[1]
    #
    # xx = np.linspace(0, 12)
    # yy = a * xx - clf.intercept_[0] / w[1]
    #
    # h0 = plt.plot(xx, yy, 'k-', label="non weighted div")
    #
    # plt.scatter(X[:, 0], X[:, 1], c=y)
    # plt.legend()
    # plt.show()

if __name__ == "__main__":
    main()
