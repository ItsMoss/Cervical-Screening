# This file is for running main program
import cervical as cer
import helpers as helps
from sklearn.externals import joblib as jl


def main():
    # 1. Parse Command Line arguments
    main_args = cer.parse_main()
    imagename = main_args.image_name
    svmfile = main_args.svm_file
    loglevel = main_args.log_level

    # 2. Init log file
    helps.init_log_file("cervical", "Cervical Imaging Classification",
                        loglevel)

    # 3. Read input image (in color)
    image = cer.read_image(imagename)
    if image is None:
        cer.error("Unable to read the provided input image: %r\n" % imagename)

    # 4. Determine x-axis parameter (critical pixel density)
    criticalvalues = cer.parse_critical("abnormal.txt")
    x = cer.critical_pixel_density(image, criticalvalues)
    cer.info("Calculated critical pixel density: %.5f" % x)

    # 5. Determine y-axis parameter (blue mode)
    channels = cer.extract_RGB(image)
    bluestats = cer.channel_stats(channels["blue"])
    y = bluestats["mode"]
    cer.info("Calculated blue channel mode: %d" % y)

    # 6. Package x and y into one variable
    unknown = [x, y]

    # 7. Use both calculated parameters to classify image from svmfile data
    svmdata = jl.load(svmfile)
    classification = svmdata.predict(unknown)

    # 8. Print to terminal & log file
    cer.print_diagnosis(imagename, classification, True)


if __name__ == "__main__":
    main()
