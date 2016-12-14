# This file is for acquiring statistics on "yellow" region of abnormal cervices
import cervical as cer
import helpers as helps
from logging import info

abnormal = "abnormal"


def main():
    # 1. Parse CLA for image name and init logfile
    main_args = cer.parse_critical_CLA()
    imgname = main_args.img_name

    helps.init_log_file(abnormal, "Abnormal cervix images", "INFO")
    info(imgname)

    # 2. Read in image
    rgbimage = cer.read_image(imgname)
    gsimage = cer.read_image(imgname, False)
    if rgbimage is None or gsimage is None:
        info("EXIT_FAILURE")
        return

    # 3. Blackout glare (i.e. white portions of image)
    rgbimage = cer.blackout_glare(rgbimage)

    # 4. Extract RGB + grayscale
    channels = cer.extract_RGB(rgbimage)
    channels["gray"] = cer.create_grayscale_channel(gsimage)

    # 5. Run stats on each color component
    redstats = cer.channel_stats(channels["red"])
    info("RED")
    helps.print_channel_stats(redstats, True)
    greenstats = cer.channel_stats(channels["green"])
    info("GREEN")
    helps.print_channel_stats(greenstats, True)
    bluestats = cer.channel_stats(channels["blue"])
    info("BLUE")
    helps.print_channel_stats(bluestats, True)
    graystats = cer.channel_stats(channels["gray"])
    info("GRAY")
    helps.print_channel_stats(graystats, True)

    # 6. Write the critical boundaries for RGB to output file
    with open(abnormal+".txt", 'w') as f:
        f.write("red ")
        f.write("%d %d\n" % (redstats["median"], cer.COLORMAX-1))
        f.write("green ")
        f.write("%d %d\n" % (greenstats["median"], cer.COLORMAX-1))
        f.write("blue ")
        f.write("%d %d\n" % (bluestats["firstQrt"], bluestats["median"]))


if __name__ == "__main__":
    main()
