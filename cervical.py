# This file is for containing all functionality used in create_svm and main
import cv2 as cv2
import helpers as helps
from numpy import ones, uint8
from logging import debug, info, error

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
    debug("Reading image")
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
    debug("Extracting RGB channels from image")
    try:
        rows = len(image)
        cols = len(image[0])
        L = len(image[0][0])
        if L != 3:
            errmsg = "Color image should have exactly 3 components (R,G,B)."
            error(errmsg)
            return {}
    except TypeError:
        errmsg = "Color image must be provided as input to 'extract_RGB'."
        error(errmsg)
        return {}

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
    debug("Extracting grayscale channel from image")
    try:
        rows = len(image)
        cols = len(image[0])
        try:
            len(image[0][0])
            # Should not reach this point! Otherwise, a color image was input
            errmsg = "Color image was provided. Input image to \
            'create_grayscale_channel' must be grayscale only!"
            error(errmsg)
            return []
        except TypeError:
            pass
    except TypeError:
        errmsg = "Invalid image. Should have 2 dimensions."
        error(errmsg)
        return []

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
    debug("Calculating useful statistics on an input color channel")
    maximum = max(channel[1:])
    mode = 1

    modes = [[channel[x], x] for x in range(1, 6)]
    modes.sort()

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
        if i > 5 and v > modes[0][0]:
            modes[0] = [v, i]
            modes.sort()
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

    modeSum = 0
    for m in range(len(modes)):
        modeSum += modes[m][1]
    modeAvg = modeSum / len(modes)
    mean = cumProdSum / total

    stats = {"mode": mode,
             "5modeAvg": modeAvg,
             "firstQrt": firstQrt,
             "median": median,
             "thirdQrt": thirdQrt,
             "mean": mean}

    return stats


def remove_glare(input, threshold):
    """
    Remove reflective glare from blue channels data

    :param input: List of RGB values from 0-255 (list)
    :param threshold: threshold for removing glare (int)
    :return: output: List of RGB values from 0-255 after removing glare
    """
    debug("Removing glare")
    # Check the size of input list
    if len(input) != 256:
        addlist = [0]*(256-len(input))
        input = input+addlist

    # Remove reflective glare by removing values greater than threshold
    output = input
    output[threshold+1:] = [0] * (255-threshold)

    return output


def blackout_glare(image, thr=240):
    """
    Blacks out all pixels in a color image that are (near) white

    :param ndarray image: the 2d image matrix
    :param int thr: threshold which all three components must be greater than \
    in order to be considered glare
    :return ndarray image: image matrix without glare
    """
    debug("Blacking out glare")
    try:
        rows = len(image)
        cols = len(image[0])
        L = len(image[0][0])
        if L != 3:
            errmsg = "Color image should have exactly 3 components (R,G,B)."
            error(errmsg)
            return None
    except TypeError:
        errmsg = "Color image must be provided as input to 'extract_RGB'."
        error(errmsg)
        return None

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
    debug("Parsing critical values file")
    import re as regx

    criticals = {}

    with open(filename, 'r') as f:
        for i in range(3):
            line = f.readline()
            mobj = regx.match(r'(\w*) (\d*) (\d*)', line, regx.I)
            if not mobj:
                errmsg = "Improper syntax in input file. A line should read \
                as follows: color num1 num2"
                error(errmsg)
                return {}
            mvals = mobj.groups()
            try:
                if int(mvals[1]) < 0 or int(mvals[2]) > 255:
                    errmsg = "Critical value bounds are invalid. Cannot be \
                    less than 0 or greater than 255."
                    error(errmsg)
                    return {}
                criticals[mvals[0]] = (int(mvals[1]), int(mvals[2]))
            except (TypeError, ValueError):
                errmsg = "Expected to parse number values"
                error(errmsg)
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
    debug("Calculating critical pixell density")
    rmin = critical_values["red"][0]
    rmax = critical_values["red"][1]
    gmin = critical_values["green"][0]
    gmax = critical_values["green"][1]
    bmin = critical_values["blue"][0]
    bmax = critical_values["blue"][1]

    try:
        rows = len(image)
        cols = len(image[0])
        L = len(image[0][0])
        if L != 3:
            errmsg = "Color image should have exactly 3 components (R,G,B)."
            error(errmsg)
            return None
    except TypeError:
        errmsg = "Color image must be provided as input to \
        'critical_pixel_density'."
        error(errmsg)
        return None

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

    try:
        density = count / image_pixels
    except ZeroDivisionError:
        errmsg = "Invalid input image. It only contains black pixels."
        error(errmsg)
        return None

    return density


