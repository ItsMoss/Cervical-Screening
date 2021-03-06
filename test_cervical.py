# This file is for unit testing all files from cervical.py
import cervical as cer
import helpers as helps
import cv2 as cv2
from numpy import ones, uint8, array_equal
from numpy.testing import assert_array_equal as assert_equal
from numpy.testing import assert_raises
from random import randrange
from json import dump

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

    cv2.imwrite("test.png", test_image)

    # Read color image and verify values
    clone_image = cer.read_image("./test.png")
    assert_equal(clone_image, test_image)

    # Read grayscale image
    gray_image = cer.read_image("./test.png", False)
    assert_raises(AssertionError, assert_equal, gray_image, test_image)
    assert_raises(AssertionError, assert_equal, gray_image, clone_image)
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
    assert output1["5modeAvg"] == 3
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
    assert output2["5modeAvg"] > 2 and output2["5modeAvg"] < 254
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
    assert output3["5modeAvg"] > 2 and output3["5modeAvg"] < 254
    assert output3["median"] > 0 and output3["median"] < 256
    assert output3["mean"] > 0 and output3["mean"] < 256
    assert output3["firstQrt"] <= output3["median"]
    assert output3["median"] <= output3["thirdQrt"]


def test_remove_glare():
    """
    Tests remove glare functionality from tamma_copy.py
    """
    input1 = [1] * 256
    expected_output1 = [1] * 241 + [0] * 15
    output1 = cer.remove_glare(input1, 240)
    assert output1 == expected_output1

    input2 = [1] * 256
    expected_output2 = [1] * 256
    output2 = cer.remove_glare(input2, 256)
    assert output2 == expected_output2

    input3 = [1] * 256
    expected_output3 = [1] + [0] * 255
    output3 = cer.remove_glare(input3, 0)
    assert output3 == expected_output3


def test_remove_glare_wronginput():
    """
    Tests remove glare functionality from tamma_copy.py
    """
    input1 = [1]*250
    expected_output1 = [1]*241 + [0]*15
    output1 = cer.remove_glare(input1, 240)
    assert output1 == expected_output1

    input2 = [1]*270
    expected_output2 = [1]*241 + [0]*15
    output2 = cer.remove_glare(input2, 240)
    assert output2 == expected_output2


def test_blackout_glare():
    """
    Tests functionality of blackout_glare from cervical.py
    """
    # Test case 1 - All white image
    test1 = COLORMAX * ones((2, 2, 3), uint8)
    expected = 0 * ones((2, 2, 3), uint8)
    output1 = cer.blackout_glare(test1)
    assert_equal(output1, expected)

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
    assert_equal(output2, expected)


def test_parse_critical():
    """
    Tests functionality of parse_critical from cervical.py
    """
    mins = [randrange(128) for x in range(3)]
    maxs = [randrange(128, 256, 1) for x in range(3)]

    # Test case 1 - Valid file
    with open("testcrit1.txt", 'w') as f:
        f.write("green %d %d\n" % (mins[1], maxs[1]))
        f.write("red %d %d\n" % (mins[0], maxs[0]))
        f.write("blue %d %d\n" % (mins[2], maxs[2]))

    output1 = cer.parse_critical("testcrit1.txt")
    assert output1["red"] == (mins[0], maxs[0])
    assert output1["green"] == (mins[1], maxs[1])
    assert output1["blue"] == (mins[2], maxs[2])

    # Test case 2 - Invalid (improper pattern)
    with open("testcrit2.txt", 'w') as f:
        f.write("%d %d green\n" % (mins[1], maxs[1]))
        f.write("red %d %d %d\n" % (mins[0], maxs[0], maxs[0]))
        f.write("%d blue %d\n" % (mins[2], maxs[2]))

    output2 = cer.parse_critical("testcrit2.txt")
    assert output2 == {}

    # Test case 3 - Invalid (critical vals too large/small)
    with open("testcrit3.txt", 'w') as f:
        f.write("green %d %d\n" % (mins[1], 300))
        f.write("red %d %d\n" % (-10, maxs[0]))
        f.write("blue %d %d\n" % (mins[2], maxs[2]))

    output3 = cer.parse_critical("testcrit3.txt")
    assert output3 == {}


def test_critical_pixel_density():
    """
    Tests functionality of critical_pixel_density from cervical.py
    """
    testCritVals = {"red": (240, 255),  # these values are looking for yellow
                    "green": (240, 255),
                    "blue": (0, 25)}
    # Test case 1 - 1/4 pixels match
    img1 = cer.read_image("./test.png")
    output1 = cer.critical_pixel_density(img1, testCritVals)
    assert output1 == 0.25

    # Test case 2 - 0/4 pixels match
    img2 = ones((2, 2, 3), uint8)
    img2[0][0] = helps.colorDict["blue"]
    img2[0][1] = helps.colorDict["blue"]
    img2[1][0] = helps.colorDict["blue"]
    img2[1][1] = helps.colorDict["blue"]

    output2 = cer.critical_pixel_density(img2, testCritVals)
    assert output2 == 0


