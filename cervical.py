# This file is for containing all functionality used in create_svm and main
import cv2 as cv2
from numpy import ones, uint8

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
