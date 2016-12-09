# This file is for containing all functionality used in create_svm and main
import cv2 as cv2


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
