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

    input1 = [1] * 10 + [0] * 246
    expected_output1 = [4.5, 0.0, 4.5, 2.9]
    output1 = tm.stat_analysis(input1)
    assert output1 == expected_output1

    input2 = list(range(10)) + [0] * 246
    expected_output2 = [6.3, 9.0, 7.0, 2.2]
    output2 = tm.stat_analysis(input2)
    assert output2 == expected_output2

    input3 = [0]*15 + list(range(10)) + [0] * 231
    expected_output3 = [21.3, 24, 22, 2.2]
    output3 = tm.stat_analysis(input3)
    assert output3 == expected_output3

    input4 = [0]*15 + list(range(10)) + [0] * 5 \
             + list(range(10)) + [0] * 216
    expected_output4 = [28.8, 24, 27.5, 7.8]
    output4 = tm.stat_analysis(input4)
    assert output4 == expected_output4

