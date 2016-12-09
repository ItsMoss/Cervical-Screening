def remove_glare(input, threshold):
    """
    Remove reflective glare from blue channels data

    :param input: List of RGB values from 0-255 (list)
    :param threshold: threshold for removing glare (int)
    :return: output: List of RGB values from 0-255 after removing glare
    """

    # Check the size of input list
    if len(input) != 256:
        addlist = [0]*(256-len(input))
        input = input+addlist

    # Remove reflective glare by removing values greater than threshold
    output = input
    output[threshold+1:] = [0] * (255-threshold)

    return output
