# This file is for running main program
import cervical as cer
import helpers as helps
from sklearn.externals import joblib as jl

success = "EXIT_SUCCESS"
fail = "EXIT_FAILURE"


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
        cer.info(fail)
        return

    # 4. Determine x-axis parameter (critical pixel density)
    criticalvalues = cer.parse_critical("abnormal.txt")
    if criticalvalues == {}:
        cer.info(fail)
        return

    x = cer.critical_pixel_density(image, criticalvalues)
    if x is None:
        cer.info(fail)
        return
    cer.info("Calculated critical pixel density: %.5f" % x)

    # 5. Determine y-axis parameter (blue mean)
    channels = cer.extract_RGB(image)
    if channels == {}:
        cer.info(fail)
        return
    bluestats = cer.channel_stats(channels["blue"])
    if bluestats == {}:
        cer.info(fail)
        return
    y = bluestats["mean"]
    cer.info("Calculated blue channel mean: %.2f" % y)

    # 6. Package x and y into one variable
    unknown = [x, y]

    # 7. Use both calculated parameters to classify image from svmfile data
    svmdata = jl.load(svmfile)
    classification = svmdata.predict(unknown)

    # 8. Print to terminal & log file
    cer.print_diagnosis(imagename, classification, True)

    # DONE
    cer.info(success)


if __name__ == "__main__":
    main()
