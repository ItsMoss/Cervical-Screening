# This file is for containing all functionality used in create_svm and main


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
