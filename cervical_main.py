# This file is for running main program
import cervical as cer
import helpers as helps


def main():
    # 1. Parse Command Line arguments
    main_args = cer.parse_main()
    dirname = main_args.directory
    tif_file = main_args.tif_filename

    

if __name__ == "__main__":
    main()