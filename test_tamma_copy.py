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
    expected_output3 = [0] * 256
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
