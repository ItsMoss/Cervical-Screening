# This file is for unit testing all files from cervical.py
import cervical as cer
import helpers as helps
import cv2 as cv2
from numpy import ones, uint8
from random import randrange

COLORMAX = 256


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


def test_extract_RGB():
    """
    Tests functionality of extract_RGB from cervical.py
    """
    # Test image matrix 1 (random)
    topleft = (randrange(COLORMAX), randrange(COLORMAX), randrange(COLORMAX))
    topright = (randrange(COLORMAX), randrange(COLORMAX), randrange(COLORMAX))
    botleft = (randrange(COLORMAX), randrange(COLORMAX), randrange(COLORMAX))
    botright = (randrange(COLORMAX), randrange(COLORMAX), randrange(COLORMAX))

    test1 = ones((2, 2, 3), uint8)
    test1[0][0] = topleft
    test1[0][1] = topright
    test1[1][0] = botleft
    test1[1][1] = botright

    output1 = cer.extract_RGB(test1)
    assert output1["red"][topleft[2]] > 0
    assert output1["red"][topright[2]] > 0
    assert output1["red"][botleft[2]] > 0
    assert output1["red"][botright[2]] > 0
    assert sum(output1["red"]) == 4
    assert len(output1["red"]) == COLORMAX
    assert output1["green"][topleft[1]] > 0
    assert output1["green"][topright[1]] > 0
    assert output1["green"][botleft[1]] > 0
    assert output1["green"][botright[1]] > 0
    assert sum(output1["green"]) == 4
    assert len(output1["green"]) == COLORMAX
    assert output1["blue"][topleft[0]] > 0
    assert output1["blue"][topright[0]] > 0
    assert output1["blue"][botleft[0]] > 0
    assert output1["blue"][botright[0]] > 0
    assert sum(output1["blue"]) == 4
    assert len(output1["blue"]) == COLORMAX

    # Test image matrix 2 (random)
    topleft = (randrange(COLORMAX), randrange(COLORMAX), randrange(COLORMAX))
    topright = (randrange(COLORMAX), randrange(COLORMAX), randrange(COLORMAX))
    botleft = (randrange(COLORMAX), randrange(COLORMAX), randrange(COLORMAX))
    botright = (randrange(COLORMAX), randrange(COLORMAX), randrange(COLORMAX))

    test2 = ones((2, 2, 3), uint8)
    test2[0][0] = topleft
    test2[0][1] = topright
    test2[1][0] = botleft
    test2[1][1] = botright

    output2 = cer.extract_RGB(test2)
    assert output2["red"][topleft[2]] > 0
    assert output2["red"][topright[2]] > 0
    assert output2["red"][botleft[2]] > 0
    assert output2["red"][botright[2]] > 0
    assert sum(output2["red"]) == 4
    assert len(output1["red"]) == COLORMAX
    assert output2["green"][topleft[1]] > 0
    assert output2["green"][topright[1]] > 0
    assert output2["green"][botleft[1]] > 0
    assert output2["green"][botright[1]] > 0
    assert sum(output2["green"]) == 4
    assert len(output1["green"]) == COLORMAX
    assert output2["blue"][topleft[0]] > 0
    assert output2["blue"][topright[0]] > 0
    assert output2["blue"][botleft[0]] > 0
    assert output2["blue"][botright[0]] > 0
    assert sum(output2["blue"]) == 4
    assert len(output1["blue"]) == COLORMAX
    assert len(output1) == len(output2)


def test_create_grayscale_channel():
    """
    Tests functionality of create_grayscale_channel from cervical.py
    """
    # Test image matrix 1 (random)
    topleft = (randrange(COLORMAX))
    topright = (randrange(COLORMAX))
    botleft = (randrange(COLORMAX))
    botright = (randrange(COLORMAX))

    test1 = ones((2, 2), uint8)
    test1[0][0] = topleft
    test1[0][1] = topright
    test1[1][0] = botleft
    test1[1][1] = botright

    output1 = cer.create_grayscale_channel(test1)
    assert output1[topleft] > 0
    assert output1[topright] > 0
    assert output1[botleft] > 0
    assert output1[botright] > 0
    assert sum(output1) == 4
    assert len(output1) == COLORMAX

    # Test image matrix 2 (random)
    topleft = (randrange(COLORMAX))
    topright = (randrange(COLORMAX))
    botleft = (randrange(COLORMAX))
    botright = (randrange(COLORMAX))

    test2 = ones((2, 2), uint8)
    test2[0][0] = topleft
    test2[0][1] = topright
    test2[1][0] = botleft
    test2[1][1] = botright

    output2 = cer.create_grayscale_channel(test2)
    assert output2[topleft] > 0
    assert output2[topright] > 0
    assert output2[botleft] > 0
    assert output2[botright] > 0
    assert sum(output2) == 4
    assert len(output2) == COLORMAX


def test_channel_stats():
    """
    Tests functionality of channel_stats from cervical.py
    """
    # Test channel 1
    test1 = ones(COLORMAX, uint8)
    test1[0] = COLORMAX  # this should not affect results
    output1 = cer.channel_stats(test1)
    assert output1["mode"] == 255
    assert output1["firstQrt"] == 64
    assert output1["median"] == 128
    assert output1["thirdQrt"] == 192
    assert output1["mean"] == 128

    # Test channel 2 - Pseudo random
    test2 = 0 * ones(COLORMAX, uint8)
    randMode = randrange(COLORMAX)
    randval1 = randrange(COLORMAX)
    randval2 = randrange(COLORMAX)
    randval3 = randrange(COLORMAX)
    test2[randMode] = 5
    test2[randval1] += 1
    test2[randval2] += 1
    test2[randval3] += 1
    output2 = cer.channel_stats(test2)
    assert output2["mode"] == randMode
    assert output2["median"] == randMode
    assert output2["firstQrt"] == randMode or output2["thirdQrt"] == randMode
    assert output2["firstQrt"] <= randMode
    assert output2["thirdQrt"] >= randMode
    assert output2["mean"] == (randval1 + randval2 + randval3 + 5*randMode) / 8

    # Test channel 3 - Random
    test3 = ones(COLORMAX, uint8)
    for i, v in enumerate(test3):
        test3[i] = randrange(11) * v

    maxval = max(test3[1:])

    output3 = cer.channel_stats(test3)
    assert output3["mode"] > 0 and output3["mode"] < 256
    assert test3[output3["mode"]] == maxval
    assert output3["median"] > 0 and output3["median"] < 256
    assert output3["mean"] > 0 and output3["mean"] < 256
    assert output3["firstQrt"] <= output3["median"]
    assert output3["median"] <= output3["thirdQrt"]


def test_blackout_glare():
    """
    Tests functionality of blackout_glare from cervical.py
    """
    # Test case 1 - All white image
    test1 = COLORMAX * ones((2, 2), uint8)
    expected = 0 * ones((2, 2), uint8)
    output1 = cer.blackout_glare(test1)
    assert output1.all() == expected.all()

    # Test case 2 - Color image with one white
    # [RED] [WHITE]
    # [GREEN] [BLUE]
    test2 = ones((2, 2, 3), uint8)
    test2[0][0] = helps.colorDict["red"]
    test2[0][1] = helps.colorDict["white"]
    test2[1][0] = helps.colorDict["green"]
    test2[1][1] = helps.colorDict["blue"]

    expected = test2
    expected[0][1] = helps.colorDict["black"]

    output2 = cer.blackout_glare(test2)
    assert output2.all() == expected.all()
