# This file is for unit testing all files from cervical.py
import cervical as cer
import helpers as helps
import cv2 as cv2
from numpy import ones, uint8


def test_read_image():
    """
    Tests functionality of read_image from cervical.py
    """
    # Create and save an image that is just four pixels as such:
    # [RED] [YELLOW]
    # [GREEN] [BLUE]
    test_image = ones((2, 2, 3), uint8)
    test_image[0][0] = helps.colorDict["red"]
    test_image[0][1] = helps.colorDict["yellow"]
    test_image[1][0] = helps.colorDict["green"]
    test_image[1][1] = helps.colorDict["blue"]

    cv2.imwrite("test.jpg", test_image)

    # Read color image and verify values
    clone_image = cer.read_image("./test.jpg")
    assert clone_image.all() == test_image.all()

    # Read grayscale image
    gray_image = cer.read_image("./test.jpg", False)
    assert gray_image.all() != test_image.all()
    assert gray_image.all() != clone_image.all()
    for i in range(2):
        for j in range(2):
            try:
                len(gray_image[i][j])
                assert False
            except TypeError:
                assert gray_image[i][j] >= 0
                assert gray_image[i][j] < 256
