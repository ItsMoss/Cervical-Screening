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


def stat_analysis(input):
    """
    Perform statistical analysis on blue channels data
    :param input: input list for blue channels values (list)
    :return: stats: ([mean, mode, median, standard deviation])
    """

    import numpy as np
    from scipy import stats

    # create list of all blue channels values
    expanded_input = []
    rgb = list(range(256))
    for i in range (0,len(input)):
        repeated_rgb = [rgb[i]] * input[i]
        expanded_input =expanded_input + repeated_rgb

    # Calculate mean, mode, median, and standard deviation
    expanded_input = np.array(expanded_input)
    mean = np.mean(expanded_input)
    mode = stats.mode(expanded_input)
    median = np.median(expanded_input)
    std = np.std(expanded_input)

    # Adjust to 1 decimal floating values
    mean = round(mean,1)
    mode = round(float(mode[0]),1)
    median = round(median,1)
    std = round(float(std),1)

    stats = [mean, mode, median, std]

    return stats