def read_jsonfile(infile):
    """
    Read data parameters from json file

    :param str infile: input json filename
    :return dict params: contains all parsed key-value pairs from JSON object
    """
    debug("Reading input JSON file")
    from json import load

    try:
        file = open(infile, 'r')
        params = load(file)
    except FileNotFoundError:
        print('Error: file not found')
        params = {'a': [], 'b': []}

    return params


def rearrange_svm(param1a, param1b, param2a, param2b):
    """
    Rearrange data for svm

    :param list param1a: 1st statstical analysis of data that is in category a
    :param list param1b: 1st statstical analysis of data that is in category b
    :param list param2a: 2nd statstical analysis of data that is in category a
    :param list param2b: 2nd statstical analysis of data that is in category b
    :return dict output: a map of for each set of data
    """
    debug("Rearranging SVM data")
    import numpy as np

    # Check that the list size is consistent
    if len(param1a) != len(param2a):
        if len(param1a) > len(param2a):
            param1a = param1a[0:len(param2a)]
        if len(param2a) > len(param1a):
            param2a = param2a[0:len(param1a)]
    if len(param1b) != len(param2b):
        if len(param1b) > len(param2b):
            param1b = param1b[0:len(param2b)]
        if len(param2b) > len(param1b):
            param2b = param2b[0:len(param1b)]

    # Rearrange data and convert to np.array
    x = param1a + param1b
    y = param2a + param2b
    X = [0] * len(x)
    for i in range(0, len(x)):
        X[i] = [x[i], y[i]]
    X = np.array(X)

    # Differentiate two data set
    Y = [0] * len(param2a) + [1] * len(param2b)

    return {'X': X, 'Y': Y}


def find_svm(X, Y):
    """
    Find support vector machine from two parameters of input

    :param ndarray X: rearranged array of input
    :param list Y: list to specify groups of data
    :return dict output: metadata for support vector creation
    """
    debug("Finding support vector")
    from sklearn import svm

    clf = svm.SVC(kernel='linear', C=1.0)
    output = clf.fit(X, Y)

    return output


def save_svm_model(clf, filename):
    """
    Save svm model

    :param dict clf: metadata for svm model
    :param str filename: filename to be saved
    """
    debug("Saving support vector")
    from sklearn.externals import joblib
    joblib.dump(clf, filename)

    return


def parse_main():
    """
    This function is for parsing command line arguments to cervical_main.py

    :return dict args: all parsed command line arguments
    """
    import argparse as ap

    par = ap.ArgumentParser(description="Accept user input argument",
                            formatter_class=ap.ArgumentDefaultsHelpFormatter)

    par.add_argument("-full_img_path",
                     dest="image_name",
                     help="full pathname of the image to be classified",
                     type=str)

    par.add_argument("--SVM_filename",
                     dest="svm_file",
                     help="Full filename containing metadata for the support \
                     vector to be used to classify input image",
                     type=str,
                     default="svm_model.pkl")

    par.add_argument("--log_level",
                     dest="log_level",
                     help="Desired level of logging to log file for program",
                     type=str,
                     default="INFO")

    args = par.parse_args()

    return args


def print_diagnosis(img_name, classification_id, log=False):
    """
    Prints the diagnosis of a cervix image

    :param str img_name: name of the input cervix image
    :param int classification_id: previously determined number that associates\
     the cervical image with diagnostic class (0 for healthy, 1 for dysplastic)
    :param ble log: whether or not the printed message should also be logged \
    to a file
    """
    debug("Printing diagnosis")
    diagnosis = img_name+" is %s.\n"
    if classification_id == 0:
        d_class = "healthy"
    else:
        d_class = "dysplastic"

    print(diagnosis % d_class)
    if log is True:
        info(diagnosis % d_class)

    return
