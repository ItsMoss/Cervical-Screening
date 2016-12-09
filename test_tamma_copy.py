import tamma_copy as tm


def test_remove_glare():
    """
    Tests remove glare functionality from tamma_copy.py
    """

    input1 = [1] * 256
    expected_output1 = [1] * 241 + [0] * 15
    output1 = tm.remove_glare(input1, 240)
    assert output1 == expected_output1

    input2 = [1] * 256
    expected_output2 = [1] * 256
    output2 = tm.remove_glare(input2, 256)
    assert output2 == expected_output2

    input3 = [1] * 256
    expected_output3 = [1] + [0] * 255
    output3 = tm.remove_glare(input3, 0)
    assert output3 == expected_output3


def test_remove_glare_wronginput():
    """
    Tests remove glare functionality from tamma_copy.py
    """

    input1 = [1]*250
    expected_output1 = [1]*241 + [0]*15
    output1 = tm.remove_glare(input1, 240)
    assert output1 == expected_output1

    input2 = [1]*270
    expected_output2 = [1]*241 + [0]*15
    output2 = tm.remove_glare(input2, 240)
    assert output2 == expected_output2


def test_stat_analysis():
    """
    Tests for stat_analysis functionality from tamma_copy.py
    """

    input1 = [1] * 241 + [0] * 15
    expected_output1 = [1.0, 1.0, 1.0, 0.0]
    output1 = tm.stat_analysis(input1)
    assert output1 == expected_output1

    input2 = list(range(241)) + [0] * 15
    expected_output2 = [120.0, 0.0, 120.0, 69.7]
    output1 = tm.stat_analysis(input2)
    assert output2 == expected_output2

    input3 = [0]*15 + list(range(226)) + [0] * 15
    expected_output3 = [112.5, 0.0, 112.5, 65.4]
    output3 = tm.stat_analysis(input3)
    assert output3 == expected_output3

    input4 = [0]*15 + list(range(101)) + [0] * 5 \
             + list(range(150)) + [0] * 15
    expected_output4 = [64.6, 0.0, 62, 40.2]
    output4 = tm.stat_analysis(input4)
    assert output4 == expected_output4

    input5 = [0] * 100 + [1] * 50 + [2] * 150
    expected_output5 = [1.6, 2.0, 2.0, 0.5]
    output5 = tm.stat_analysis(input5)
    assert output5 == expected_output5
