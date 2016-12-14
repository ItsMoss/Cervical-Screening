# This file is for creating the SVM that will be used in cervical_main.py
import cervical as cer
import helpers as helps
from logging import info

dysplasia = "dysplasia"
healthy = "healthy"
training = "trainingdata"


def main():
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
        filename = dirname+imgname
        # 2a. extract RGB + grayscale
        rgbimage = cer.read_image(filename)
        gsimage = cer.read_image(filename, False)
        if rgbimage is None or gsimage is None:
            break

        info(filename)
        channels = cer.extract_RGB(rgbimage)
        channels["gray"] = cer.create_grayscale_channel(gsimage)

        # 2b. Blue channel analysis
        blue_channels = cer.remove_glare(channels["blue"],240)
        bluestats = cer.channel_stats(channels["blue"])
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
        filename = dirname+imgname
        # 3a. extract RGB + grayscale
        rgbimage = cer.read_image(filename)
        gsimage = cer.read_image(filename, False)
        if rgbimage is None or gsimage is None:
            break

        info(filename)
        channels = cer.extract_RGB(rgbimage)
        channels["gray"] = cer.create_grayscale_channel(gsimage)

        # 3b. Blue channel analysis
        bluestats = cer.channel_stats(channels["blue"])
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

    # 4. Any further analysis here

    # 5. Plot and create SVM

    info("EXIT_SUCCESS")

if __name__ == "__main__":
    main()