def test_read_jsonfile():
    """
    Tests read_jsonfile functionality from cervical.py
    """

    # Case 1
    infile1 = 'jsontest.json'
    with open(infile1, 'w') as f:
        dump({"a": [1, 2, 3, 4, 5], "b": [6, 7, 8, 9, 0]}, f)

    output1 = cer.read_jsonfile(infile1)
    a1 = output1['a']
    b1 = output1['b']

    assert a1 == [1, 2, 3, 4, 5]
    assert b1 == [6, 7, 8, 9, 0]

    # Case2
    infile2 = 'jsontest2.json'
    output2 = cer.read_jsonfile(infile2)
    a2 = output2['a']
    b2 = output2['b']

    assert a2 == []
    assert b2 == []


def test_rearrange_svm():
    """
    Test rearrange_svm functionality from cervical.py
    """

    # Case 1
    inlist1a = [1, 2]
    inlist1b = [8, 9]
    inlist2a = [8, 9]
    inlist2b = [1, 2]

    output = cer.rearrange_svm(inlist1a, inlist1b, inlist2a, inlist2b)
    outputX = output['X']
    outputY = output['Y']

    assert array_equal(outputX, [[1, 8], [2, 9], [8, 1], [9, 2]])
    assert outputY == [0, 0, 1, 1]

    # Case 2
    inlist1a = [1, 2, 3]
    inlist1b = [8, 9, 10]
    inlist2a = [8, 9]
    inlist2b = [1, 2]

    output = cer.rearrange_svm(inlist1a, inlist1b, inlist2a, inlist2b)
    outputX = output['X']
    outputY = output['Y']

    assert array_equal(outputX, [[1, 8], [2, 9], [8, 1], [9, 2]])
    assert outputY == [0, 0, 1, 1]

    # Case 3
    inlist1a = [1, 2, 3]
    inlist1b = [8, 9]
    inlist2a = [8, 9]
    inlist2b = [1, 2]

    output = cer.rearrange_svm(inlist1a, inlist1b, inlist2a, inlist2b)
    outputX = output['X']
    outputY = output['Y']

    assert array_equal(outputX, [[1, 8], [2, 9], [8, 1], [9, 2]])
    assert outputY == [0, 0, 1, 1]

    # Case 4
    inlist1a = [1, 2, 3]
    inlist1b = [8, 9]
    inlist2a = [8, 9, 10]
    inlist2b = [1, 2]

    output = cer.rearrange_svm(inlist1a, inlist1b, inlist2a, inlist2b)
    outputX = output['X']
    outputY = output['Y']

    assert array_equal(outputX, [[1, 8], [2, 9], [3, 10], [8, 1], [9, 2]])
    assert outputY == [0, 0, 0, 1, 1]


def test_find_svm():
    """
    Test find_svm functionality from cervical.py
    """
    X = [[5, 0], [4, 1], [3, 2], [2, 3], [1, 4], [0, 5],
         [5, 2], [4, 3], [3, 4], [2, 5], [1, 6], [0, 7]]
    Y = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    output = cer.find_svm(X, Y)

    assert output.predict([0, 0]) == 0
    assert output.predict([1, 1]) == 0
    assert output.predict([2, 2]) == 0
    assert output.predict([3, 3]) == 1
    assert output.predict([4, 4]) == 1
    assert output.predict([5, 5]) == 1
    assert output.predict([0.5, 0.5]) == 0


def test_save_svm_model():
    """
    Test save_svm_model functionality from cervical.py
    """

    from sklearn.externals import joblib

    X = [[5, 0], [4, 1], [3, 2], [2, 3], [1, 4], [0, 5],
         [5, 2], [4, 3], [3, 4], [2, 5], [1, 6], [0, 7]]
    Y = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    clf = cer.find_svm(X, Y)
    cer.save_svm_model(clf, 'test_svm_model.pkl')

    output = joblib.load('test_svm_model.pkl')

    # Case 1
    assert output.predict([0, 0]) == 0
    assert output.predict([1, 1]) == 0
    assert output.predict([2, 2]) == 0
    assert output.predict([3, 3]) == 1
    assert output.predict([4, 4]) == 1
    assert output.predict([5, 5]) == 1

    # Case 2
    X = [[1, 0], [2, 1], [3, 2], [4, 3], [5, 4], [6, 5],
         [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]]
    Y = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    clf = cer.find_svm(X, Y)
    cer.save_svm_model(clf, 'test_svm_model.pkl')
    output = joblib.load('test_svm_model.pkl')

    assert output.predict([2, 0]) == 0
    assert output.predict([3, 0]) == 0
    assert output.predict([4, 1]) == 0
    assert output.predict([3, 3]) == 1
    assert output.predict([0, 4]) == 1
    assert output.predict([1, 5]) == 1
