# This file is for containing all functionality used in create_svm and main
import cv2 as cv2
import helpers as helps
from numpy import ones, uint8
from logging import debug

COLORMAX = 256


def parse_SVM_CLA():
    """
    This function is for parsing command line arguments to create_svm.py

    :return dict args: all parsed command line arguments
    """
    import argparse as ap

    par = ap.ArgumentParser(description="Accept user input argument",
                            formatter_class=ap.ArgumentDefaultsHelpFormatter)

    par.add_argument("--full_dir_path",
                     dest="directory",
                     help="full pathname of the directory containing test \
                     images for creating SVM",
                     type=str,
                     default="./TrainingData/")

    par.add_argument("--critical_file",
                     dest="crit_file",
                     help="full pathname of file containing critical values \
                     corresponding to yellow-ish regions of cervix",
                     type=str,
                     default="./abnormal.txt")

    args = par.parse_args()

    if args.directory[-1] != '/':
        args.directory += '/'

    return args


def parse_critical_CLA():
    """
    This function is for parsing command line args to find_critical_vals.py

    :return dict args: all parsed command line arguments
    """
    import argparse as ap

    par = ap.ArgumentParser(description="Accept user input argument",
                            formatter_class=ap.ArgumentDefaultsHelpFormatter)

    par.add_argument("--img_name",
                     dest="img_name",
                     help="full pathname of the image containing critical regi\
                     ons",
                     type=str,
                     default="./dysplasia_roi3.png")

    args = par.parse_args()

    return args


def read_image(image_name, color=True):
    """
    This function reads in an image

    :param str image_name: name of input image
    :param ble color: whether the image should be read in as a color image or \
    not; default is True otherwise a grayscale image will be read
    :return ndarray image: resulting image matrix
    """
    if color is True:
        image = cv2.imread(image_name, 1)
    else:
        image = cv2.imread(image_name, 0)

    return image


def extract_RGB(image):
    """
    This function extracts red, green, and blue content from a color image

    :return dict channels: intensity histograms for each color (R, G, B)
    """
    # NOTE. Should add logging error if color image is not provided
    rows = len(image)
    cols = len(image[0])

    red = 0 * ones(COLORMAX, uint8)
    green = 0 * ones(COLORMAX, uint8)
    blue = 0 * ones(COLORMAX, uint8)

    for row in range(rows):
        for col in range(cols):
            red[image[row][col][2]] += 1
            green[image[row][col][1]] += 1
            blue[image[row][col][0]] += 1

    channels = {"red": red,
                "green": green,
                "blue": blue}

    return channels


def create_grayscale_channel(image):
    """
    This function creates grayscale intensity histogram from grayscale image

    :return ndarray channel: intensity histogram for grayscale
    """
    # NOTE. Should add logging error if color image is provided
    rows = len(image)
    cols = len(image[0])

    channel = 0 * ones(COLORMAX, uint8)
    for row in range(rows):
        for col in range(cols):
            channel[image[row][col]] += 1

    return channel


def channel_stats(channel):
    """
    This function calculates various statistics on an input color channel

    :param ndarray channel: input channel (red, gree, blue, or grayscale)
    :return dict stats: various stats on the input channel data
    """
    maximum = max(channel[1:])
    mode = 1

    total = sum(channel[1:])
    halfTot = total / 2
    qtrTot = halfTot / 2
    cumSum = 0
    firstQrt = 0
    median = 0
    thirdQrt = 0
    found1stQtr = False
    foundMedian = False
    found3rdQtr = False

    cumProdSum = 0

    for i, v in enumerate(channel):
        if i == 0:
            continue
        if channel[-i] == maximum and COLORMAX - i > mode:
            mode = COLORMAX - i
        cumSum += v
        if cumSum >= qtrTot and found1stQtr is False:
            firstQrt = i
            found1stQtr = True
        if cumSum >= halfTot and foundMedian is False:
            median = i
            foundMedian = True
        if cumSum >= 3*qtrTot and found3rdQtr is False:
            thirdQrt = i
            found3rdQtr = True
        cumProdSum += i * v

    mean = cumProdSum / total

    stats = {"mode": mode,
             "firstQrt": firstQrt,
             "median": median,
             "thirdQrt": thirdQrt,
             "mean": mean}

    return stats


def blackout_glare(image, thr=240):
    """
    Blacks out all pixels in a color image that are (near) white

    :param ndarray image: the 2d image matrix
    :param int thr: threshold which all three components must be greater than \
    in order to be considered glare
    :return ndarray image: image matrix without glare
    """
    rows = len(image)
    cols = len(image[0])

    try:
        len(image[0][0])
        color = True
    except TypeError:
        color = False

    if color is True:
        for row in range(rows):
            for col in range(cols):
                if image[row][col][0] >= thr and image[row][col][1] >= thr and\
                        image[row][col][2] >= thr:
                    image[row][col] = (0, 0, 0)
    else:
        for row in range(rows):
            for col in range(cols):
                if image[row][col] >= thr:
                    image[row][col] = 0

    return image


def parse_critical(filename):
    """
    Parses critical values for each color component (RGB) from text file

    :param str filename: input file name containing critical values
    :return dict criticals: each color component matched to its critical range
    """
    import re as regx

    criticals = {}

    with open(filename, 'r') as f:
        for i in range(3):
            line = f.readline()
            mobj = regx.match(r'(\w*) (\d*) (\d*)', line, regx.I)
            if not mobj:
                return {}
                raise SyntaxError
            mvals = mobj.groups()
            try:
                if int(mvals[1]) < 0 or int(mvals[2]) > 255:
                    return {}
                    raise SyntaxError
                criticals[mvals[0]] = (int(mvals[1]), int(mvals[2]))
            except (TypeError, ValueError):
                # Occurs if non-numbers provided for critical vals
                return {}

    return criticals


def critical_pixel_density(image, critical_values):
    """
    Determines percentage of "critical" pixels contained within an image, \
    ensuring to ignore all black pixels

    :param ndarray image: 2d image matrix
    :param dict critical_values: critical value ranges for each color component
    :return float density: calculated density of critical pixels as decimal
    """
    rmin = critical_values["red"][0]
    rmax = critical_values["red"][1]
    gmin = critical_values["green"][0]
    gmax = critical_values["green"][1]
    bmin = critical_values["blue"][0]
    bmax = critical_values["blue"][1]

    rows = len(image)
    cols = len(image[0])
    # NOTE. add error handling for improperly sized input matrix

    count = 0
    image_pixels = 0

    for row in range(rows):
        for col in range(cols):
            if tuple(image[row][col]) != helps.colorDict["black"]:
                image_pixels += 1
            if image[row][col][2] >= rmin and image[row][col][2] <= rmax:
                if image[row][col][1] >= gmin and image[row][col][1] <= gmax:
                    if image[row][col][0] >= bmin and image[row][col][0] <= \
                            bmax:
                        count += 1

    density = count / image_pixels
    # NOTE. add ZeroDivision error handling

    return density
